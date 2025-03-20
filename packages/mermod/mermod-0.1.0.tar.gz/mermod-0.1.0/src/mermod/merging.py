import functools
import gc
import json
import logging
import pathlib
import shutil
import sys
import time
from typing import Any, Optional

import torch

from . import io, utils

logger = logging.getLogger(__name__)


def partition_to_batches(lst: list[Any], batch_size: int, reverse: bool) -> list[Any]:
    batches = [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]
    if reverse:
        return [batch[::-1] for batch in batches][::-1]
    return batches


def find_duplicates(batches):
    res_set = set()
    duplicates = []

    for b in batches:
        for bi in b:
            if bi in res_set:
                duplicates.append(bi)
            else:
                res_set.add(bi)
    return duplicates


def check_if_unique(batches):
    duplicates = find_duplicates(batches)
    assert len(duplicates) == 0, f"Duplicate weights found {duplicates}"


def prepare_batches(*, weight_names, weight_batch_size, weight_batches_custom, reverse):

    if weight_batches_custom:
        weights_to_skip = set()
        for b in weight_batches_custom:
            weights_to_skip.update(b)
        weight_names_no_custom = [w for w in weight_names if w not in weights_to_skip]
        res = weight_batches_custom + partition_to_batches(
            weight_names_no_custom, weight_batch_size, reverse
        )
    else:
        res = partition_to_batches(weight_names, weight_batch_size, reverse)
    check_if_unique(res)
    return res


def get_tensor_size_mb(w: torch.Tensor) -> float:
    return (w.nelement() * w.element_size()) / 1024**2


def get_rand(*, size, device, gen, seed):
    gen.manual_seed(seed)
    return torch.rand(size=size, generator=gen, device=device)


def get_randperm(*, n, device, gen, seed):
    gen.manual_seed(seed)
    return torch.randperm(n, generator=gen, device=device)


def mask_random(*, t: torch.Tensor, sparsity: float, device, gen, seed):
    rand_tensor = get_rand(size=t.shape, device=device, gen=gen, seed=seed)
    mask = torch.where(rand_tensor > sparsity, 1.0, 0.0)
    return t * mask, mask


def create_random_interleaved_masks(k: int, shape, gen, seed, device):
    # Create a tensor of indices
    total_elements = torch.prod(torch.tensor(shape)).item()
    msg = f"Creating indices - num elements {total_elements/1.0e6} M"
    utils.log_memory(logger, msg)
    indices = get_randperm(n=total_elements, device=device, gen=gen, seed=seed)
    logger.info(f"Created inidices - tensor size {get_tensor_size_mb(indices)} MB")

    # Calculate elements per mask (ensuring equal distribution)
    elements_per_mask = total_elements // k

    # Create empty masks
    masks = torch.zeros((k,) + shape, device=device)

    # Fill each mask with 1s in its designated positions
    for i in range(k):
        start_idx = i * elements_per_mask
        end_idx = (i + 1) * elements_per_mask if i < k - 1 else total_elements

        # Get the random positions for this mask
        mask_indices = indices[start_idx:end_idx]

        # Convert linear indices to subscript indices
        if len(shape) == 1:
            masks[i].view(-1)[mask_indices] = 1.0
        else:
            row_indices = mask_indices // shape[1]
            col_indices = mask_indices % shape[1]
            masks[i][row_indices, col_indices] = 1.0

    return masks


def get_pruned_diff(
    diff: torch.Tensor,
    sparsity: float,
    per_row: bool = False,
    per_column: bool = False,
):
    if per_row and len(diff.shape) == 2:
        masks = []
        for row_id in range(diff.shape[0]):
            _, row_mask = get_pruned_diff(diff[row_id], sparsity=sparsity)
            masks.append(row_mask)

        mask = torch.stack(masks, dim=0)
        return mask * diff, mask
    if per_column and len(diff.shape) == 2:
        masks = []
        for column_id in range(diff.shape[1]):
            _, column_mask = get_pruned_diff(diff[:, column_id], sparsity=sparsity)
            masks.append(column_mask)

        mask = torch.stack(masks, dim=1)
        return mask * diff, mask

    abs_diff = torch.abs(diff)
    original_shape = diff.shape
    _, indices = torch.topk(abs_diff.flatten(), k=int((1 - sparsity) * diff.numel()))
    mask = torch.zeros_like(abs_diff.flatten())
    mask[indices] = 1.0
    mask = mask.reshape(original_shape)
    return diff * mask, mask


def get_joint_pruned_diff(
    task_vectors: dict[str, torch.Tensor],
    sparsity: float,
):
    abs_diffs = torch.stack([torch.abs(t) for t in task_vectors.values()], dim=0)
    device = abs_diffs.device
    original_shape = abs_diffs.shape
    n_abs_diffs = abs_diffs.numel()
    _, indices = torch.topk(abs_diffs.flatten(), k=int((1 - sparsity) * n_abs_diffs))
    del abs_diffs
    masks = torch.zeros(n_abs_diffs, device=device)
    masks[indices] = 1.0
    masks = masks.reshape(original_shape)
    masks_list = torch.unbind(masks, dim=0)

    for_iter = zip(task_vectors.keys(), masks_list, task_vectors.values())

    for task_name, mask, task_vector in for_iter:
        task_vectors[task_name] = mask * task_vector
        del task_vector

    return task_vectors, masks_list


def get_first_value(d):
    return next(iter(d.values()))


def apply_ties_in_place(task_vectors):
    sum_values = torch.zeros_like(get_first_value(task_vectors), dtype=torch.float32)
    for tv in task_vectors.values():
        sum_values += tv
    sign = torch.sign(sum_values)
    del sum_values

    for task_name, task_vector in task_vectors.items():
        aligned_task_vector = torch.where(
            torch.sign(task_vector) == sign, task_vector, 0.0
        )
        task_vectors[task_name] = aligned_task_vector
        del task_vector


def all_tasks_vectors_zero(task_vectors):
    for task_vector in task_vectors.values():
        if torch.max(torch.abs(task_vector)) > 1.0e-6:
            return False
    return True


def merge_to_base_sd(
    *,
    base_sd,
    merged_sds,
    method: str = "dare",
    lambda_param: Optional[float] = 1.0,
    sparsity: float = 0.9,
    use_ties: bool = False,
    seed_dict: Optional[dict[str, int]] = None,
    device: torch.device,
    progress_bar,
):
    # TODO Matter only for abs_diff, either remove them totally or put them in config
    per_row = False
    per_column = False

    start = time.perf_counter()
    if str(device).startswith("cuda"):
        sfx = "_cuda"
    else:
        sfx = "_cpu"

    gen_for_seeds = torch.Generator()
    gen_for_tensors = torch.Generator(device=device)

    new_seed_dict = {}
    n = len(base_sd)

    for k, weight_name in enumerate(base_sd, start=1):
        utils.free_memory(f"{weight_name} - start")

        # BUILD TASK VECTORS
        task_vectors = {
            sd_name: (sd[weight_name] - base_sd[weight_name])
            for sd_name, sd in merged_sds.items()
        }

        utils.log_memory(logger, f"{weight_name} - task vectors")

        msg = f"Weight {k} of {n}: {weight_name}"
        if all_tasks_vectors_zero(task_vectors):
            logger.info(f"{msg} untrained parameters, skipping")
            continue
        else:
            weight_size = get_tensor_size_mb(base_sd[weight_name])
            logger.info(f"{msg} size={weight_size:.1f} MB")

        # CREATE MASKS AND TRIM TASK VECTOS

        masks = []

        if method.lower() == "dare":
            for task_name, task_vector in task_vectors.items():
                seed_id = f"{weight_name}@{task_name}:{sfx}"
                if seed_dict is not None:
                    seed = seed_dict[seed_id]
                else:
                    assert seed_id not in new_seed_dict
                    seed = gen_for_seeds.seed()
                    new_seed_dict[seed_id] = seed
                pruned_task_vector, mask = mask_random(
                    t=task_vector,
                    sparsity=sparsity,
                    seed=seed,
                    gen=gen_for_tensors,
                    device=device,
                )
                task_vectors[task_name] = pruned_task_vector
                masks.append(mask)

        elif method.lower() == "dare_disjoint":
            utils.log_memory(logger, "dare disjoint start")
            seed_id = f"{weight_name}@PERMUTATION:{sfx}"
            if seed_dict is not None:
                seed = seed_dict[seed_id]
            else:
                seed = gen_for_seeds.seed()
                new_seed_dict[seed_id] = seed
            shape = get_first_value(task_vectors).shape
            initial_masks = create_random_interleaved_masks(
                k=len(task_vectors),
                shape=shape,
                gen=gen_for_tensors,
                seed=seed,
                device=device,
            )
            task_iter = zip(task_vectors.keys(), task_vectors.values(), initial_masks)
            for task_name, task_vector, mask0 in task_iter:
                seed_id = f"{weight_name}@{task_name}:{sfx}"
                if seed_dict is not None:
                    seed = seed_dict[seed_id]
                else:
                    seed = gen_for_seeds.seed()
                    new_seed_dict[seed_id] = seed
                rand_mask = get_rand(
                    size=mask0.shape, device=device, gen=gen_for_tensors, seed=seed
                )
                mask1 = torch.where(rand_mask > sparsity, mask0, 0.0)
                task_vectors[task_name] = mask1 * task_vector
                masks.append(mask1)

        elif method.lower() == "abs_diff":
            for task_name, task_vector in task_vectors.items():
                pruned_task_vector, mask = get_pruned_diff(
                    task_vector, sparsity, per_row=per_row, per_column=per_column
                )
                task_vectors[task_name] = pruned_task_vector
                masks.append(mask)
                del task_vector
        elif method.lower() == "joint_abs_diff":
            task_vectors, masks = get_joint_pruned_diff(
                task_vectors=task_vectors, sparsity=sparsity
            )
        else:
            raise ValueError(f'Unknown merge method - "{method}"')

        # APPLY TIES ALIGNMENT

        if use_ties:
            logger.info("Using ties")
            apply_ties_in_place(task_vectors)
        else:
            logger.info("Not using ties")

        # CREATE MERGED PARAM VALUE

        if lambda_param is None:
            mask_sum = functools.reduce(torch.max, masks)
            current_lambda_param = 1.0 / mask_sum.mean()
            logger.info(f"Current lambda: {current_lambda_param}")
        else:
            current_lambda_param = lambda_param

        for task_vector in task_vectors.values():
            base_sd[weight_name] += current_lambda_param * task_vector

        del task_vectors
        del masks
        gc.collect()
        utils.free_memory()
        msg = f"Finished weight {k} of {n}: {weight_name} [{weight_size:.1f} MB]"
        logger.info(msg)
        progress_bar.update()

    time_merging = time.perf_counter() - start
    logger.info(f"t = {time_merging:5.2f} s - merging {len(base_sd)} layers")

    if seed_dict is None:
        return new_seed_dict, time_merging
    else:
        return seed_dict, time_merging


def log_sd(sd_name, sd):
    sd_size = 0
    for k, v in sd.items():
        sd_size += sys.getsizeof(v.untyped_storage())
    logger.info(f"MEM {sd_name}: len={len(sd)} size={sd_size/1024**3:.2f} GB")


def _merge_one_batch(
    *,
    sd_base_path,
    sd_merged_paths,
    names_batch,
    method,
    sparsity,
    use_ties,
    lambda_param,
    seed_dict,
    seed_dict_new,
    sd_out_path,
    device,
    progress_bar,
):
    tot_t_compute, tot_t_io = 0.0, 0.0
    base_partial_sd, t_io = io.load_partial_sd(sd_base_path, names_batch, device)
    tot_t_io += t_io

    merged_partial_sds = {}
    for sd_name, sd_path in sd_merged_paths.items():
        sd, t_io = io.load_partial_sd(sd_path, names_batch, device)
        tot_t_io += t_io
        merged_partial_sds[sd_name] = sd
        log_sd(sd_name, sd)

    with torch.no_grad():
        partial_seed_dict, t_compute = merge_to_base_sd(
            base_sd=base_partial_sd,
            merged_sds=merged_partial_sds,
            method=method,
            sparsity=sparsity,
            lambda_param=lambda_param,
            use_ties=use_ties,
            seed_dict=seed_dict,
            device=device,
            progress_bar=progress_bar,
        )
    tot_t_compute += t_compute

    if seed_dict is None:
        seed_dict_new.update(partial_seed_dict)

    tot_t_io += io.save_partial_sd(base_partial_sd, sd_out_path)
    tot_tensors_size = 0
    for tensor in base_partial_sd.values():
        tot_tensors_size += tensor.element_size() * tensor.nelement()

    for k in merged_partial_sds:
        v = merged_partial_sds[k]
        merged_partial_sds[k] = None
        utils.delete_sd(v)

    del merged_partial_sds
    utils.delete_sd(base_partial_sd)
    del base_partial_sd

    gc.collect()

    return tot_tensors_size, tot_t_compute, tot_t_io


def get_empty_hf_index():
    return {"metadata": {"total_size": 0}, "weight_map": {}}


def update_hf_index_in_place(hf_index, names_batch, sd_fname, batch_tot_tensors_size):
    hf_index["metadata"]["total_size"] += batch_tot_tensors_size
    weight_map = hf_index["weight_map"]

    for wn in names_batch:
        assert wn not in weight_map
        weight_map[wn] = sd_fname


def merge(
    *,
    sd_base_path,
    sd_merged_paths,
    method,
    sparsity,
    use_ties,
    lambda_param,
    weight_batch_size,
    weight_batches_custom,
    sd_output_path,
    seed_dict,
    merge_device,
    use_progress_bar=True,
):
    logger.info(f"{merge_device=}")
    start = time.perf_counter()
    tot_t_compute, tot_t_io = 0.0, 0.0
    sd_output_path = pathlib.Path(sd_output_path)

    if io.get_sd_type(sd_output_path, should_exist=False) == io.FORMAT_HF:
        merging_tmp_dir = sd_output_path
        merging_tmp_dir.mkdir(exist_ok=True)
    else:
        merging_tmp_dir = io.mkdir_tmp()

    try:
        logger.info(f"{sd_base_path=}")
        logger.info(f"{sd_merged_paths=}")

        weight_names, t_io = io.get_weight_names(sd_base_path)
        tot_t_io += t_io
        weights_names_batches = prepare_batches(
            weight_names=weight_names,
            weight_batch_size=weight_batch_size,
            weight_batches_custom=weight_batches_custom,
            reverse=False,
        )

        n_weights = len(weight_names)
        n_batches = len(weights_names_batches)
        partial_paths = []
        logger.info(f"{n_weights=} {n_batches=} {weight_batch_size=}")

        seed_dict_new = {}
        hf_index = get_empty_hf_index()

        with utils.ProgressBar(
            total=n_weights,
            desc="Merge",
            units="layers",
            enabled=use_progress_bar,
        ) as progress_bar:
            for i, names_batch in enumerate(weights_names_batches, start=1):
                mem1 = utils.get_cpu_reserved_memory_gb()
                mem1_gpu = utils.get_gpu_reserved_memory_gb()
                sd_fname = f"model-{i:05d}-{n_batches:05d}.safetensors"
                sd_out_path = merging_tmp_dir / sd_fname
                batch_tot_tensors_size, t_compute, t_io = _merge_one_batch(
                    sd_base_path=sd_base_path,
                    sd_merged_paths=sd_merged_paths,
                    sd_out_path=sd_out_path,
                    names_batch=names_batch,
                    method=method,
                    sparsity=sparsity,
                    use_ties=use_ties,
                    lambda_param=lambda_param,
                    seed_dict=seed_dict,
                    seed_dict_new=seed_dict_new,
                    device=merge_device,
                    progress_bar=progress_bar,
                )
                update_hf_index_in_place(
                    hf_index=hf_index,
                    names_batch=names_batch,
                    sd_fname=sd_fname,
                    batch_tot_tensors_size=batch_tot_tensors_size,
                )
                tot_t_compute += t_compute
                tot_t_io += t_io
                partial_paths.append(sd_out_path)
                utils.free_memory()

            mem2 = utils.get_cpu_reserved_memory_gb()
            mem2_gpu = utils.get_gpu_reserved_memory_gb()
            logger.info(f"MEM {mem2=:.2f} {mem2_gpu=:.2f}")
            memd = mem1 - mem2
            prefix = "MEM CPU usage during iteration - "
            logger.info(f"{prefix} {mem1:.2f} -> {mem2:.2f} GB [freed {memd:.2f} GB]")
            prefix = "MEM GPU usage during iteration - "
            memd = mem1_gpu - mem2_gpu
            msg = f"{prefix} {mem1_gpu:.2f} -> {mem2_gpu:.2f} GB [freed {memd:.2f} GB]"
            logger.info(msg)

        with open(merging_tmp_dir / io.HF_MODEL_INDEX_FNAME, "wt") as f:
            json.dump(hf_index, f)

        if seed_dict is None:
            seed_dict = seed_dict_new

        merge_device = torch.device("cpu")
        if merging_tmp_dir != sd_output_path:
            t_io = io.merge_partial_sds(sd_output_path, partial_paths, merge_device)
        tot_t_io += t_io
        utils.log_memory(logger, "after merging")
    finally:
        if merging_tmp_dir != sd_output_path:
            shutil.rmtree(merging_tmp_dir)

    time_full = time.perf_counter() - start
    logger.info(f"Merge time io:      {tot_t_io/60.0:6.2f} min")
    logger.info(f"Merge time compute: {tot_t_compute/60.0:6.2f} min")
    logger.info(f"Merge time tot:     {time_full/60.0:6.2f} min")
    timing_dict = {
        "merge_time_io": tot_t_io,
        "merge_time_compute": tot_t_compute,
        "merge_time_total": time_full,
    }
    return seed_dict, timing_dict
