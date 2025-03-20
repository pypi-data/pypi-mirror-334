from functools import lru_cache
import vpex
import vpex._C
import torch
from torch._utils import _get_device_index as _torch_get_device_index
from typing import Any


__all__ = ["current_device", "device_count", "set_device", "device", "device_of", "synchronize", "current_stream"]

def synchronize(device=None):
    r"""Waits for all kernels in all streams on a VSI device to complete.

    Arguments:
        device (torch.device or int, optional): device for which to synchronize.
            It uses the current device, given by :func:`~vpex.vtal.current_device`,
            if :attr:`device` is ``None`` (default).
    """
    vpex.vtal._lazy_init()
    with vpex.vtal.device(device):
        return vpex._C._synchronize()

def current_device():
    vpex.vtal._lazy_init()
    return vpex._C._get_device()

@lru_cache(maxsize=1)
def device_count():
    return vpex._C._get_device_count()

def set_device(device):
    device_id = _get_device_index(device, optional=True)
    if device_id >= 0:
        vpex._C._set_device(device_id)

class _DeviceGuard:
    def __init__(self, index: int):
        self.idx = index
        self.prev_idx = -1

    def __enter__(self):
        if self.idx == -1:
            return
        self.prev_idx = vpex._C._get_device()
        if self.prev_idx != self.idx:
            vpex._C._set_device(self.idx)
        vpex.vtal._lazy_init()

    def __exit__(self, type: Any, value: Any, traceback: Any):
        if self.prev_idx != self.idx:
            vpex._C._set_device(self.prev_idx)
        return False

class device(object):
    r"""Context-manager that changes the selected device.

    Arguments:
        device (torch.device or int): device index to select. It's a no-op if
            this argument is a negative integer or ``None``.
    """

    def __init__(self, device):
        self.idx = _get_device_index(device, optional=True)
        self.prev_idx = -1

    def __enter__(self):
        if self.idx == -1:
            return
        self.prev_idx = vpex._C._get_device()
        if self.prev_idx != self.idx:
            vpex._C._set_device(self.idx)
        vpex.vtal._lazy_init()

    def __exit__(self, *args):
        if self.prev_idx != self.idx:
            vpex._C._set_device(self.prev_idx)
        return False

def _get_device_index(device: Any, optional: bool = False,
                      allow_cpu: bool = False) -> int:
    r"""Gets the device index from :attr:`device`, which can be a torch.device
    object, a Python integer, or ``None``.

    If :attr:`device` is a torch.device object, returns the device index if it
    is a VSI device. Note that for a VSI device without a specified index,
    i.e., ``torch.device('vsi')``, this will return the current default VSI
    device if :attr:`optional` is ``True``. If :attr:`allow_cpu` is ``True``,
    CPU devices will be accepted and ``-1`` will be returned in this case.

    If :attr:`device` is a Python integer, it is returned as is.

    If :attr:`device` is ``None``, this will return the current default VSI
    device if :attr:`optional` is ``True``.
    """
    if isinstance(device, int):
        return device
    if isinstance(device, str):
        device = torch.device(device)
    if isinstance(device, torch.device):
        if allow_cpu:
            if device.type not in ['vsi', 'cpu']:
                raise ValueError('Expected a vsi or cpu device, but got: {}'.format(device) )
        elif device.type != 'vsi':
            raise ValueError('Expected a vsi device, but got: {}'.format(device))
    if not torch.jit.is_scripting():
        if isinstance(device, torch.vsi.device):
            return device.idx
    return _torch_get_device_index(device, optional, allow_cpu)

def _dummy_type(name):
    def init_err(self):
        class_name = self.__class__.__name__
        raise RuntimeError(
            "Tried to instantiate dummy base class {}".format(class_name)
        )

    return type(name, (object,), {"__init__": init_err})

if not hasattr(vpex._C, '_VtalStreamBase'):
    # Define dummy base classes
    vpex._C.__dict__['_VtalStreamBase'] = _dummy_type('VtalStreamBase')
    vpex._C.__dict__['_VtalEventBase'] = _dummy_type('VtalEventBase')

def current_stream(device=None):
    r"""Returns the currently selected :class:`Stream` for a given device.

    Arguments:
        device (torch.device or int, optional): selected device. Returns
            the currently selected :class:`Stream` for the current device, given
            by :func:`~vpex.vtal.current_device`, if :attr:`device` is ``None``
            (default).
    """
    vpex.vtal._lazy_init()
    streamdata = vpex._C._get_current_stream(
        _get_device_index(device, optional=True))
    return vpex.vtal.Stream(stream_id=streamdata[0], device_index=streamdata[1], device_type=streamdata[2])

# class device_of(device):
#     r"""Context-manager that changes the current device to that of given object.

#     You can use both tensors and storages as arguments. If a given object is
#     not allocated on a GPU, this is a no-op.

#     Arguments:
#         obj (Tensor or Storage): object allocated on the selected device.
#     """

#     def __init__(self, obj):
#         idx = obj.get_device() if vpex._C.is_vsi(obj) else -1
#         super(device_of, self).__init__(idx)