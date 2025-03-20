from deepsport_utilities.ds.generic_dataset import import_dataset, export_dataset, GenericItem, serialize_keys, deserialize_keys
from deepsport_utilities.ds.instants_dataset import InstantsDataset
from deepsport_utilities.court import Court
from deepsport_utilities.dataset import find, Subset, Stage

__all__ = ["import_dataset", "export_dataset", "GenericItem", "serialize_keys", "deserialize_keys", "InstantsDataset", "Court", "find", "Subset", "Stage"]

import importlib.metadata
try:
    # __package__ allows for the case where __name__ is "__main__"
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"
