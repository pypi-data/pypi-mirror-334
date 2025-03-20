# RSProduction MachineLearning

This project provides some usefull machine learning functionality.

# Table of Contents

- [1 dataset](#1-dataset)
  - [1.1 HMDB51 : torch.utils.data.dataset.Dataset](#11-hmdb51--torchutilsdatadatasetdataset)
    - [1.1.1 \_\_init\_\_](#111-\_\_init\_\_)
  - [1.2 Kinetics : torch.utils.data.dataset.Dataset](#12-kinetics--torchutilsdatadatasetdataset)
    - [1.2.1 \_\_init\_\_](#121-\_\_init\_\_)
  - [1.3 TUCRID : torch.utils.data.dataset.Dataset](#13-tucrid--torchutilsdatadatasetdataset)
    - [1.3.1 \_\_init\_\_](#131-\_\_init\_\_)
    - [1.3.2 get\_uniform\_sampler](#132-get\_uniform\_sampler)
    - [1.3.3 load\_backgrounds](#133-load\_backgrounds)
  - [1.4 UCF101 : torch.utils.data.dataset.Dataset](#14-ucf101--torchutilsdatadatasetdataset)
    - [1.4.1 \_\_init\_\_](#141-\_\_init\_\_)
- [2 metrics](#2-metrics)
  - [2.1 AUROC](#21-auroc)
  - [2.2 F1\_Score](#22-f1\_score)
  - [2.3 FN](#23-fn)
  - [2.4 FP](#24-fp)
  - [2.5 FPR](#25-fpr)
  - [2.6 ROC](#26-roc)
  - [2.7 TN](#27-tn)
  - [2.8 TP](#28-tp)
  - [2.9 TPR](#29-tpr)
  - [2.10 confusion\_matrix](#210-confusion\_matrix)
  - [2.11 plot\_ROC](#211-plot\_roc)
  - [2.12 plot\_confusion\_matrix](#212-plot\_confusion\_matrix)
  - [2.13 precision](#213-precision)
  - [2.14 recall](#214-recall)
  - [2.15 top\_10\_accuracy](#215-top\_10\_accuracy)
  - [2.16 top\_1\_accuracy](#216-top\_1\_accuracy)
  - [2.17 top\_2\_accuracy](#217-top\_2\_accuracy)
  - [2.18 top\_3\_accuracy](#218-top\_3\_accuracy)
  - [2.19 top\_5\_accuracy](#219-top\_5\_accuracy)
  - [2.20 top\_k\_accuracy](#220-top\_k\_accuracy)
- [3 model](#3-model)
  - [3.1 MODELS : enum.Enum](#31-models--enumenum)
  - [3.2 WEIGHTS : enum.Enum](#32-weights--enumenum)
  - [3.3 list\_model\_weights](#33-list\_model\_weights)
  - [3.4 load\_model](#34-load\_model)
  - [3.5 publish\_model](#35-publish\_model)
- [4 multi\_transforms](#4-multi\_transforms)
  - [4.1 BGR2GRAY : MultiTransform](#41-bgr2gray--multitransform)
    - [4.1.1 \_\_call\_\_](#411-\_\_call\_\_)
    - [4.1.2 \_\_init\_\_](#412-\_\_init\_\_)
  - [4.2 BGR2RGB : MultiTransform](#42-bgr2rgb--multitransform)
    - [4.2.1 \_\_call\_\_](#421-\_\_call\_\_)
    - [4.2.2 \_\_init\_\_](#422-\_\_init\_\_)
  - [4.3 Brightness : MultiTransform](#43-brightness--multitransform)
    - [4.3.1 \_\_call\_\_](#431-\_\_call\_\_)
    - [4.3.2 \_\_init\_\_](#432-\_\_init\_\_)
  - [4.4 CenterCrop : MultiTransform](#44-centercrop--multitransform)
    - [4.4.1 \_\_call\_\_](#441-\_\_call\_\_)
    - [4.4.2 \_\_init\_\_](#442-\_\_init\_\_)
  - [4.5 Color : MultiTransform](#45-color--multitransform)
    - [4.5.1 \_\_call\_\_](#451-\_\_call\_\_)
    - [4.5.2 \_\_init\_\_](#452-\_\_init\_\_)
  - [4.6 Compose : builtins.object](#46-compose--builtinsobject)
    - [4.6.1 \_\_call\_\_](#461-\_\_call\_\_)
    - [4.6.2 \_\_init\_\_](#462-\_\_init\_\_)
  - [4.7 GaussianNoise : MultiTransform](#47-gaussiannoise--multitransform)
    - [4.7.1 \_\_call\_\_](#471-\_\_call\_\_)
    - [4.7.2 \_\_init\_\_](#472-\_\_init\_\_)
  - [4.8 MultiTransform : builtins.object](#48-multitransform--builtinsobject)
    - [4.8.1 \_\_call\_\_](#481-\_\_call\_\_)
    - [4.8.2 \_\_init\_\_](#482-\_\_init\_\_)
  - [4.9 Normalize : MultiTransform](#49-normalize--multitransform)
    - [4.9.1 \_\_call\_\_](#491-\_\_call\_\_)
    - [4.9.2 \_\_init\_\_](#492-\_\_init\_\_)
  - [4.10 RGB2BGR : BGR2RGB](#410-rgb2bgr--bgr2rgb)
    - [4.10.1 \_\_call\_\_](#4101-\_\_call\_\_)
    - [4.10.2 \_\_init\_\_](#4102-\_\_init\_\_)
  - [4.11 RandomCrop : MultiTransform](#411-randomcrop--multitransform)
    - [4.11.1 \_\_call\_\_](#4111-\_\_call\_\_)
    - [4.11.2 \_\_init\_\_](#4112-\_\_init\_\_)
  - [4.12 RandomHorizontalFlip : MultiTransform](#412-randomhorizontalflip--multitransform)
    - [4.12.1 \_\_call\_\_](#4121-\_\_call\_\_)
    - [4.12.2 \_\_init\_\_](#4122-\_\_init\_\_)
  - [4.13 RandomVerticalFlip : MultiTransform](#413-randomverticalflip--multitransform)
    - [4.13.1 \_\_call\_\_](#4131-\_\_call\_\_)
    - [4.13.2 \_\_init\_\_](#4132-\_\_init\_\_)
  - [4.14 ReplaceBackground : MultiTransform](#414-replacebackground--multitransform)
    - [4.14.1 \_\_call\_\_](#4141-\_\_call\_\_)
    - [4.14.2 \_\_init\_\_](#4142-\_\_init\_\_)
  - [4.15 Resize : MultiTransform](#415-resize--multitransform)
    - [4.15.1 \_\_call\_\_](#4151-\_\_call\_\_)
    - [4.15.2 \_\_init\_\_](#4152-\_\_init\_\_)
  - [4.16 Rotate : MultiTransform](#416-rotate--multitransform)
    - [4.16.1 \_\_call\_\_](#4161-\_\_call\_\_)
    - [4.16.2 \_\_init\_\_](#4162-\_\_init\_\_)
  - [4.17 Satturation : MultiTransform](#417-satturation--multitransform)
    - [4.17.1 \_\_call\_\_](#4171-\_\_call\_\_)
    - [4.17.2 \_\_init\_\_](#4172-\_\_init\_\_)
  - [4.18 Scale : MultiTransform](#418-scale--multitransform)
    - [4.18.1 \_\_call\_\_](#4181-\_\_call\_\_)
    - [4.18.2 \_\_init\_\_](#4182-\_\_init\_\_)
  - [4.19 Stack : MultiTransform](#419-stack--multitransform)
    - [4.19.1 \_\_call\_\_](#4191-\_\_call\_\_)
    - [4.19.2 \_\_init\_\_](#4192-\_\_init\_\_)
  - [4.20 ToCVImage : MultiTransform](#420-tocvimage--multitransform)
    - [4.20.1 \_\_call\_\_](#4201-\_\_call\_\_)
    - [4.20.2 \_\_init\_\_](#4202-\_\_init\_\_)
  - [4.21 ToNumpy : MultiTransform](#421-tonumpy--multitransform)
    - [4.21.1 \_\_call\_\_](#4211-\_\_call\_\_)
    - [4.21.2 \_\_init\_\_](#4212-\_\_init\_\_)
  - [4.22 ToPILImage : MultiTransform](#422-topilimage--multitransform)
    - [4.22.1 \_\_call\_\_](#4221-\_\_call\_\_)
    - [4.22.2 \_\_init\_\_](#4222-\_\_init\_\_)
  - [4.23 ToTensor : MultiTransform](#423-totensor--multitransform)
    - [4.23.1 \_\_call\_\_](#4231-\_\_call\_\_)
    - [4.23.2 \_\_init\_\_](#4232-\_\_init\_\_)
- [5 run](#5-run)
  - [5.1 Run : builtins.object](#51-run--builtinsobject)
    - [5.1.1 \_\_init\_\_](#511-\_\_init\_\_)
    - [5.1.2 append](#512-append)
    - [5.1.3 get\_avg](#513-get\_avg)
    - [5.1.4 get\_val](#514-get\_val)
    - [5.1.5 len](#515-len)
    - [5.1.6 load\_best\_state\_dict](#516-load\_best\_state\_dict)
    - [5.1.7 load\_state\_dict](#517-load\_state\_dict)
    - [5.1.8 pickle\_dump](#518-pickle\_dump)
    - [5.1.9 pickle\_load](#519-pickle\_load)
    - [5.1.10 plot](#5110-plot)
    - [5.1.11 recalculate\_moving\_average](#5111-recalculate\_moving\_average)
    - [5.1.12 save](#5112-save)
    - [5.1.13 save\_best\_state\_dict](#5113-save\_best\_state\_dict)
    - [5.1.14 save\_state\_dict](#5114-save\_state\_dict)
    - [5.1.15 train\_epoch](#5115-train\_epoch)
    - [5.1.16 validate\_epoch](#5116-validate\_epoch)




# 1 dataset

[TOC](#table-of-contents)



## 1.1 HMDB51 : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for HMDB51.

**Example**

```python
from rsp.ml.dataset import HMDB51
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

transforms = multi_transforms.Compose([
    multi_transforms.Color(1.5, p=0.5),
    multi_transforms.Stack()
])
ds = HMDB51('train', fold=1, transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.1.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| split | str | Dataset split [train|val|test] |
| fold | int | Fold number. The dataset is split into 3 folds. If fold is None, all folds will be loaded. |
| cache_dir | str, default = None | Directory to store the downloaded files. If set to `None`, the default cache directory will be used |
| force_reload | bool, default = False | If set to `True`, the dataset will be reloaded |
| target_size | (int, int), default = (400, 400) | Size of the frames. The frames will be resized to this size. |
| sequence_length | int, default = 30 | Length of the sequences |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
| verbose | bool, default = False | If set to `True`, the progress will be printed. |
## 1.2 Kinetics : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for the Kinetics dataset.

**Example**

```python
from rsp.ml.dataset import Kinetics

ds = Kinetics(split='train', type=400)

for X, T in ds:
    print(X)
```
### 1.2.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| split | str | Dataset split [train|val] |
| type | int, default = 400 | Type of the kineticts dataset. Currently only 400 is supported. |
| frame_size | (int, int), default = (400, 400) | Size of the frames. The frames will be resized to this size. |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
| cache_dir | str, default = None | Directory to store the downloaded files. If set to `None`, the default cache directory will be used |
| num_threads | int, default = 0 | Number of threads to use for downloading the files. |
## 1.3 TUCRID : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

Dataset class for the Robot Interaction Dataset by University of Technology Chemnitz (TUCRID).

**Example**

```python
from rsp.ml.dataset import TUCRID
from rsp.ml.dataset import ReplaceBackgroundRGBD
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

backgrounds = TUCRID.load_backgrounds_color()
transforms = multi_transforms.Compose([
    ReplaceBackgroundRGBD(backgrounds),
    multi_transforms.Stack()
])

ds = TUCRID('train', transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.3.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| phase | str | Dataset phase [train|val] |
| load_depth_data | bool, default = True | Load depth data |
| sequence_length | int, default = 30 | Length of the sequences |
| num_classes | int, default = 10 | Number of classes |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
### 1.3.2 get\_uniform\_sampler

[TOC](#table-of-contents)

### 1.3.3 load\_backgrounds

[TOC](#table-of-contents)

**Description**

Loads the background images.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| load_depth_data | bool, default = True | If set to `True`, the depth images will be loaded as well. |
## 1.4 UCF101 : torch.utils.data.dataset.Dataset

[TOC](#table-of-contents)

**Description**

An abstract class representing a :class:`Dataset`.

All datasets that represent a map from keys to data samples should subclass
it. All subclasses should overwrite :meth:`__getitem__`, supporting fetching a
data sample for a given key. Subclasses could also optionally overwrite
:meth:`__len__`, which is expected to return the size of the dataset by many
:class:`~torch.utils.data.Sampler` implementations and the default options
of :class:`~torch.utils.data.DataLoader`. Subclasses could also
optionally implement :meth:`__getitems__`, for speedup batched samples
loading. This method accepts list of indices of samples of batch and returns
list of samples.

.. note::
  :class:`~torch.utils.data.DataLoader` by default constructs an index
  sampler that yields integral indices.  To make it work with a map-style
  dataset with non-integral indices/keys, a custom sampler must be provided.

**Example**

```python
from rsp.ml.dataset import UCF101
import rsp.ml.multi_transforms as multi_transforms
import cv2 as cv

transforms = multi_transforms.Compose([
    multi_transforms.Color(1.5, p=0.5),
    multi_transforms.Stack()
])
ds = UCF101('train', fold=1, transforms=transforms)

for X, T in ds:
  for x in X.permute(0, 2, 3, 1):
    img_color = x[:, :, :3].numpy()
    img_depth = x[:, :, 3].numpy()

    cv.imshow('color', img_color)
    cv.imshow('depth', img_depth)

    cv.waitKey(30)
```
### 1.4.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| split | str | Dataset split [train|val|test] |
| fold | int | Fold number. The dataset is split into 3 folds. If fold is None, all folds will be loaded. |
| cache_dir | str, default = None | Directory to store the downloaded files. If set to `None`, the default cache directory will be used |
| force_reload | bool, default = False | If set to `True`, the dataset will be reloaded |
| target_size | (int, int), default = (400, 400) | Size of the frames. The frames will be resized to this size. |
| sequence_length | int, default = 30 | Length of the sequences |
| transforms | rsp.ml.multi_transforms.Compose = default = rsp.ml.multi_transforms.Compose([]) | Transformations, that will be applied to each input sequence. See documentation of `rsp.ml.multi_transforms` for more details. |
| verbose | bool, default = False | If set to `True`, the progress will be printed. |
# 2 metrics

[TOC](#table-of-contents)

The module `rsp.ml.metrics` provides some functionality to quantify the quality of predictions.

## 2.1 AUROC

[TOC](#table-of-contents)

**Description**

Calculates the Area under the Receiver Operation Chracteristic Curve.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| num_thresholds | int, default = 100 | Number of thresholds to compute. |

**Returns**

Receiver Operation Chracteristic Area under the Curve : float

## 2.2 F1\_Score

[TOC](#table-of-contents)

**Description**

F1 Score. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

F1 Score : float

**Equations**

$precision = \frac{TP}{TP + FP}$

$recall = \frac{TP}{TP + FN}$

$F_1 = \frac{2 \cdot precision \cdot recall}{precision + recall} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$



**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

f1score = m.F1_Score(Y, T)

print(f1score) --> 0.5
```

## 2.3 FN

[TOC](#table-of-contents)

**Description**

False negatives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

False negatives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fn = m.FN(Y, T)
print(fn) -> 1
```

## 2.4 FP

[TOC](#table-of-contents)

**Description**

False positives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

False positives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fp = m.FP(Y, T)
print(fp) -> 1
```

## 2.5 FPR

[TOC](#table-of-contents)

**Description**

False positive rate. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

False positive rate : float

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fpr = m.FPR(Y, T)
print(fpr) -> 0.08333333333333333
```

## 2.6 ROC

[TOC](#table-of-contents)

**Description**

Calculates the receiver operating characteristic: computes False Positive Rates and True positive Rates for `num_thresholds` aligned between 0 and 1

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| num_thresholds | int, default = 100 | Number of thresholds to compute. |

**Returns**

(False Positive Rates, True Positive Rates) for 100 different thresholds : (List[float], List[float])

**Example**

```python
import rsp.ml.metrics as m
import torch
import torch.nn.functional as F

num_elements = 100000
num_classes = 7

T = []
for i in range(num_elements):
  true_class = torch.randint(0, num_classes, (1,))
  t = F.one_hot(true_class, num_classes=num_classes)
  T.append(t)
T = torch.cat(T)

dist = torch.normal(T.float(), 1.5)
Y = F.softmax(dist, dim = 1)
FPRs, TPRs = m.ROC(Y, T)
```

## 2.7 TN

[TOC](#table-of-contents)

**Description**

True negatives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

True negatives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tn = m.TN(Y, T)
print(tn) -> 11
```

## 2.8 TP

[TOC](#table-of-contents)

**Description**

True positives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

True positives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tp = m.TP(Y, T)
print(tp) -> 5
```

## 2.9 TPR

[TOC](#table-of-contents)

**Description**

True positive rate. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

True positive rate : float

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tpr = m.TPR(Y, T)
print(tpr) -> 0.8333333333333334
```

## 2.10 confusion\_matrix

[TOC](#table-of-contents)

**Description**

Calculates the confusion matrix. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Confusion matrix : torch.Tensor

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

conf_mat = m.confusion_matrix(Y, T)
print(conf_mat) -> tensor([
  [1, 1, 0],
  [0, 2, 0],
  [0, 0, 2]
])
```

## 2.11 plot\_ROC

[TOC](#table-of-contents)

**Description**

Plot the receiver operating characteristic.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| num_thresholds | int, default = 100 | Number of thresholds to compute. |
| title | str, optional, default = 'Confusion Matrix' | Title of the plot |
| class_curves | bool, default = False | Plot ROC curve for each class |
| labels | str, optional, default = None | Class labels -> automatic labeling C000, ..., CXXX if labels is None |
| plt_show | bool, optional, default = False | Set to True to show the plot |
| save_file_name | str, optional, default = None | If not None, the plot is saved under the specified save_file_name. |

**Returns**

Image of the confusion matrix : np.array

![](documentation/image/ROC_AUC.jpg)
## 2.12 plot\_confusion\_matrix

[TOC](#table-of-contents)

**Description**

Plot the confusion matrix

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| confusion_matrix | torch.Tensor | Confusion matrix |
| labels | str, optional, default = None | Class labels -> automatic labeling C000, ..., CXXX if labels is None |
| cmap | str, optional, default = 'Blues' | Seaborn cmap, see https://r02b.github.io/seaborn_palettes/ |
| xlabel | str, optional, default = 'Predicted label' | X-Axis label |
| ylabel | str, optional, default = 'True label' | Y-Axis label |
| title | str, optional, default = 'Confusion Matrix' | Title of the plot |
| plt_show | bool, optional, default = False | Set to True to show the plot |
| save_file_name | str, optional, default = None | If not None, the plot is saved under the specified save_file_name. |

**Returns**

Image of the confusion matrix : np.array

![](documentation/image/confusion_matrix.jpg)
## 2.13 precision

[TOC](#table-of-contents)

**Description**

Precision. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

Precision : float

**Equations**

$precision = \frac{TP}{TP + FP}$



**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

precision = m.precision(Y, T)
print(precision) -> 0.8333333333333334
```

## 2.14 recall

[TOC](#table-of-contents)

**Description**

Recall. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |
| threshold | float | All values that are greater than or equal to the threshold are considered a positive class. |

**Returns**

Recall : float

**Equations**

$recall = \frac{TP}{TP + FN}$



**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

recall = m.recall(Y, T)
print(recall) -> 0.8333333333333334
```

## 2.15 top\_10\_accuracy

[TOC](#table-of-contents)

**Description**

Top 10 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 10 accuracy -> top k accuracy | k = 10 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_10_accuracy = m.top_10_accuracy(Y, T, k = 3)

print(top_10_accuracy) --> 1.0
```

## 2.16 top\_1\_accuracy

[TOC](#table-of-contents)

**Description**

Top 1 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 1 accuracy -> top k accuracy | k = 1 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_1_accuracy = m.top_1_accuracy(Y, T, k = 3)

print(top_1_accuracy) --> 0.8333333333333334
```

## 2.17 top\_2\_accuracy

[TOC](#table-of-contents)

**Description**

Top 2 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 2 accuracy -> top k accuracy | k = 2 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_2_accuracy = m.top_2_accuracy(Y, T, k = 3)

print(top_2_accuracy) --> 1.0
```

## 2.18 top\_3\_accuracy

[TOC](#table-of-contents)

**Description**

Top 3 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 3 accuracy -> top k accuracy | k = 3 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_3_accuracy = m.top_3_accuracy(Y, T, k = 3)

print(top_3_accuracy) --> 1.0
```

## 2.19 top\_5\_accuracy

[TOC](#table-of-contents)

**Description**

Top 5 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 5 accuracy -> top k accuracy | k = 5 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_5_accuracy = m.top_5_accuracy(Y, T, k = 3)

print(top_5_accuracy) --> 1.0
```

## 2.20 top\_k\_accuracy

[TOC](#table-of-contents)

**Description**

Top k accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top k accuracy : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_k_accuracy = m.top_k_accuracy(Y, T, k = 3)

print(top_k_accuracy) --> 1.0
```

# 3 model

[TOC](#table-of-contents)

The module `rsp.ml.model` provides some usefull functionality to store and load pytorch models.

## 3.1 MODELS : enum.Enum

[TOC](#table-of-contents)

**Description**

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

>>> Color.RED
<Color.RED: 1>

- value lookup:

>>> Color(1)
<Color.RED: 1>

- name lookup:

>>> Color['RED']
<Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.


## 3.2 WEIGHTS : enum.Enum

[TOC](#table-of-contents)

**Description**

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

>>> Color.RED
<Color.RED: 1>

- value lookup:

>>> Color(1)
<Color.RED: 1>

- name lookup:

>>> Color['RED']
<Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.


## 3.3 list\_model\_weights

[TOC](#table-of-contents)

**Description**

Lists all available weight files.


**Returns**

List of (MODEL:str, WEIGHT:str) : List[Tuple(str, str)]

**Example**

```python
import rsp.ml.model as model

model_weight_files = model.list_model_weights()
```

## 3.4 load\_model

[TOC](#table-of-contents)

**Description**

Loads a pretrained PyTorch model from HuggingFace.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | MODELS | ID of the model |
| weights | WEIGHTS | ID of the weights |

**Returns**

Pretrained PyTorch model : torch.nn.Module

**Example**

```python
import rsp.ml.model as model

action_recognition_model = model.load_model(MODEL.TUCARC3D, WEIGHTS.TUCAR)
```

## 3.5 publish\_model

[TOC](#table-of-contents)

# 4 multi\_transforms

[TOC](#table-of-contents)

The module `rsp.ml.multi_transforms` is based on `torchvision.transforms`, which is made for single images. `rsp.ml.multi_transforms` extends this functionality by providing transformations for sequences of images, which could be usefull for video augmentation.

## 4.1 BGR2GRAY : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a sequence of BGR images to grayscale images.


### 4.1.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.1.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.2 BGR2RGB : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts sequence of BGR images to RGB images.


### 4.2.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.2.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.3 Brightness : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.3.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.3.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.4 CenterCrop : MultiTransform

[TOC](#table-of-contents)

**Description**

Crops Images at the center after upscaling them. Dimensions kept the same.

![](documentation/image/multi_transforms.CenterCrop.png)


### 4.4.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.4.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| max_scale | float | Images are scaled randomly between 1. and max_scale before cropping to original size. |
## 4.5 Color : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.5.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.5.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.6 Compose : builtins.object

[TOC](#table-of-contents)

**Description**

Composes several MultiTransforms together.

**Example**

```python
import rsp.ml.multi_transforms as t

transforms = t.Compose([
  t.BGR2GRAY(),
  t.Scale(0.5)
])
```
### 4.6.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

### 4.6.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| children | List[MultiTransform] | List of MultiTransforms to compose. |
## 4.7 GaussianNoise : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.7.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.7.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.8 MultiTransform : builtins.object

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.8.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.8.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.9 Normalize : MultiTransform

[TOC](#table-of-contents)

**Description**

Normalize images with mean and standard deviation. Given mean: (mean[1],...,mean[n]) and std: (std[1],..,std[n]) for n channels, this transform will normalize each channel of the input torch.*Tensor i.e., output[channel] = (input[channel] - mean[channel]) / std[channel]

> Based on torchvision.transforms.Normalize


### 4.9.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.9.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| mean | List[float] | Sequence of means for each channel. |
| std | List[float] | Sequence of standard deviations for each channel. |
| inplace | bool | Set to True make this operation in-place. |
## 4.10 RGB2BGR : BGR2RGB

[TOC](#table-of-contents)

**Description**

Converts sequence of RGB images to BGR images.


### 4.10.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.10.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.11 RandomCrop : MultiTransform

[TOC](#table-of-contents)

**Description**

Crops Images at a random location after upscaling them. Dimensions kept the same.

![](documentation/image/multi_transforms.RandomCrop.png)


### 4.11.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.11.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| max_scale | float | Images are scaled randomly between 1. and max_scale before cropping to original size. |
## 4.12 RandomHorizontalFlip : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.12.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.12.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.13 RandomVerticalFlip : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.13.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.13.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.14 ReplaceBackground : MultiTransform

[TOC](#table-of-contents)

**Description**

Transformation for background replacement based on HSV values. Supports depth background replacement. backgrounds have to be passed as list of tuples of rgb and depth images.

**Example**

```python
from rsp.nl.dataset import TUCRID
import rsp.ml.multi_transforms as multi_transforms

USE_DEPTH_DATA = False
backgrounds = TUCRID.load_backgrounds(USE_DEPTH_DATA)
tranforms_train = multi_transforms.Compose([
    multi_transforms.ReplaceBackground(
        backgrounds = backgrounds,
        hsv_filter=[(69, 87, 139, 255, 52, 255)],
        p = 0.8
    ),
    multi_transforms.Stack()
])
tucrid = TUCRID('train', load_depth_data=USE_DEPTH_DATA, transforms=tranforms_train)

for X, T in tucrid:
    for x in X:
        img = x.permute(1, 2, 0).numpy()

        cv.imshow('img', img)
        cv.waitKey(30)
```
### 4.14.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.14.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Transformation for background replacement based on HSV values. Supports depth background replacement. backgrounds have to be passed as list of tuples of rgb and depth images.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| backgrounds | List[np.array] | List of background images |
| hsv_filter | List[tuple[int, int, int, int, int, int]] | List of HSV filters |
| p | float, default = 1. | Probability of applying the transformation |
| rotate | float, default = 5 | Maximum rotation angle |
| max_scale | float, default = 2 | Maximum scaling factor |
| max_noise | float, default = 0.002 | Maximum noise level |
## 4.15 Resize : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.15.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.15.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.16 Rotate : MultiTransform

[TOC](#table-of-contents)

**Description**

Randomly rotates images.

**Equations**

$angle = -max\_angle + 2 \cdot random() \cdot max\_angle$

![](documentation/image/multi_transforms.Rotate.png)


### 4.16.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.16.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Iitializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| max_angle | float | Maximal rotation in degrees | -max_angle <= rotate <= max_angle |
| auto_scale | bool, default = True | Image will be resized when auto scale is activated to avoid black margins. |
## 4.17 Satturation : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.17.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.17.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.18 Scale : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.18.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.18.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.19 Stack : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 4.19.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.19.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.20 ToCVImage : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a `torch.Tensor`to Open CV image by changing dimensions (d0, d1, d2) -> (d1, d2, d0) and converting `torch.Tensor` to `numpy`.


### 4.20.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.20.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.21 ToNumpy : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a `torch.Tensor`to `numpy`


### 4.21.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.21.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.22 ToPILImage : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts sequence of images to sequence of `PIL.Image`.


### 4.22.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.22.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 4.23 ToTensor : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a sequence of images to torch.Tensor.


### 4.23.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 4.23.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

# 5 run

[TOC](#table-of-contents)

The module `rsp.ml.run` provides some tools for storing, loading and visualizing data during training of models using PyTorch. 

## 5.1 Run : builtins.object

[TOC](#table-of-contents)

**Description**

Run class to store and manage training

**Example**

```python
from rsp.ml.run import Run
import rsp.ml.metrics as m

metrics = [
    m.top_1_accuracy
]
config = {
    m.top_1_accuracy.__name__: {
        'ymin': 0,
        'ymax': 1
    }
}
run = Run(id='run0001', metrics=metrics, config=config, ignore_outliers_in_chart_scaling=True)

for epoch in range(100):
    """here goes some training code, giving us inputs, predictions and targets"""
    acc = m.top_1_accuracy(predictions, targets)
    run.append(m.top_1_accuracy.__name__, 'train', acc)
```
### 5.1.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Run class to store and manage training

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| id | str, default = None | Id of the run. If None, a new id is generated |
| moving_average_epochs | int, default = 1 | Number of epochs to average over |
| metrics | list, default = None | List of metrics to compute. Each metric should be a function that takes Y and T as input. |
| device | str, default = None | torch device to run on |
| ignore_outliers_in_chart_scaling | bool, default = False | Ignore outliers when scaling charts |
| config | dict, default = {} | Configuration dictionary. Keys are metric names and values are dictionaries with keys 'ymin' and 'ymax' |
### 5.1.2 append

[TOC](#table-of-contents)

**Description**

Append value to key in phase.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| key | str | Key to append to |
| phase | str | Phase to append to |
| value | float | Value to append |
### 5.1.3 get\_avg

[TOC](#table-of-contents)

**Description**

Get last average value of key in phase

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| key | str | Key to get |
| phase | str | Phase to get from |

**Returns**

Last average value of key in phase : value : float

### 5.1.4 get\_val

[TOC](#table-of-contents)

**Description**

Get last value of key in phase

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| key | str | Key to get |
| phase | str | Phase to get from |

**Returns**

Last value of key in phase : value : float

### 5.1.5 len

[TOC](#table-of-contents)

**Description**

Get length of longest phase

### 5.1.6 load\_best\_state\_dict

[TOC](#table-of-contents)

**Description**

Load best state_dict from runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | torch.nn.Module | Model to load state_dict into |
| fname | str, default = 'state_dict.pt' | Filename to load from |
| verbose | bool, default = False | Print loaded file |
### 5.1.7 load\_state\_dict

[TOC](#table-of-contents)

**Description**

Load state_dict from runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | torch.nn.Module | Model to load state_dict into |
| fname | str, default = None | Filename to load from |
### 5.1.8 pickle\_dump

[TOC](#table-of-contents)

**Description**

Pickle model to runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model | torch.nn.Module | Model to pickle |
| fname | str, default = 'model.pkl' | Filename to save to |
### 5.1.9 pickle\_load

[TOC](#table-of-contents)

**Description**

Load model from runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| fname | str, default = 'model.pkl' | Filename to load from |
### 5.1.10 plot

[TOC](#table-of-contents)

**Description**

Plot all keys to runs/{id}/plot/{key}.jpg

### 5.1.11 recalculate\_moving\_average

[TOC](#table-of-contents)

**Description**

Recalculate moving average

### 5.1.12 save

[TOC](#table-of-contents)

**Description**

Save data to runs/{id}/data.json

### 5.1.13 save\_best\_state\_dict

[TOC](#table-of-contents)

**Description**

Save state_dict if new_acc is better than previous best

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| state_dict | dict | State dict to save |
| new_acc | float | New accuracy |
| epoch | int, default = None | Epoch to save |
| fname | str, default = 'state_dict.pt' | Filename to save to |
### 5.1.14 save\_state\_dict

[TOC](#table-of-contents)

**Description**

Save state_dict to runs/{id}/{fname}

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| state_dict | dict | State dict to save |
| fname | str, default = 'state_dict.pt' | Filename to save to |
### 5.1.15 train\_epoch

[TOC](#table-of-contents)

**Description**

Train one epoch.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| dataloader | DataLoader | DataLoader to train on |
| model | torch.nn.Module | Model to train |
| optimizer | torch.optim.Optimizer | Optimizer to use |
| criterion | torch.nn.Module | Criterion to use |
| num_batches | int, default = None | Number of batches to train on. If None, train on all batches |
| return_YT | bool, default = False | Append Y and T to results |

**Returns**

Dictionary with results : results : dict

### 5.1.16 validate\_epoch

[TOC](#table-of-contents)

**Description**

Validate one epoch.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| dataloader | DataLoader | DataLoader to validate on |
| model | torch.nn.Module | Model to validate |
| optimizer | torch.optim.Optimizer | Optimizer to use |
| criterion | torch.nn.Module | Criterion to use |
| num_batches | int, default = None | Number of batches to validate on. If None, validate on all batches |
| return_YT | bool, default = False | Append Y and T to results |

**Returns**

Dictionary with results : results : dict

