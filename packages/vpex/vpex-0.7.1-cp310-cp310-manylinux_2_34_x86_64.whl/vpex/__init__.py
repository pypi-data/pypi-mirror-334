import vpex.vtal
import vpex.tc
import torch
import vpex._C

torch._register_device_module('vsi', vpex.vtal)