import torch
from src.shared import relative, tensor_from_file

r = relative(__file__)
t = tensor_from_file(r("input.txt"))

sorted, _ = t.sort(dim=0)
sum = (sorted[:,0] - sorted[:,1]).abs().sum()
print("Part 1:", sum.item())

score = (t[:,0] * t[:,1].bincount(minlength=t[:,0].max()+1)[t[:,0]]).sum()
print("Part 2:", score.item())
