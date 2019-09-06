import os
import pickle
import collections

from .vision import VisionDataset
from torchstream.io.datapoint import DataPoint
import torchstream.io.backends.opencv as backend
from torchstream.io.__support__ import SUPPORTED_IMAGES, SUPPORTED_VIDEOS
from torchstream.utils.download import download

CACHE_DIR = os.path.expanduser("~/.cache/torchstream/datasets/kinetics400/")
DOWNLOAD_SERVER_PREFIX = (
    "a18:/home/eecs/zhen/video-acc/download/"
    "torchstream/datasets/kinetics400/"
)


class Kinetics400(VisionDataset):

    def __init__(self, root, train,
                 transform=None, target_transform=None):
        root = os.path.expanduser(root)

        super(Kinetics400, self).__init__(root=root,
                                     transform=transform,
                                     target_transform=target_transform)
        # -------------------- #
        #   load datapoints    #
        # -------------------- #

        # assemble paths
        if not (os.path.exists(CACHE_DIR) and
                os.path.isdir(CACHE_DIR)):
            os.makedirs(CACHE_DIR, exist_ok=True)
        if train:
            datapoint_file_name = "kinetics_training.pkl"
        else:
            datapoint_file_name = "kinetics_val.pkl"
        datapoint_file_path = os.path.join(CACHE_DIR, datapoint_file_name)
        # download when missing
        if not os.path.exists(datapoint_file_path):
            print("downloading Kinetics datapoints...")
            download(src=os.path.join(DOWNLOAD_SERVER_PREFIX,
                                      datapoint_file_name),
                     dst=datapoint_file_path)
        # real load
        with open(datapoint_file_path, "rb") as fin:
            self.datapoints = pickle.load(fin)
            assert isinstance(self.datapoints, list), TypeError
            assert isinstance(self.datapoints[0], DataPoint), TypeError
        # replace dataset root
        for dp in self.datapoints:
            dp.root = root
            dp._path = dp.path
        # ------------------ #
        #  load class_to_idx #
        # ------------------ #
        # download labels
        label_file = "kinetics-400_labels.txt"
        label_path = os.path.join(CACHE_DIR, label_file)
        if not os.path.exists(label_path):
            print("downloading Kinetics-400 label_path...")
            label_src = os.path.join(DOWNLOAD_SERVER_PREFIX, label_file)
            download(label_src, label_path)
        # build class label to class id mapping (a dictionary)
        self.class_to_idx = collections.OrderedDict()
        with open(label_path, "r") as fin:
            for _line in fin:
                text = _line.split('\n')[0]
                text = text.split(' ')
                self.class_to_idx[' '.join(text[1:])] = int(text[0]) - 1

    def __len__(self):
        return len(self.datapoints)

    def __getitem__(self, index):
        datapoint = self.datapoints[index]

        if datapoint.ext in SUPPORTED_VIDEOS["RGB"]:
            loader = backend.video2ndarray
        elif datapoint.ext in SUPPORTED_IMAGES["RGB"]:
            loader = backend.frames2ndarray

        path = datapoint._path
        varray = loader(path)

        label = datapoint.label
        target = self.class_to_idx[label]

        if self.transform is not None:
            varray = self.transform(varray)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return varray, target