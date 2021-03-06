"""Collecting DataPoints for different configurations of HMDB51
and dump the pickle file
"""
import os
import pickle
import argparse

from torchstream.utils.metadata import collect_folder

import label
import split

FILE_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)

parser = argparse.ArgumentParser()
parser.add_argument("root", type=str, help="path to dataset root")
parser.add_argument("--ext", default="avi", type=str,
                    help="dataset file extension")
parser.add_argument("--split", default=1, type=int,
                    help="dataset splitting plan")


def main(args):
    # collecting data points
    all_datapoints = collect_folder(
        root=args.root, ext=args.ext,
        annotations=label.class_to_idx
    )

    # get all sample names of given split plan
    train_set_names = split.train_sample_names(split_num=args.split)
    test_set_names = split.test_sample_names(split_num=args.split)

    # filter data points
    training_datapoints = []
    testing_datapoints = []
    for dp in all_datapoints:
        if dp.name in train_set_names:
            training_datapoints.append(dp)
        elif dp.name in test_set_names:
            testing_datapoints.append(dp)

    # dump files
    training_pickle = os.path.join(
        DIR_PATH,
        "hmdb51_training_split{}.pkl".format(args.split)
    )
    testing_pickle = os.path.join(
        DIR_PATH,
        "hmdb51_testing_split{}.pkl".format(args.split)
    )
    with open(training_pickle, "wb") as fout:
        pickle.dump(training_datapoints, fout)
    with open(testing_pickle, "wb") as fout:
        pickle.dump(testing_datapoints, fout)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
