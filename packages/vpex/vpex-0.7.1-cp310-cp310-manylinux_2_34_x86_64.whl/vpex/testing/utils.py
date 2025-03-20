import os
import random
import torch
import torch.testing
import unittest
import numpy as np
import itertools
from dataclasses import dataclass
from beartype.typing import (Sequence, Union, Tuple, Any, Optional, List, Dict)

__all__ = [
    "CHARM_NUMBER",
    "CHARM_NUMBER_F",
    "is_floating_point",
    "flush_seed",
    "is_device_kwarg",
    "clone_tensors",
    "clone_out_tensors",
    "convert_to_vtal_arg",
    "convert_to_vtal_args",
    "convert_to_vtal_kwargs",
    "convert_to_cpu_args",
    "half_to_float",
    "compare_tensor",
    "compare_result",
    "compare_results",
    "full_tensor",
    "create_tensor",
    "create_tensor_no_zero",
    "create_int_tensor",
    "create_bool_tensor",
    "randperm_tensor",
    "assert_equal",
    "assert_rtol_equal",
    "assert_true",
    "pack_param_list",
    "BaseFnTest",
    "set_test_tolerance",
    "Tolerance",
    "HalfTolerance",
]

CHARM_NUMBER = 688521
CHARM_NUMBER_F = 688.521

@dataclass(frozen=True)
class Tolerance:
    atol: float = 1e-5
    rtol: float = 1e-5

    def __call__(self):
        return self.atol, self.rtol

@dataclass(frozen=True)
class HalfTolerance(Tolerance):
    atol: float = 1e-3
    rtol: float = 1e-3

@dataclass(frozen=True)
class IntTolerance(Tolerance):
    atol: float = 0
    rtol: float = 0

def is_floating_point(x: Union[torch.dtype, torch.Tensor]) -> bool:
    if isinstance(x, torch.Tensor):
        return torch.is_floating_point(x)
    return x in [torch.float32, torch.float16, torch.float64,
                 torch.float8_e4m3fn,
                 torch.float8_e4m3fnuz,
                 torch.float8_e5m2,
                 torch.float8_e5m2fnuz,
                 ]

def is_sequence_arg0(*args) -> bool:
    return len(args) == 1 and isinstance(args[0], Sequence)

def is_tensor_list(arg) -> bool:
    if not isinstance(arg, Sequence):
        return False
    for a in arg:
        if not isinstance(a, torch.Tensor):
            return False
    return True

def flush_seed(seed):
    os.environ['PYTHONHASHSEED'] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def assert_true(value: bool):
    assert value

def assert_equal(a, b):
    torch.testing.assert_close(a, b, rtol=0, atol=0)

def assert_rtol_equal(a, b, rtol=0, atol=1e-5):
    if not np.issubdtype(a.dtype, np.floating):
        rtol = 0
    torch.testing.assert_close(a, b, rtol=rtol, atol=atol)

def is_device_kwarg(name) -> bool:
    return name == "device"

def convert_to_vtal_arg(arg):
    if isinstance(arg, torch.Tensor):
        arg = arg.to("vsi")
    return arg

def convert_to_vtal_args(*args):
    new_args = []
    for arg in args:
        new_args.append(convert_to_vtal_arg(arg))
    return new_args

def convert_to_vtal_kwargs(**kwargs):
    new_kwargs = {}
    for k,arg in kwargs.items():
        if isinstance(arg, torch.Tensor):
            arg = arg.to("vsi")
        elif is_tensor_list(arg):
            arg = convert_to_vtal_args(*arg)
        elif is_device_kwarg(k):
            arg = "vsi"
        new_kwargs[k] = arg
    return new_kwargs

def clone_tensors(*args) -> List[torch.Tensor]:
    new_args = []
    if is_sequence_arg0(*args):
        return clone_tensors(*args[0])
    for arg in args:
        new_args.append(arg.clone())
    if len(args) == 1:
        return new_args[0]
    return new_args

def clone_out_tensors(**kwargs) -> Dict[str, Any]:
    new_args = {}
    for k,arg in kwargs.items():
        if isinstance(arg, torch.Tensor):
            new_args[k] = arg.clone()
        else:
            new_args[k] = arg
    return new_args

def half_to_float(x: torch.Tensor):
    if x is not None and x.dtype == torch.float16:
        return x.to(torch.float32)
    return x

def convert_to_cpu_args(*args):
    if is_sequence_arg0(*args):
        return convert_to_cpu_args(*args[0])
    new_args = []
    for arg in args:
        if isinstance(arg, torch.Tensor):
            if not arg.is_contiguous():
                arg = arg.contiguous()
            arg = arg.to("cpu")
        new_args.append(arg)
    if len(args) == 1:
        return new_args[0]
    return new_args

def get_tolerance(type_tolerances: Dict[torch.dtype, Tolerance],
                  dtype, atol: float, rtol: float) -> Tuple[float, float]:
    if dtype in type_tolerances:
        return type_tolerances[dtype]()
    atol = atol
    rtol = rtol
    return atol, rtol

def compare_tensor(gdn: torch.Tensor, ref: torch.Tensor,
                   atol: float = 1e-5,
                   rtol: float = 1e-5,
                   assert_false: bool = True) -> bool:
    if isinstance(gdn, torch.Tensor):
       gdn = gdn.detach().numpy()
    if isinstance(ref, torch.Tensor):
       ref = ref.detach().numpy()
    if not (gdn.shape == ref.shape):
        print(f"Shape mismatch {gdn.shape} vs {ref.shape}")
    if not (gdn.dtype == ref.dtype):
        print(f"Dtype mismatch {gdn.dtype} vs {ref.dtype}")
    assert gdn.dtype == ref.dtype
    assert gdn.shape == ref.shape
    #print('...')
    #print(gdn.shape)
    #print(gdn)
    #print('...')
    #print(ref.shape)
    #print(ref)
    gdn = gdn.flatten()
    ref = ref.flatten()
    gdn = np.nan_to_num(gdn)
    ref = np.nan_to_num(ref)
    #print("max error", (np.abs(gdn - ref)).max())
    if assert_false:
        assert_rtol_equal(gdn, ref, rtol, atol)
        return False
    else:
        return np.isclose(gdn, ref, atol=atol, rtol=rtol).all()

def try_copy_contiguous(tensor: torch.Tensor) -> torch.Tensor:
    if not tensor.is_contiguous():
        tensor = tensor.contiguous()
    return tensor

def compare_result(gdn, ref, atol: float = 1e-5, rtol: float = 1e-5,
                   assert_false: bool = True,
                   type_tolerances: Dict[torch.dtype, Tolerance] = {},
                   ) -> bool:
    assert type(gdn) == type(ref)
    if isinstance(gdn, torch.Tensor):
        atol, rtol = get_tolerance(type_tolerances, gdn.dtype, atol, rtol)
        gdn = try_copy_contiguous(gdn)
        ref = try_copy_contiguous(ref)
        return compare_tensor(gdn, ref, atol, rtol, assert_false)
    else:
        return gdn == ref

def compare_results(gdns, refs,
                    atols: Union[Sequence[float], float] = 1e-5,
                    rtols: Union[Sequence[float], float] = 1e-6,
                    type_tolerances: Dict[torch.dtype, Tolerance] = {},
                    assert_false: bool = True,
                    ) -> bool:
    if not isinstance(gdns, Sequence):
        gdns = [gdns]
    if not isinstance(refs, Sequence):
        refs = [refs]
    assert len(gdns) == len(refs), f"Output number mismatch {len(gdns)} vs {len(refs)}"
    if not isinstance(atols, Sequence):
        atols = [atols] * len(gdns)
    if not isinstance(rtols, Sequence):
        rtols = [rtols] * len(gdns)
    all_pass = True
    for i, item in enumerate(zip(gdns, refs)):
        g, r = item
        #print(f"compare {i} output")
        all_pass = all_pass and compare_result(g, r, atols[i], rtols[i],
                                               assert_false, type_tolerances)
    return all_pass

def full_tensor(dtype, shape: Tuple[int, ...],
                value: Tuple[float, int],
                device=None) -> torch.Tensor:
    x = torch.empty(shape, dtype=dtype, device=device)
    x.fill_(value)
    return x

def create_tensor(dtype, shape: Tuple[int, ...],
                  range: Tuple[float, float] = (0, 1.0),
                  device=None) -> torch.Tensor:
    x = torch.rand(shape, dtype=torch.float32)
    x = x * (range[1] - range[0]) + range[0]
    if dtype != torch.float32:
        x = x.to(dtype)
    if device:
        x = x.to(device)
    return x

def create_tensor_no_zero(dtype, shape: Tuple[int, ...],
                  range: Tuple[float, float] = (0, 1.0),
                  device=None) -> torch.Tensor:

    x = torch.rand(shape, dtype=torch.float32)
    x = x * (range[1] - range[0]) + range[0]
    if dtype != torch.float32:
        x = x.to(dtype)
    ones = torch.ones_like(x)
    x = torch.where(x != 0, x, ones)
    if device:
        x = x.to(device)
    return x

def create_int_tensor(shape: Tuple[int, ...],
                  range: Tuple[float, float] = (0, 100),
                  dtype = torch.int64,
                  device=None) -> torch.Tensor:
    x = torch.randint(range[0], range[1], shape, dtype=dtype)
    if device:
        x = x.to(device)
    return x

def create_bool_tensor(shape: Tuple[int, ...],
                       ratio = 0.5,
                       device=None) -> torch.Tensor:
    x = torch.rand(shape, dtype=torch.float32)
    x = x > ratio
    if device:
        x = x.to(device)
    return x

def randperm_tensor(shape: Tuple[int, ...],
                    n: Optional[int] = None,
                    dtype = torch.int64,
                    device = None) -> torch.Tensor:
    tensor_size = int(np.prod(shape))
    if n is None:
        n = tensor_size
    else:
        assert tensor_size <= n
    x = torch.randperm(n, dtype=dtype)
    if n > tensor_size:
        x = x[:tensor_size].clone()
    x = x.reshape(shape)
    if device:
        x = x.to(device)
    return x

def pack_param_list(*lists) -> Sequence[Tuple[Any, ...]]:
    return list(itertools.product(*lists))

def set_test_tolerance(type_tolerances: Dict[torch.dtype, Tolerance] = {}):
    def decorator(cls):
        class WrappedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, type_tolerances=type_tolerances, **kwargs)
        return WrappedClass
    return decorator

class BaseFnTest(unittest.TestCase):
    def __init__(self, *args,
                type_tolerances: Dict[torch.dtype, Tolerance] = {},
                **kwargs):
        super(BaseFnTest, self).__init__(*args, **kwargs)
        self.type_tolerances = type_tolerances.copy()

    def setUp(self):
        flush_seed(CHARM_NUMBER)

    def run_cpu(self, fn, *args, **kwargs):
        kwargs = clone_out_tensors(**kwargs)
        return fn(*args, **kwargs)

    def run_vtal(self, fn, *args, **kwargs):
        vtal_args = convert_to_vtal_args(*args)
        vtal_kwargs = convert_to_vtal_kwargs(**kwargs)
        return fn(*vtal_args, **vtal_kwargs)

    def run_cpu_attr(self, fn: str, tensor: torch.Tensor, *args, **kwargs):
        kwargs = clone_out_tensors(**kwargs)
        tensor = tensor.clone()
        return getattr(tensor, fn)(*args, **kwargs)

    def run_vtal_attr(self, fn: str, tensor: torch.Tensor, *args, **kwargs):
        tensor = tensor.to("vsi")
        vtal_args = convert_to_vtal_args(*args)
        vtal_kwargs = convert_to_vtal_kwargs(**kwargs)
        return getattr(tensor, fn)(*vtal_args, **vtal_kwargs)

    def run_and_compare(self, fn, *args,
                        atols: Union[Sequence[float], float] = 1e-5,
                        rtols: Union[Sequence[float], float] = 1e-6,
                        clone: bool = False,
                        **kwargs) -> bool:
        gdn = self.run_cpu(fn, *args, **kwargs)
        ref = self.run_vtal(fn, *args, **kwargs)
        if clone:
            gdn = clone_tensors(gdn)
            ref = clone_tensors(ref)
        ref = convert_to_cpu_args(ref)
        return compare_results(gdn, ref, atols, rtols,
                               type_tolerances=self.type_tolerances.copy())

    def run_and_compare_attr(self, fn: str, tensor: torch.Tensor,
                        *args,
                        atols: Union[Sequence[float], float] = 1e-5,
                        rtols: Union[Sequence[float], float] = 1e-6,
                        clone: bool = False,
                        **kwargs) -> bool:
        gdn = self.run_cpu_attr(fn, tensor, *args, **kwargs)
        ref = self.run_vtal_attr(fn, tensor, *args, **kwargs)
        if clone:
            gdn = clone_tensors(gdn)
            ref = clone_tensors(ref)
        ref = convert_to_cpu_args(ref)
        return compare_results(gdn, ref, atols, rtols,
                               type_tolerances=self.type_tolerances.copy())

    def run_and_compare_auto_devices(self, fn,
                        *args,
                        atols: Union[Sequence[float], float] = 1e-5,
                        rtols: Union[Sequence[float], float] = 1e-6,
                        clone: bool = False,
                        **kwargs) -> bool:
        gdn = self.run_cpu(fn, *args, device="cpu", **kwargs)
        ref = self.run_vtal(fn, *args, device="vsi", **kwargs)
        if clone:
            gdn = clone_tensors(gdn)
            ref = clone_tensors(ref)
        ref = convert_to_cpu_args(ref)
        return compare_results(gdn, ref, atols, rtols,
                               type_tolerances=self.type_tolerances.copy())
