from pathlib import Path
from PIL import Image
import json
import os

import torch
from torch.utils.data import Dataset


class PortraitDataset(Dataset):
    def __init__(self, path, transform):
        self.portraits = Path(path).glob('**/*/*.jpg')
        self.portraits = [str(path) for path in self.portraits]

        with open('portrait_tags.json', 'r') as f:
            self.port_tags = json.load(f)

        with open('tags.json', 'r') as f:
            self.tag_ind = json.load(f)
        self.lb_len = len(self.tag_ind)
        self.tag_ind = {tag:ind for ind,tag in enumerate(self.tag_ind)}

        self.transform = transform
      
    def one_hot(self, lb):
        labels = [0] * self.lb_len
        for tag in lb:
            labels[self.tag_ind[tag]] = 1
        return labels
    
    def __len__(self):
        return len(self.portraits)

    def __getitem__(self, index):
        path = self.portraits[index]
        img = Image.open(path)
        img = self.transform(img)
        basename = os.path.basename(path)
        lb = self.port_tags[basename]
        lb = self.one_hot(lb)
        lb = torch.tensor(lb).float()
        return img, lb
