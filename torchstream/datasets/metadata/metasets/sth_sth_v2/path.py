"""
Dataset Path
"""
__all__ = [
    "WEBM_DATA_PATH", "AVI_DATA_PATH",
    "JPG_DATA_PATH", "JPG_FILE_TMPL", "JPG_IDX_OFFSET",
    "RAW_DATA_PATH", "PRC_DATA_PATH",
]

import os

USER_HOME = os.path.expanduser("~")
LOCAL_DATASETS = os.path.join(USER_HOME, "Datasets-local")

# Default setting
# NOTE
# If you have your seetings, please change it
WEBM_DATA_PATH = os.path.join(USER_HOME, "Datasets", "Sth-sth", "Sth-sth-v2-webm")
AVI_DATA_PATH = os.path.join(USER_HOME, "Datasets", "Sth-sth", "Sth-sth-v2-avi")
JPG_DATA_PATH = os.path.join(USER_HOME, "Datasets", "Sth-sth", "Sth-sth-v2-jpg")
RAW_DATA_PATH = os.path.join(USER_HOME, "Datasets", "Sth-sth", "Sth-sth-v2-raw")
PRC_DATA_PATH = os.path.join(USER_HOME, "Datasets", "Sth-sth", "Sth-sth-v2-avi")


if os.path.exists(LOCAL_DATASETS):
    local_path = os.path.join(LOCAL_DATASETS, "Sth-sth", "Sth-sth-v2-jpg")
    if os.path.exists(local_path):
        JPG_DATA_PATH = local_path
    
if os.path.exists(LOCAL_DATASETS):
    local_path = os.path.join(LOCAL_DATASETS, "Sth-sth", "Sth-sth-v2-avi")
    if os.path.exists(local_path):
        AVI_DATA_PATH = local_path

# jpg file name template of the official datasets
JPG_FILE_TMPL = "{0:06d}"

# jpg frame index offset
JPG_IDX_OFFSET = 1
