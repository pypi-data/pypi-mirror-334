import os
import threading
import traceback
from multiprocessing.util import register_after_fork as _register_after_fork
import torch
import vpex
from typing import Tuple, Union
from .utils import (current_device, device_count, set_device, device, _DeviceGuard, synchronize, current_stream)
from .streams import Stream, Event

default_generators: Tuple[torch._C.Generator] = ()  # type: ignore[assignment]

_is_internal_in_bad_fork = False
_initialized = False
_tls = threading.local()
_initialization_lock = threading.Lock()
_queued_calls = []  # don't invoke these until initialization occurs
_original_pid = False

def _is_in_bad_fork():
    return _is_internal_in_bad_fork

def is_initialized():
    return _initialized and not _is_internal_in_bad_fork

def _lazy_call(cb):
    if _initialized:
        cb()
    else:
        # Don't store the actual traceback to avoid memory cycle
        _queued_calls.append((cb, traceback.format_stack()))

class DeferredVtalCallError(Exception):
    pass

def init():
    r"""Initialize PyTorch's VSI state.  You may need to call
    this explicitly if you are interacting with PyTorch via
    its C API, as Python bindings for VSI functionality will not
    be until this initialization takes place.  Ordinary users
    should not need this, as all of PyTorch's VSI methods
    automatically initialize VSI state on-demand.

    Does nothing if the VSI state is already initialized.
    """
    vpex.vtal._lazy_init()


def _lazy_init():
    def _queue_call(queued_calls):
        for queued_call, orig_traceback in queued_calls:
            try:
                queued_call()
            except Exception as e:
                msg = (f"VSI call failed lazily at initialization with error: {str(e)}\n\n"
                       f"VSI call was originally invoked at:\n\n{orig_traceback}")
                raise DeferredVtalCallError(msg) from e

    global _initialized, _original_pid, _queued_calls
    if _initialized or hasattr(_tls, 'is_initializing'):
        return
    with _initialization_lock:
        # We be double-checked locking, boys!  This is OK because
        # the above test was GIL protected anyway.  The inner test
        # is for when a thread blocked on some other thread which was
        # doing the initialization; when they get the lock, they will
        # find there is nothing left to do.
        if _initialized:
            return
        # It is important to prevent other threads from entering _lazy_init
        # immediately, while we are still guaranteed to have the GIL, because some
        # of the C calls we make below will release the GIL
        if _is_internal_in_bad_fork:
            raise RuntimeError(
                "Cannot re-initialize VSI in forked subprocess. To use VSI with "
                "multiprocessing, you must use the 'spawn' start method")

        vpex._C._lazy_init()

        _original_pid = os.getpid()
        # Some of the queued calls may reentrantly call _lazy_init();
        # we need to just return without initializing in that case.
        # However, we must not let any *other* threads in!
        _tls.is_initializing = True
        try:
            _queue_call(_queued_calls)
        finally:
            delattr(_tls, 'is_initializing')
        _initialized = True

def _after_fork(arg):
    global _initialized, _is_internal_in_bad_fork
    if _initialized and _original_pid != os.getpid():
        _initialized = False
        _is_internal_in_bad_fork = True
        #vpex._C._vtal_set_run_yet_variable_to_false()

_register_after_fork(_after_fork, _after_fork)

def _get_device(device: Union[int, str, torch.device]) -> torch.device:
    r"""Return the torch.device type object from the passed in device.

    Args:
        device (torch.device or int): selected device.
    """
    if isinstance(device, str):
        return torch.device(device)
    elif isinstance(device, int):
        return torch.device('vsi', device)
    return device


def _get_generator(device: torch.device) -> torch._C.Generator:
    r"""Return the VSI Generator object for the given device.

    Args:
        device (torch.device): selected device.
    """

    idx = device.index
    if idx is None:
        idx = current_device()
    return torch.vsi.default_generators[idx]


def _set_rng_state_offset(offset: int, device: Union[int, str, torch.device] = 'vsi') -> None:
    r"""Sets the random number generator state offset of the specified VSI.

    Args:
        offset (int): The desired offset
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``'vsi'`` (i.e., ``torch.device('vsi')``, the current VSI device).
    """
    final_device = _get_device(device)

    def cb():
        default_generator = _get_generator(final_device)
        default_generator.set_offset(offset)

    _lazy_call(cb)

def _get_rng_state_offset(device: Union[int, str, torch.device] = 'vsi') -> int:
    r"""Returns the random number generator state offset of the specified VSI.

    Args:
        device (torch.device or int, optional): The device to return the RNG state offset of.
            Default: ``'vsi'`` (i.e., ``torch.device('vsi')``, the current VSI device).

    .. warning::
        This function eagerly initializes VSI.
    """
    _lazy_init()
    final_device = _get_device(device)
    default_generator = _get_generator(final_device)
    return default_generator.get_offset()


def is_available():
   if (not hasattr(vpex._C, '_set_device')):
       return False
   return device_count() > 0

from .random import *