#!/usr/bin/env python
import os

import numpy as np
import PIL.Image
import torch
from torch.utils import data
import pdb


class MyData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images
                    - images (images here)
                - masks (ground truth)
                - ptag (initial maps)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, ptag='priors'):
        super(MyData, self).__init__()
        self.root = root
        self._transform = transform

        img_root = os.path.join(self.root, 'images/images')
        gt_root = os.path.join(self.root, 'masks')
        map_root = os.path.join(self.root, ptag)
        file_names = os.listdir(gt_root)
        self.img_names = []
        self.map_names = []
        self.gt_names = []
        self.names = []
        for i, name in enumerate(file_names):
            if not name.endswith('.png'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.map_names.append(
                os.path.join(map_root, name[:-4] + '.png')
            )
            self.gt_names.append(
                os.path.join(gt_root, name[:-4] + '.png')
            )
            self.names.append(name[:-4])

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img = img.resize((256, 256))
        img = np.array(img, dtype=np.uint8)

        map_file = self.map_names[index]
        map = PIL.Image.open(map_file)
        map = map.resize((256, 256))
        map = np.array(map, dtype=np.uint8)

        gt_file = self.gt_names[index]
        gt = PIL.Image.open(gt_file)
        gt = gt.resize((256, 256))
        gt = np.array(gt, dtype=np.int32)
        gt[gt != 0] = 1
        if self._transform:
            img, map, gt = self.transform(img, map, gt)
            return img, map, gt
        else:
            return img, map, gt

    def transform(self, img, map, gt):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()

        map = map.astype(np.float64) / 255
        map = torch.from_numpy(map).float()

        gt = torch.from_numpy(gt).float()
        return img, map, gt


class MyTestData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images
                    - images (images here)
                - masks (ground truth)
                - ptag (initial maps)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, ptag='priors'):
        super(MyTestData, self).__init__()
        self.root = root
        self._transform = transform

        img_root = os.path.join(self.root, 'images/images')
        map_root = os.path.join(self.root, ptag)
        file_names = os.listdir(img_root)
        self.img_names = []
        self.map_names = []
        self.names = []
        for i, name in enumerate(file_names):
            if not name.endswith('.jpg'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.map_names.append(
                os.path.join(map_root, name[:-4] + '.png')
            )
            self.names.append(name[:-4])

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img_size = img.size
        img = img.resize((256, 256))
        img = np.array(img, dtype=np.uint8)

        map_file = self.map_names[index]
        map = PIL.Image.open(map_file)
        map = map.resize((256, 256))
        map = np.array(map, dtype=np.uint8)
        if self._transform:
            img, map = self.transform(img, map)
            return img, map, self.names[index], img_size
        else:
            return img, map, self.names[index], img_size

    def transform(self, img, map):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()

        map = map.astype(np.float64) / 255
        map = torch.from_numpy(map).float()
        return img, map