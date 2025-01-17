import pytorch_lightning as pl
import torch

from configs import *
from data.dataset_beat import BeatDataset
from data.dataset_quantisation import QuantisationDataset
from data.dataset_hand_part import HandPartDataset
from data.dataset_key_signature import KeySignatureDataset
from data.dataset_time_signature import TimeSignatureDataset

class Pm2sDataModule(pl.LightningDataModule):

    def __init__(self, args, feature='beat', full_train=True):
        super().__init__()
        
        # Parameters from input arguments
        self.workspace = args.workspace
        self.ASAP = args.ASAP
        self.A_MAPS = args.A_MAPS
        self.CPM = args.CPM
        self.feature = feature
        self.full_train = full_train

    def _get_dataset(self, split):
        if self.feature == 'beat':
            dataset = BeatDataset(self.workspace, split)
        elif self.feature == 'quantisation':
            dataset = QuantisationDataset(self.workspace, split)
        elif self.feature == 'hand_part':
            dataset = HandPartDataset(self.workspace, split)
        elif self.feature == 'key_signature':
            dataset = KeySignatureDataset(self.workspace, split)
        elif self.feature == 'time_signature':
            dataset = TimeSignatureDataset(self.workspace, split)
        else:
            raise ValueError('Unknown feature: {}'.format(self.feature))
        return dataset

    def train_dataloader(self):
        if self.full_train:
            dataset = self._get_dataset(split='all')
        else:
            dataset = self._get_dataset(split='train')
        sampler = torch.utils.data.sampler.RandomSampler(dataset)
        dataloader = torch.utils.data.dataloader.DataLoader(
            dataset,
            batch_size=batch_size,
            sampler=sampler,
            num_workers=num_workers,
            drop_last=True
        )
        return dataloader

    def val_dataloader(self):
        dataset = self._get_dataset(split='valid')
        sampler = torch.utils.data.sampler.SequentialSampler(dataset)
        dataloader = torch.utils.data.dataloader.DataLoader(
            dataset,
            batch_size=batch_size,
            sampler=sampler,
            num_workers=num_workers,
            drop_last=True
        )
        return dataloader

    def test_dataloader(self):
        dataset = self._get_dataset(split='test')
        sampler = torch.utils.data.sampler.SequentialSampler(dataset)
        dataloader = torch.utils.data.dataloader.DataLoader(
            dataset,
            batch_size=1,
            sampler=sampler,
            num_workers=0,
            drop_last=False
        )
        return dataloader


