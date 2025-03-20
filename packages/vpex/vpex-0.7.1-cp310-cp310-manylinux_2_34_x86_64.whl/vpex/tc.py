import numpy as np
from beartype import beartype
from beartype.typing import Optional, Union, Type
import vpex._C

__all__ = ["np_bfloat16", "encode_gptj_coef"]

np_bfloat16 = np.dtype([("bfloat16", np.uint16)])

def str_dtype_to_np(dtype: str) -> np.dtype:
    _map = {
        "bfloat16": np_bfloat16,
        "half": np.float16,
        "float": np.float32,
        "int8": np.int8,
        "int16": np.int16,
        "int32": np.int32,
        "int64": np.int64,
        "uint8": np.uint8,
        "uint16": np.uint16,
        "uint32": np.uint32,
        "uint64": np.uint64,
    }

    if dtype not in _map:
        raise NotImplementedError(
          f"Unsupport str dtype {dtype}, allow {_map.keys()}")
    return _map[dtype]

@beartype
def read_numpy(data: np.ndarray,
               cast_type: Optional[Union[Type[np.generic], str]] = None
) -> np.ndarray:
    if isinstance(cast_type, str):
      cast_type = str_dtype_to_np(cast_type)
    if cast_type is not None and cast_type != data.dtype:
      data = data.astype(cast_type)
    return data

def encode_gptj_coef(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    mlp1_weight: np.ndarray,
    mlp1_bias: np.ndarray,
    mlp2_weight: np.ndarray,
    mlp2_bias: np.ndarray,
    out_prj: np.ndarray,
    encode_dtype: str = "half"
) -> vpex._C.GPTJCoefs:
    allow_dtypes = ["half", "bfloat16"]
    if encode_dtype not in allow_dtypes:
        raise NotImplementedError(
          f"Unsupport encode gptj coef type {encode_dtype}, allow {allow_dtypes}")
    q = read_numpy(q, encode_dtype)
    k = read_numpy(k, encode_dtype)
    v = read_numpy(v, encode_dtype)
    mlp1_weight = read_numpy(mlp1_weight, encode_dtype)
    mlp1_bias = read_numpy(mlp1_bias, np.float32)
    mlp2_weight = read_numpy(mlp2_weight, encode_dtype)
    mlp2_bias = read_numpy(mlp2_bias, np.float32)
    out_prj = read_numpy(out_prj, encode_dtype)
    return vpex._C.encode_gptj_coef(
        q.view(np.uint16),
        k.view(np.uint16),
        v.view(np.uint16),
        mlp1_weight.view(np.uint16),
        mlp1_bias,
        mlp2_weight.view(np.uint16),
        mlp2_bias,
        out_prj.view(np.uint16))
