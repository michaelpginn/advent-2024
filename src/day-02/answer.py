import torch

from src.shared import padded_tensor_from_file, relative

r = relative(__file__)
t = padded_tensor_from_file(r("input.txt"))


def get_safe(t: torch.Tensor):
    diff = t.diff()

    # Check if each report is only increasing or only decreasing
    diff = diff.nan_to_num(posinf=0, neginf=0)
    satisfies_monotonic = torch.logical_or(
        torch.all(diff >= 0, dim=1), torch.all(diff <= 0, dim=1)
    )

    # Check if we satisfy min and max
    diff_min = torch.abs(
        t.diff().nan_to_num(
            nan=torch.finfo(torch.float32).max, neginf=torch.finfo(torch.float32).max
        )
    )
    satisfies_min = diff_min.min(dim=1).values >= 1

    diff_max = torch.abs(t.diff().nan_to_num(nan=0, neginf=0))
    satisfies_max = diff_max.max(dim=1).values <= 3

    safe = torch.logical_and(
        torch.logical_and(satisfies_monotonic, satisfies_min), satisfies_max
    )
    return safe


safe = get_safe(t)
print("Part 1:", safe.sum().item())

safe_with_dampener = safe
for col in range(t.size(1)):
    omitting_column = torch.cat((t[:, :col], t[:, col + 1 :]), dim=1)
    safe_omitting_column = get_safe(omitting_column)
    safe_with_dampener = torch.logical_or(safe_with_dampener, safe_omitting_column)

print("Part 2:", safe_with_dampener.sum().item())
