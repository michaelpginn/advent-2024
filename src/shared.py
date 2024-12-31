import torch
import os

def relative(script_file: str):
    dirname = os.path.dirname(script_file)
    def _r(filename: str):
        return os.path.join(dirname, filename)
    return _r


def tensor_from_file(filename: str) -> torch.Tensor:
    """Reads a file consisting of numbers and spaces and converts to a tensor"""
    with open(filename, "r") as f:
        contents = [[int(n) for n in line.split()] for line in f.readlines()]
        return torch.tensor(contents)

def nested_tensor_from_file(filename: str) -> torch.Tensor:
    with open(filename, "r") as f:
        contents = [torch.tensor([int(n) for n in line.split()]) for line in f.readlines()]
        return torch.nested.nested_tensor(contents)

def padded_tensor_from_file(filename: str, padding_value = -float("inf")) -> torch.Tensor:
    t = torch.nested.to_padded_tensor(nested_tensor_from_file(filename), padding=-1)
    t = t.to(torch.float)
    t[t==-1] = padding_value
    return t
