# -*- coding:utf-8 -*-


import os
import re
import sys
import cv2
import time
import json
import glob
import random
import shutil
import struct
import pickle
import socket
import logging
import hashlib
import zipfile
import threading
import numpy as np
import pandas as pd
from tqdm import tqdm


def timestamp_to_strftime(timestamp: float):
    if timestamp is None or timestamp == "":
        strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return strftime
    else:
        assert type(timestamp) == float, "timestamp should be float!"
        strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        return strftime


def strftime_to_timestamp(strftime: str):
    """
    strftime = "2024-11-06 12:00:00"
    """
    assert strftime is not None or strftime != "", "strftime is empty!"
    struct_time = time.strptime(strftime, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(struct_time)
    return timestamp


def get_date_time(mode=0):
    """
    0: %Y-%m-%d %H:%M:%S
    1: %Y %m %d %H:%M:%S
    2: %Y/%m/%d %H:%M:%S
    """
    if mode == 0:
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return datetime
    elif mode == 1:
        datetime = time.strftime("%Y %m %d %H:%M:%S", time.localtime(time.time()))
        return datetime
    elif mode == 2:
        datetime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        return datetime
    else:
        print("mode should be 0, 1, 2!")


def get_file_list(data_path: str, abspath=False) -> list:
    file_list = []
    list_ = sorted(os.listdir(data_path))
    for f in list_:
        f_path = data_path + "/{}".format(f)
        if os.path.isfile(f_path):
            if abspath:
                file_list.append(f_path)
            else:
                file_list.append(f)
    return file_list


def get_dir_list(data_path: str, abspath=False):
    dir_list = []
    list_ = sorted(os.listdir(data_path))
    for f in list_:
        f_path = data_path + "/{}".format(f)
        if os.path.isdir(f_path):
            if abspath:
                dir_list.append(f_path)
            else:
                dir_list.append(f)
    return dir_list


def get_dir_file_list(data_path: str, abspath=False):
    list_ = sorted(os.listdir(data_path))
    if abspath:
        list_new = []
        for f in list_:
            f_path = data_path + "/{}".format(f)
            list_new.append(f_path)
        return list_new
    else:
        return list_


def get_base_name(data_path: str):
    base_name = os.path.basename(data_path)
    return base_name


def get_dir_name(data_path: str):
    assert os.path.isdir(data_path), "{} is not a dir!".format(data_path)
    dir_name = os.path.basename(data_path)
    return dir_name


def get_file_name(data_path: str):
    """
    without suffix
    """
    assert os.path.isfile(data_path), "{} is not a file!".format(data_path)
    base_name = os.path.basename(data_path)
    file_name = os.path.splitext(base_name)[0]
    return file_name


def get_file_name_with_suffix(data_path: str):
    assert os.path.isfile(data_path), "{} is not a file!".format(data_path)
    base_name = os.path.basename(data_path)
    return base_name


def get_suffix(data_path: str):
    assert os.path.isfile(data_path), "{} is not a file!".format(data_path)
    base_name = os.path.basename(data_path)
    suffix = os.path.splitext(base_name)[1]
    return suffix


def make_save_path(data_path: str, relative=".", add_str="results"):
    base_name = get_base_name(data_path)
    if relative == ".":
        save_path = os.path.abspath(os.path.join(data_path, "..")) + "/{}_{}".format(base_name, add_str)
    elif relative == "..":
        save_path = os.path.abspath(os.path.join(data_path, "../..")) + "/{}_{}".format(base_name, add_str)
    elif relative == "...":
        save_path = os.path.abspath(os.path.join(data_path, "../../..")) + "/{}_{}".format(base_name, add_str)
    else:
        print("relative should be . or .. or ...")
        raise ValueError
    os.makedirs(save_path, exist_ok=True)
    # print("Create successful! save_path: {}".format(save_path))
    return save_path


def rename_files(data_path, use_orig_name=False, new_name_prefix="", zeros_num=7, start_num=0):
    data_list = sorted(os.listdir(data_path))
    length= len(data_list)
    for i in range(length):
        img_abs_path = data_path + "/" + data_list[i]
        orig_name = os.path.splitext(data_list[i])[0]
        file_ends = os.path.splitext(data_list[i])[1]
        if use_orig_name:
            new_name = "{}_{:0{}d}{}".format(orig_name, i + start_num, zeros_num, file_ends)
            os.rename(img_abs_path, data_path + "/" + new_name)
        else:
            if new_name_prefix is None or new_name_prefix == "":
                new_name = "{:0{}d}{}".format(i + start_num, zeros_num, file_ends)
            else:
                new_name = "{}_{:0{}d}{}".format(new_name_prefix, i + start_num, zeros_num, file_ends)
            os.rename(img_abs_path, data_path + "/" + new_name)


def save_file_path_to_txt(data_path: str, abspath=True):
    assert type(data_path) == str, "{} should be str!".format(data_path)
    dirname = os.path.basename(data_path)
    data_list = sorted(os.listdir(data_path))
    txt_save_path = os.path.abspath(os.path.join(data_path, "../{}_list.txt".format(dirname)))
    with open(txt_save_path, 'w', encoding='utf-8') as fw:
        for f in data_list:
            if abspath:
                f_abs_path = data_path + "/{}".format(f)
                f_abs_path = f_abs_path.replace("\\", "/")
                fw.write("{}\n".format(f_abs_path))
            else:
                fw.write("{}\n".format(f))

    print("Success! --> {}".format(txt_save_path))


if __name__ == '__main__':
    pass

    

































