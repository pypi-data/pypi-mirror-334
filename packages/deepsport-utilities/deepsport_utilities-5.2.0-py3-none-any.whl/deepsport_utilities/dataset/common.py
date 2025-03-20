from enum import IntFlag
import inspect

from mlworkflow import TransformedDataset


class Stage(IntFlag):
    TRAIN = 1
    EVAL  = 2


def transforms_wrapper(subsets, transforms):
    return {
        "training": DataAugmentationDataset(subsets.pop("training"), transforms, Stage.TRAIN),
           **{name: DataAugmentationDataset(subset, transforms) for name, subset in subsets.items()}
    }

class DataAugmentationDataset(TransformedDataset):
    def __init__(self, dataset, transforms, stage=Stage.EVAL):
        super().__init__(dataset, transforms)
        self.stage = stage

    def query_item(self, key):
        item = self.parent.query_item(key)
        for transform in self.transforms:
            signature = inspect.signature(transform.__call__)
            if len(signature.parameters) == 3:
                item = transform(key, item, self.stage)
            elif len(signature.parameters) == 2:
                item = transform(key, item)
        return item

SUBSETS_CONVERTION = {
    "train": ["training"],
    "val": ["validation", "testing"],
    "test": []
}

""" Group dict items
"""
def group(d, groups):
    return {name: {key: d[key] for key in group} for name, group in groups.items()}




