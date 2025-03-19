import torch
import numpy as np
from typing import Tuple, Mapping
from torch.utils.data import Dataset

class BertDataset(Dataset):
	""" 配合BertCollator使用 """

	def __init__(self, tokenizies: Mapping[str, torch.Tensor], labels: np.ndarray):
		super().__init__()
		self.tokenizies = tokenizies
		self.labels = labels

	def __getitem__(self, index: int) -> Tuple[Mapping[str, torch.Tensor], torch.Tensor]:
		return {k: v[index] for k, v in self.tokenizies.items()}, self.labels[index]

	def __len__(self):
		return len(self.labels)
