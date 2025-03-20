# from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch import Tensor

from typing import Any, Callable, List, Optional, Type, Union
# from PIL import Image
# import matplotlib.pyplot as plt

# import torchvision.transforms as transforms
# import torchvision.models as models

import copy
import numpy as np
import pandas as pd
import os
# import scipy.io as sio

# from torch.autograd import Variable
# from torchvision.transforms import ToTensor

from torch.utils.data import Dataset, DataLoader
# from torchvision import datasets
from pathlib import Path

class MyDataset(Dataset):
    def __init__(self, ydata_df, data_dir, device):#='./DNN_data/data/'
        # ydata_df = 
        # ydata_df = pd.read_csv(yfile_name, index_col=0)
        # x = xdata_df.values#.iloc[:,0:8]
        
        self.device = device
        
        self.gene = ydata_df.iloc[:,0].values
        target_y = ydata_df.iloc[:,1:].values
        
        # self.x_train = torch.tensor(x, dtype=torch.float32)
        self.y_train = torch.tensor(target_y, dtype=torch.float32)
        self.y_train = self.y_train.to(self.device)
        self.data_dir = data_dir
 
    def __len__(self):
        return(len(self.gene))
   
    def __getitem__(self, idx):
        slice_path = os.path.join(self.data_dir, self.gene[idx] + '.npy')
        slice_in = np.load(slice_path)
        
        self.x_train = torch.tensor(slice_in)
        self.x_train = self.x_train.to(self.device)
            
        return(self.x_train, self.y_train[idx])
    
## from pytorch
import sys
import re
import shutil
import tempfile
import hashlib
from urllib.request import urlopen, Request
from urllib.parse import urlparse
HASH_REGEX = re.compile(r'-([a-f0-9]*)\.')

class _Faketqdm(object):  # type: ignore[no-redef]

    def __init__(self, total=None, disable=False,
                 unit=None, *args, **kwargs):
        self.total = total
        self.disable = disable
        self.n = 0
        # Ignore all extra *args and **kwargs lest you want to reinvent tqdm

    def update(self, n):
        if self.disable:
            return

        self.n += n
        if self.total is None:
            sys.stderr.write("\r{0:.1f} bytes".format(self.n))
        else:
            sys.stderr.write("\r{0:.1f}%".format(100 * self.n / float(self.total)))
        sys.stderr.flush()

    def close(self):
        self.disable = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return

        sys.stderr.write('\n')

try:
    from tqdm import tqdm  # If tqdm is installed use it, otherwise use the fake wrapper
except ImportError:
    tqdm = _Faketqdm

def download_url_to_file(url, file_name, hash_prefix=None, progress=True):
    r"""Download object at the given URL to a local path.
    Args:
        url (str): URL of the object to download
        dst (str): Full path where object will be saved, e.g. ``/tmp/temporary_file``
        hash_prefix (str, optional): If not None, the SHA256 downloaded file should start with ``hash_prefix``.
            Default: None
        progress (bool, optional): whether or not to display a progress bar to stderr
            Default: True
    Example:
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_HUB)
        >>> # xdoctest: +REQUIRES(POSIX)
        >>> torch.hub.download_url_to_file('https://s3.amazonaws.com/pytorch/models/resnet18-5c106cde.pth', '/tmp/temporary_file')
    """
    file_size = None
    req = Request(url, headers={"User-Agent": "torch.hub"})
    u = urlopen(req)
    meta = u.info()
    if hasattr(meta, 'getheaders'):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    # We deliberately save it in a temp file and move it after
    # download is complete. This prevents a local working checkpoint
    # being overridden by a broken download.
    
    dst_dir = os.path.dirname(__file__)
    dst = os.path.expanduser(os.path.join(dst_dir, file_name))
    f = tempfile.NamedTemporaryFile(delete=False, dir=dst_dir)

    try:
        if hash_prefix is not None:
            sha256 = hashlib.sha256()
        with tqdm(total=file_size, disable=not progress,
                  unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                if hash_prefix is not None:
                    sha256.update(buffer)
                pbar.update(len(buffer))

        f.close()
        if hash_prefix is not None:
            digest = sha256.hexdigest()
            if digest[:len(hash_prefix)] != hash_prefix:
                raise RuntimeError('invalid hash value (expected "{}", got "{}")'
                                   .format(hash_prefix, digest))
        shutil.move(f.name, dst)
    finally:
        f.close()
        if os.path.exists(f.name):
            os.remove(f.name)

def conv3x3(in_planes: int, out_planes: int, stride: int = 1, groups: int = 1, dilation: int = 1) -> nn.Conv2d:
    """3x3 convolution with padding"""
    return nn.Conv2d(
        in_planes,
        out_planes,
        kernel_size=3,
        stride=stride,
        padding=dilation,
        groups=groups,
        bias=False,
        dilation=dilation,
    )


def conv1x1(in_planes: int, out_planes: int, stride: int = 1) -> nn.Conv2d:
    """1x1 convolution"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)

class BasicBlock(nn.Module):
    expansion: int = 1

    def __init__(
        self,
        inplanes: int,
        planes: int,
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
        groups: int = 1,
        base_width: int = 64,
        dilation: int = 1,
        norm_layer: Optional[Callable[..., nn.Module]] = None,
    ) -> None:
        super().__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        if groups != 1 or base_width != 64:
            raise ValueError("BasicBlock only supports groups=1 and base_width=64")
        if dilation > 1:
            raise NotImplementedError("Dilation > 1 not supported in BasicBlock")
        # Both self.conv1 and self.downsample layers downsample the input when stride != 1
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = norm_layer(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = norm_layer(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x: Tensor) -> Tensor:
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out

class Bottleneck(nn.Module):
    # Bottleneck in torchvision places the stride for downsampling at 3x3 convolution(self.conv2)
    # while original implementation places the stride at the first 1x1 convolution(self.conv1)
    # according to "Deep residual learning for image recognition" https://arxiv.org/abs/1512.03385.
    # This variant is also known as ResNet V1.5 and improves accuracy according to
    # https://ngc.nvidia.com/catalog/model-scripts/nvidia:resnet_50_v1_5_for_pytorch.

    expansion: int = 4

    def __init__(
        self,
        inplanes: int,
        planes: int,
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
        groups: int = 1,
        base_width: int = 64,
        dilation: int = 1,
        norm_layer: Optional[Callable[..., nn.Module]] = None,
    ) -> None:
        super().__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        width = int(planes * (base_width / 64.0)) * groups
        # Both self.conv2 and self.downsample layers downsample the input when stride != 1
        self.conv1 = conv1x1(inplanes, width)
        self.bn1 = norm_layer(width)
        self.conv2 = conv3x3(width, width, stride, groups, dilation)
        self.bn2 = norm_layer(width)
        self.conv3 = conv1x1(width, planes * self.expansion)
        self.bn3 = norm_layer(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x: Tensor) -> Tensor:
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):
    def __init__(
        self,
        block: Type[Union[BasicBlock, Bottleneck]],
        layers: List[int],
        num_classes: int = 1000,
        zero_init_residual: bool = False,
        groups: int = 1,
        width_per_group: int = 64,
        replace_stride_with_dilation: Optional[List[bool]] = None,
        norm_layer: Optional[Callable[..., nn.Module]] = None,
    ) -> None:
        super().__init__()
        #_log_api_usage_once(self)
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self._norm_layer = norm_layer

        self.inplanes = 64
        self.dilation = 1
        if replace_stride_with_dilation is None:
            # each element in the tuple indicates if we should replace
            # the 2x2 stride with a dilated convolution instead
            replace_stride_with_dilation = [False, False, False]
        if len(replace_stride_with_dilation) != 3:
            raise ValueError(
                "replace_stride_with_dilation should be None "
                f"or a 3-element tuple, got {replace_stride_with_dilation}"
            )
        self.groups = groups
        self.base_width = width_per_group
        self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = norm_layer(self.inplanes)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2, dilate=replace_stride_with_dilation[0])
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2, dilate=replace_stride_with_dilation[1])
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2, dilate=replace_stride_with_dilation[2])
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        # Zero-initialize the last BN in each residual branch,
        # so that the residual branch starts with zeros, and each residual block behaves like an identity.
        # This improves the model by 0.2~0.3% according to https://arxiv.org/abs/1706.02677
        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, Bottleneck) and m.bn3.weight is not None:
                    nn.init.constant_(m.bn3.weight, 0)  # type: ignore[arg-type]
                elif isinstance(m, BasicBlock) and m.bn2.weight is not None:
                    nn.init.constant_(m.bn2.weight, 0)  # type: ignore[arg-type]

    def _make_layer(
        self,
        block: Type[Union[BasicBlock, Bottleneck]],
        planes: int,
        blocks: int,
        stride: int = 1,
        dilate: bool = False,
    ) -> nn.Sequential:
        norm_layer = self._norm_layer
        downsample = None
        previous_dilation = self.dilation
        if dilate:
            self.dilation *= stride
            stride = 1
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                conv1x1(self.inplanes, planes * block.expansion, stride),
                norm_layer(planes * block.expansion),
            )

        layers = []
        layers.append(
            block(
                self.inplanes, planes, stride, downsample, self.groups, self.base_width, previous_dilation, norm_layer
            )
        )
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(
                block(
                    self.inplanes,
                    planes,
                    groups=self.groups,
                    base_width=self.base_width,
                    dilation=self.dilation,
                    norm_layer=norm_layer,
                )
            )

        return nn.Sequential(*layers)

    def _forward_impl(self, x: Tensor) -> Tensor:
        # See note [TorchScript super()]
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x

    def forward(self, x: Tensor) -> Tensor:
        return self._forward_impl(x)


class NbcNet(ResNet):#()models.ResNet
    def __init__(self, para):
        super(NbcNet, self).__init__(block = BasicBlock, layers = [3, 4, 6, 3])

        filePath = Path(__file__).parent / 'resnet34-b627a593.pth'
        if filePath.is_file():
#             model_resnet34 = models.resnet34()
#             model_resnet34.load_state_dict(torch.load('./data/resnet34-b627a593.pth'))
            pass
        else:
            download_url_to_file(url='https://download.pytorch.org/models/resnet34-b627a593.pth',file_name='resnet34-b627a593.pth', progress=True)

        self.load_state_dict(torch.load(filePath))

        self.avgpool = nn.AvgPool2d((3, 3))
        self.AdaptiveAvgPool2d = nn.AdaptiveAvgPool2d((1, 1))
        #10 10 10
        #20 18 17
        a, b, c = para
        self.layer5= nn.Sequential(
            nn.ConvTranspose2d(in_channels = 512, out_channels = 128, kernel_size=a,  padding=0, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.layer6= nn.Sequential(
            nn.ConvTranspose2d(in_channels = 128, out_channels = 16, kernel_size=b, stride = 2, padding=0, bias=False),
            nn.BatchNorm2d(16),#21
            nn.ReLU(inplace=True)
        )
        
        self.layer7= nn.Sequential(
            nn.ConvTranspose2d(16, 1, kernel_size=c, stride = 2, bias=False),
            nn.ReLU()
        )
        
        
        in_channels=3
        self.conv_first = nn.Conv2d(in_channels, out_channels=64, kernel_size=3, stride=2, padding=3, bias=False)
        
            
    def forward(self,x):
        
        x = self.conv_first(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.AdaptiveAvgPool2d(x)
        x = self.layer5(x)#avgpool(x)
        x = self.layer6(x)
        x = self.layer7(x)
        
        return(x)


def train_loop(dataloader, model, loss_fn, optimizer, mask64, device, y_flag, mask_y=None):
    size = len(dataloader.dataset)
    rloss = 0
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        X = X.float()
#         print(X.shape)
        pred = model(X)
        
        pred = pred[:, :, mask64]#torch.squeeze(pred)[mask64]#torch.flatten(torch.mul(model(X), ))
        pred = torch.squeeze(pred)
        
        y = y.float()
        if y_flag == 0:
            y = y[:, torch.flatten(mask_y)]
        
        # print(pred.shape, y.shape)
        
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            # print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
            rloss = loss
    return(rloss)


def test_loop(dataloader, model, loss_fn, mask64, device, y_flag, mask_y=None):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            X = X.float()
            y = y.float()
            
            pred = model(X)
            pred = pred[:,:,mask64]##torch.mul(, mask)
            pred = torch.squeeze(pred)
                    
            y = y.float()
            if y_flag == 0:
                y = y[:, torch.flatten(mask_y)]
            
            test_loss += loss_fn(pred, y).item()
#             correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
#     correct /= size
    # print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
    return(test_loss)


def generate_input(protein_table_i, index_x, index_y):
    # df_out_i = run_data.iloc[gene, 2:]
    # assess = str(run_data.iloc[gene, 0]) + '_' + str(run_data.iloc[gene, 1]) + '_norm'
    half_tmpX = np.array(protein_table_i[index_x[0]:index_x[1]])#[::-1]#[::2]#
    half_tmpY = np.array(protein_table_i[index_y[0]:index_y[1]])#[::-1]#[::2]#
    
    
    half_tmpXY_mean = (1e-5+np.mean(np.concatenate([half_tmpX, half_tmpY]))/500)
    half_tmpX /= half_tmpXY_mean
    half_tmpY /= half_tmpXY_mean

    Xrep = np.tile(np.array(half_tmpX)[:,np.newaxis], int(len(half_tmpY)))
    Yrep = np.array([half_tmpY] * int(len(half_tmpX)))
    XYrep = Xrep + Yrep

    input_XYrep = np.float32(np.stack((Xrep, Yrep, XYrep), axis=0))
    
    return(input_XYrep, half_tmpXY_mean)
    
    
def generate_val_distribution(model, C3C5_input, index_x, index_y, mask64, device):
    input_XYrep, half_tmpXY_mean = generate_input(C3C5_input, index_x, index_y)
    input_XYrep_tensor = torch.tensor(input_XYrep)
    input_XYrep_tensor = input_XYrep_tensor.to(device)
    
    # print(input_XYrep.shape)
    a,b,c = input_XYrep_tensor.size()
    # pred = model(input_XYrep_tensor.reshape(1, a,b,c))#
    
    pred = model(input_XYrep_tensor.reshape(1, a,b,c))#input_XYrep_tensor.shape()
    pred = pred[:, :, mask64]
    # pred = torch.squeeze(pred)
    # pred[:,:,mask64 == False] = np.nan
    
    tmp_return = pred.squeeze().detach().cpu().numpy() * half_tmpXY_mean #[10:60, 8:82]
    return(tmp_return)
    
def denoise_mean(input_dat, FDesign0_len, lens=5):
    channel_intensity_list_dat_dropna_impute = input_dat.copy()
    
    for i in range(2, (2+int((FDesign0_len-1)/2) + 1)):
        
        tmp_i = 1
        tmp = channel_intensity_list_dat_dropna_impute.iloc[:,i]

        if (lens>=3) and (i >= 3): 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i-1] 

        if (lens>=3) and (i < (2+int((FDesign0_len-1)/2)) ): 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i+1] 

        if (lens>=5) and (i > 3) : 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i-2]

        if (lens>=5) and (i < (1+int((FDesign0_len-1)/2)) ):
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i+2]
        
        if (lens>=7) and (i > 4) : 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i-3]

        if (lens>=7) and (i < (0+int((FDesign0_len-1)/2)) ):
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i+3]
            
        channel_intensity_list_dat_dropna_impute.iloc[:,i] = tmp / tmp_i
    
    for i in range((2+int((FDesign0_len-1)/2) + 1), channel_intensity_list_dat_dropna_impute.shape[1]):

        tmp_i = 1
        tmp = channel_intensity_list_dat_dropna_impute.iloc[:,i]

        if (lens>=3) and (i >= 3+int((FDesign0_len-1)/2) + 1): 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i-1] 

        if (lens>=3) and (i < (channel_intensity_list_dat_dropna_impute.shape[1] - 1) ): 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i+1] 

        if (lens>=5) and (i > 3+int((FDesign0_len-1)/2) + 1) : 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i-2]

        if (lens>=5) and (i < (channel_intensity_list_dat_dropna_impute.shape[1] - 2) ):
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i+2]

        if (lens>=7) and (i > 4) : 
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i-3]

        if (lens>=7) and (i < (0+int((FDesign0_len-1)/2)) ):
            tmp_i += 1
            tmp += channel_intensity_list_dat_dropna_impute.iloc[:,i+3]
            
        channel_intensity_list_dat_dropna_impute.iloc[:,i] = tmp / tmp_i
    
    return(channel_intensity_list_dat_dropna_impute)