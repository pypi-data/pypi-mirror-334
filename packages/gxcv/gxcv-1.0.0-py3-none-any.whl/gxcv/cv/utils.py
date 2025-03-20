# -*- coding:utf-8 -*-

import os
import re
import sys
import PIL.Image
import cv2
import json
import time
import math
import copy
import glob
import yaml
import random
import shutil
import codecs
import imghdr
import struct
import pickle
import hashlib
import base64
import socket
import argparse
import threading
import itertools
import numpy as np
import pandas as pd
from tqdm import tqdm
import PIL
from PIL import (
    Image, ImageDraw,
    ImageOps, ImageFont
)
import skimage
import scipy
import torch
import torchvision
import onnxruntime as ort
from torchvision import transforms
import matplotlib as mpl
import matplotlib.pyplot as plt
import pyclipper
from shapely.geometry import Polygon
from torch import nn
from collections import OrderedDict
from sklearn.model_selection import train_test_split
from labelme import utils
import subprocess

lock = threading.Lock()


# Base utils ===================================================
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
    print("Create directory successful! save_path: {}".format(save_path))
    return save_path


def save_file_path_to_txt(data_path: str, abspath=True):
    assert type(data_path) == str, "{} should be str!".format(data_path)
    dirname = os.path.basename(data_path)
    data_list = sorted(os.listdir(data_path))
    txt_save_path = os.path.abspath(os.path.join(data_path, "../{}_list.txt".format(dirname)))
    with open(txt_save_path, 'w', encoding='utf-8') as fw:
        for f in data_list:
            if abspath:
                f_abs_path = data_path + "/{}".format(f)
                fw.write("{}\n".format(f_abs_path))
            else:
                fw.write("{}\n".format(f))

    print("Success! --> {}".format(txt_save_path))


def cv2pil(image):
    assert isinstance(image, np.ndarray), f'Input image type is not cv2 and is {type(image)}!'
    if len(image.shape) == 2:
        return Image.fromarray(image)
    elif len(image.shape) == 3:
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:
        return None


def pil2cv(image):
    assert isinstance(image, Image.Image), f'Input image type is not PIL.image and is {type(image)}!'
    if len(image.split()) == 1:
        return np.asarray(image)
    elif len(image.split()) == 3:
        return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    elif len(image.split()) == 4:
        return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGBA2BGR)
    else:
        return None
    

def holefill(img):
    img_copy = img.copy()
    mask = np.zeros((img.shape[0]+2,img.shape[1]+2),dtype=np.uint8)
    cv2.floodFill(img,mask,(0,0),255)
    img_inverse = cv2.bitwise_not(img)
    dst = cv2.bitwise_or(img_copy,img_inverse)
    return dst


def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def process_list(lst):
    # 步骤 1：替换前面的 0 为 255（如果连续的 0 小于等于 5）
    count_zeros = 0
    for i in range(len(lst)):
        if lst[i] == 0:
            count_zeros += 1
        else:
            break

    # 如果前面的 0 数量小于等于 5，则替换为 255
    if count_zeros <= 5:
        for i in range(count_zeros):
            lst[i] = 255

    # 步骤 2：找到第一个连续 5 个 0，并从这个位置开始，后续的所有 255 替换为 0
    for i in range(len(lst) - 4):  # 只需要遍历到倒数第 5 个元素
        if lst[i:i + 5] == [0] * 5:
            # 找到连续 5 个 0 后，替换后续所有的 255 为 0
            for j in range(i + 5, len(lst)):
                if lst[j] == 255:
                    lst[j] = 0
            break  # 只处理第一个出现的连续 5 个 0

    return lst


# HSV域处理+
def deal_HSV(src,minArea,maxArea,pts):
    # 转HSV空间
    # 第一条平行边：从 (1002, 57) 到 (1127, 57)
    x1, y1 = pts[0]  # (1002, 57)
    x2, y2 = pts[1]  # (1127, 57)

    # 第二条平行边：从 (1435, 983) 到 (755, 983)
    x3, y3 = pts[2]  # (1435, 983)
    x4, y4 = pts[3]  # (755, 983)

    # 计算每条边的中心点
    center_1 = (int((x1 + x2) / 2), int((y1 + y2) / 2))
    center_2 = (int((x3 + x4) / 2), int((y3 + y4) / 2))

    x1,y1 = center_1
    x2,y2 = center_2


    Drawsrc = np.zeros((src.shape[:3]), dtype=src.dtype)
    Drawsrc = np.copy(src)
    HSVimage = cv2.cvtColor(Drawsrc, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSVimage)
    # cv2.imshow('S', V)
    # cv2.imshow("h",H)
    cv2.imshow("V",V)

    sumValue = np.sum(V)
    Tcount = cv2.countNonZero(V)
    if Tcount == 0:
        MeanValue = 0
    else:
        MeanValue = int(sumValue / Tcount)

    thresholdValue = int(MeanValue)

    # S通道处理（比对目前图像，S域内对比度明显)
    # V = cv2.GaussianBlur(V, (5, 5), 0)
    thresh, Th_image = cv2.threshold(V, thresholdValue, 255, cv2.THRESH_BINARY)
    cv2.imshow('111', Th_image)
    kernel = np.ones((8, 8), np.uint8)

    # 进行腐蚀操作
    Th_image = cv2.erode(Th_image, kernel, iterations=1)
    # cv2.imshow('bb', Th_image)

    kernel = np.ones((5, 5), np.uint8)
    Th_image = cv2.dilate(Th_image, kernel, iterations=1)
    cv2.imshow('33', Th_image)
    # Th_image = find_boundary_and_fit_line(Th_image)
    # cv2.imshow("44",Th_image)
    # Th_image = process_mask(Th_image,pts)
    # cv2.imshow("55",Th_image)

    count = 0
    cound = []
    f = False

    if x2 - x1 != 0:
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y = int(k * x + b)
            cound.append(Th_image[y,x])
            if Th_image[y, x] == 0:
                count += 1
    print(cound)
    cound.reverse()
    list = process_list(cound)
    print(list)
    print(len(list))
    list0 = list.count(0)
    print(list0)
    if (minArea<count) and (maxArea>count):
        f = True

    return f, src,(x1,y1),(x2,y2),list0


def order_points(pts):
    # 根据坐标点的顺序排序，分别为左上、右上、右下和左下
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_crop(image, pts):
    # 对坐标点进行排序
    rect = order_points(pts)

    # 计算输入图像的宽度和高度
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # 定义裁剪后输出图像的四个点坐标
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # 计算透视变换矩阵并进行变换
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def mask_outside_polygon(image, pts):
    mask = np.zeros_like(image)
    cv2.fillConvexPoly(mask, pts.astype(int), (255, 255, 255))
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


class CLS_ORT(object):
    """
    yolov5-6.2 yolov5-7.0
    onnx-opset 10
    """
    def __init__(self, config_path, cuda=False):
        self.cuda = cuda and torch.cuda.is_available()
        self.providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if self.cuda else ['CPUExecutionProvider']
        self.config_path = config_path
        self.config = self.get_config()
        self.weight_path = self.config["path"]["cls_model_path"].replace("\\", "/")
        self.class_path = self.config["path"]["cls_class_path"].replace("\\", "/")
        self.INPUT_WIDTH = int(self.weight_path.split("_")[-3])
        self.INPUT_HEIGHT = int(self.weight_path.split("_")[-2])
        self.INPUT_SIZE = (self.INPUT_HEIGHT, self.INPUT_WIDTH)
        self.conf_threshold = float(self.config["threshold"]["conf_threshold"])
        self.mean = list(map(float, self.config["threshold"]["mean"].replace(", ", ",").split(",")))
        self.std = list(map(float, self.config["threshold"]["std"].replace(", ", ",").split(",")))
        self.mean = np.array(self.mean).reshape(1, 1, 3)
        self.std = np.array(self.std).reshape(1, 1, 3)
        self.keep_ratio_flag = bool(self.config["flag"]["keep_ratio"])
        self.session = ort.InferenceSession(self.weight_path, providers=self.providers)
        self.input_names = self.session.get_inputs()[0].name
        self.output_names = self.session.get_outputs()[0].name

    def get_config(self):
        with open(self.config_path, "rb") as file:
            config = yaml.safe_load(file)
        return config
    
    def keep_ratio(self, img, flag=True, shape=(128, 128)):
        if flag:
            img, ratio, (dw, dh) = self.letterbox(img, new_shape=shape)
            return img
        else:
            img = cv2.resize(img, shape)
            return img
        
    def letterbox(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, ratio, (dw, dh)
    
    def to_numpy(self, tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    def pre_process(self, input, imgsz=(128, 128)):
        if imgsz is None and self.INPUT_SIZE is not None:
            self.imgsz = self.INPUT_SIZE
        else:
            assert imgsz is not None, "imgsz is None!"
            self.imgsz = imgsz

        if isinstance(input, str):
            img0 = cv2.imread(input)
        elif isinstance(input, Image.Image):
            img0 = pil2cv(input)
        else:
            assert isinstance(input, np.ndarray), f'input is not np.ndarray and is {type(input)}!'
            img0 = input

        img = self.keep_ratio(img0, flag=self.keep_ratio_flag, shape=self.imgsz)
        img = np.transpose(img, (2, 0, 1))
        img = np.ascontiguousarray(img)
        img = img.astype(dtype=np.float32)
        img /= 255.0
        # img = (img - self.mean) / self.std
        img = (img - 0.5) / 0.5
        img = np.expand_dims(img, axis=0)

        return img

    def inference(self, img):
        # ort_outs = self.session.run([self.output_names], {self.input_names: self.to_numpy(img)})
        ort_outs = self.session.run([self.output_names], {self.input_names: img})
        return ort_outs[0]

    def post_process(self, ort_out):
        cls = np.argmax(ort_out)
        return cls
    

class YOLOv5_ORT(object):
    """
    yolov5-6.2 yolov5-7.0
    onnx-opset 10
    """
    def __init__(self, config_path, detection_name, cuda=False):
        self.cuda = cuda and torch.cuda.is_available()
        self.providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if self.cuda else ['CPUExecutionProvider']
        self.config_path = config_path
        self.detection_name = detection_name
        self.config = self.get_config()
        self.weight_path = self.config["{}".format(self.detection_name)]["path"]["det_model_path"].replace("\\", "/")
        self.class_path = self.config["{}".format(self.detection_name)]["path"]["det_class_path"].replace("\\", "/")
        self.INPUT_WIDTH = int(self.weight_path.split("_")[-3])
        self.INPUT_HEIGHT = int(self.weight_path.split("_")[-2])
        self.INPUT_SIZE = (self.INPUT_HEIGHT, self.INPUT_WIDTH)
        self.conf_threshold = float(self.config["{}".format(self.detection_name)]["threshold"]["conf_threshold"])
        self.iou_threshold = float(self.config["{}".format(self.detection_name)]["threshold"]["iou_threshold"])
        self.session = ort.InferenceSession(self.weight_path, providers=self.providers)
        self.input_names = self.session.get_inputs()[0].name
        self.output_names = self.session.get_outputs()[0].name

    def get_config(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    
    def load_classes(self):
        class_list = []
        with open(self.class_path, "r", encoding="utf-8") as f:
            class_list = [cname.strip() for cname in f.readlines()]
        return class_list

    def letterbox(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios
        
        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, ratio, (dw, dh)
    
    def xywh2xyxy(self, x):
        # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
        return y

    def box_area(self, box):
        # box = xyxy(4,n)
        return (box[2] - box[0]) * (box[3] - box[1])
    
    def box_iou(self, box1, box2, eps=1e-7):
        # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
        """
        Return intersection-over-union (Jaccard index) of boxes.
        Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
        Arguments:
            box1 (Tensor[N, 4])
            box2 (Tensor[M, 4])
        Returns:
            iou (Tensor[N, M]): the NxM matrix containing the pairwise
                IoU values for every element in boxes1 and boxes2
        """

        # inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
        (a1, a2), (b1, b2) = box1[:, None].chunk(2, 2), box2.chunk(2, 1)
        inter = (torch.min(a2, b2) - torch.max(a1, b1)).clamp(0).prod(2)

        # IoU = inter / (area1 + area2 - inter)
        return inter / (self.box_area(box1.T)[:, None] + self.box_area(box2.T) - inter + eps)
    
    def non_max_suppression(self, prediction,
                            conf_thres=0.25,
                            iou_thres=0.45,
                            classes=None,
                            agnostic=False,
                            multi_label=False,
                            labels=(),
                            max_det=300):
        """Non-Maximum Suppression (NMS) on inference results to reject overlapping bounding boxes

        Returns:
             list of detections, on (n,6) tensor per image [xyxy, conf, cls]
        """

        bs = prediction.shape[0]  # batch size
        nc = prediction.shape[2] - 5  # number of classes
        xc = prediction[..., 4] > conf_thres  # candidates

        # Checks
        assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
        assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'

        # Settings
        # min_wh = 2  # (pixels) minimum box width and height
        max_wh = 7680  # (pixels) maximum box width and height
        max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
        time_limit = 0.3 + 0.03 * bs  # seconds to quit after
        redundant = True  # require redundant detections
        multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)
        merge = False  # use merge-NMS

        # output = [torch.zeros((0, 6), device=prediction.device)] * bs
        output = [torch.zeros((0, 6))] * bs
        for xi, x in enumerate(prediction):  # image index, image inference
            # Apply constraints
            # x[((x[..., 2:4] < min_wh) | (x[..., 2:4] > max_wh)).any(1), 4] = 0  # width-height
            x = x[xc[xi]]  # confidence

            # Cat apriori labels if autolabelling
            if labels and len(labels[xi]):
                lb = labels[xi]
                # v = torch.zeros((len(lb), nc + 5), device=x.device)
                v = torch.zeros((len(lb), nc + 5))
                v[:, :4] = lb[:, 1:5]  # box
                v[:, 4] = 1.0  # conf
                v[range(len(lb)), lb[:, 0].long() + 5] = 1.0  # cls
                x = torch.cat((x, v), 0)

            # If none remain process next image
            if not x.shape[0]:
                continue

            # Compute conf
            x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf

            # Box (center x, center y, width, height) to (x1, y1, x2, y2)
            box = self.xywh2xyxy(x[:, :4])

            # Detections matrix nx6 (xyxy, conf, cls)
            if multi_label:
                i, j = (x[:, 5:] > conf_thres).nonzero(as_tuple=False).T
                x = torch.cat((box[i], x[i, j + 5, None], j[:, None].float()), 1)
            else:  # best class only
                # conf, j = x[:, 5:].max(1, keepdim=True)
                conf, j = torch.tensor(x[:, 5:]).float().max(1, keepdim=True)
                # x = torch.cat((box, conf, j.float()), 1)[conf.view(-1) > conf_thres]
                x = torch.cat((torch.tensor(box), conf, j.float()), 1)[conf.view(-1) > conf_thres]

            # Filter by class
            if classes is not None:
                # x = x[(x[:, 5:6] == torch.tensor(classes, device=x.device)).any(1)]
                x = x[(x[:, 5:6] == torch.tensor(classes)).any(1)]

            # Apply finite constraint
            # if not torch.isfinite(x).all():
            #     x = x[torch.isfinite(x).all(1)]

            # Check shape
            n = x.shape[0]  # number of boxes
            if not n:  # no boxes
                continue
            elif n > max_nms:  # excess boxes
                x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence

            # Batched NMS
            c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
            boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
            i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
            if i.shape[0] > max_det:  # limit detections
                i = i[:max_det]
            if merge and (1 < n < 3E3):  # Merge NMS (boxes merged using weighted mean)
                # update boxes as boxes(i,4) = weights(i,n) * boxes(n,4)
                iou = self.box_iou(boxes[i], boxes) > iou_thres  # iou matrix
                weights = iou * scores[None]  # box weights
                # x[i, :4] = torch.mm(weights, x[:, :4]).float() / weights.sum(1, keepdim=True

            output[xi] = x[i]
            # if (time.time() - t) > time_limit:
            #     LOGGER.warning(f'WARNING: NMS time limit {time_limit:.3f}s exceeded')
            #     break  # time limit exceeded

        return output
    
    def clip_coords(self, boxes, shape):
        # Clip bounding xyxy bounding boxes to image shape (height, width)
        if isinstance(boxes, torch.Tensor):  # faster individually
            boxes[:, 0].clamp_(0, shape[1])  # x1
            boxes[:, 1].clamp_(0, shape[0])  # y1
            boxes[:, 2].clamp_(0, shape[1])  # x2
            boxes[:, 3].clamp_(0, shape[0])  # y2
        else:  # np.array (faster grouped)
            boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, shape[1])  # x1, x2
            boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, shape[0])  # y1, y2

    def scale_coords(self, img1_shape, coords, img0_shape, ratio_pad=None):
        # Rescale coords (xyxy) from img1_shape to img0_shape
        if ratio_pad is None:  # calculate from img0_shape
            gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
            pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
        else:
            gain = ratio_pad[0][0]
            pad = ratio_pad[1]

        coords[:, [0, 2]] -= pad[0]  # x padding
        coords[:, [1, 3]] -= pad[1]  # y padding
        coords[:, :4] /= gain
        self.clip_coords(coords, img0_shape)
        return coords
    
    def pre_process(self, input, imgsz=(640, 640), stride=32):
        if imgsz is None and self.INPUT_SIZE is not None:
            self.imgsz = self.INPUT_SIZE
        else:
            assert imgsz is not None, "imgsz is None!"
            self.imgsz = imgsz
            
        if isinstance(input, str):
            img0 = cv2.imread(input)
        elif isinstance(input, Image.Image):
            img0 = pil2cv(input)
        else:
            assert isinstance(input, np.ndarray), f'input is not np.ndarray and is {type(input)}!'
            img0 = input

        self.srcsz = img0.shape[:2]
        img = self.letterbox(img0, self.imgsz, stride=stride, auto=False)[0]
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        img = img.astype(dtype=np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        return img0, img
    
    def inference(self, img):
        # im = img.cpu().numpy()  # torch to numpy
        pred = self.session.run([self.output_names], {self.input_names: img})[0]
        return pred

    def post_process(self, pred, conf_threshold, iou_threshold):
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

        output = self.non_max_suppression(pred, self.conf_threshold, self.iou_threshold, agnostic=False)
        out_bbx = []
        for i, det in enumerate(output):  # detections per image
            if len(det):
                det[:, :4] = self.scale_coords(self.imgsz, det[:, :4], self.srcsz).round()
                for *xyxy, conf, cls in reversed(det):
                    x1y1x2y2_VOC = [int(round(ci)) for ci in torch.tensor(xyxy).view(1, 4).view(-1).tolist()]
                    x1y1x2y2_VOC.append(float(conf.numpy()))
                    x1y1x2y2_VOC.append(int(cls.numpy()))
                    out_bbx.append(x1y1x2y2_VOC)

        return out_bbx


class YOLOv5_CV2(object):
    """
    opencv-contrib-python  4.9.0.80
    opencv-python          4.9.0.80
    opencv-python-headless 4.9.0.80
    """
    def __init__(self, config_path, detection_name, cuda=False):
        self.config_path = config_path
        self.detection_name = detection_name
        self.config = self.get_config()
        self.weight_path = self.config["{}".format(self.detection_name)]["path"]["det_model_path"].replace("\\", "/")
        self.class_path = self.config["{}".format(self.detection_name)]["path"]["det_class_path"].replace("\\", "/")
        self.net = self.build_model(cuda)
        self.class_list = self.load_classes()
        self.cuda = cuda
        self.INPUT_WIDTH = int(self.weight_path.split("_")[-3])
        self.INPUT_HEIGHT = int(self.weight_path.split("_")[-2])
        self.score_threshold = self.config["{}".format(self.detection_name)]["threshold"]["score_threshold"]
        self.nms_threshold = self.config["{}".format(self.detection_name)]["threshold"]["nms_threshold"]
        self.confidence_threshold = self.config["{}".format(self.detection_name)]["threshold"]["confidence_threshold"]

    def get_config(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    
    def build_model(self, cuda):
        net = cv2.dnn.readNet(self.weight_path)
        if cuda:
            print("Attempting to use CUDA")
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        else:
            print("Running on CPU")
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net

    def inference(self, image):
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (self.INPUT_WIDTH, self.INPUT_HEIGHT), swapRB=True, crop=False)
        self.net.setInput(blob)
        preds = self.net.forward()
        return preds

    def load_classes(self):
        class_list = []
        with open(self.class_path, "r", encoding="utf-8") as f:
            class_list = [cname.strip() for cname in f.readlines()]
        return class_list

    def wrap_detection(self, input_image, output_data):
        if not isinstance(output_data, np.ndarray):
            raise TypeError("Output data should be a NumPy array")

        class_ids = []
        confidences = []
        boxes = []

        rows = output_data.shape[0]  # Use the first dimension as rows
        image_width, image_height, _ = input_image.shape
        x_factor = image_width / self.INPUT_WIDTH
        y_factor = image_height / self.INPUT_HEIGHT

        for r in range(rows):
            row = output_data[r]
            confidence = row[4]
            if confidence >= self.confidence_threshold:
                classes_scores = row[5:]
                _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
                class_id = max_indx[1]
                if classes_scores[class_id] > self.score_threshold:
                    confidences.append(confidence)
                    class_ids.append(class_id)
                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                    left = int((x - 0.5 * w) * x_factor)
                    top = int((y - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)
                    box = np.array([left, top, width, height])
                    boxes.append(box)

        boxes = np.array(boxes)

        unique_class_ids = np.unique(class_ids)
        result_class_ids = []
        result_confidences = []
        result_boxes = []
        for class_id in unique_class_ids:
            class_mask = np.array([i == class_id for i in class_ids])
            class_boxes = boxes[class_mask]
            class_confidences = np.array(confidences)[class_mask]
            indexes = cv2.dnn.NMSBoxes(class_boxes.tolist(), class_confidences.tolist(), self.score_threshold, self.nms_threshold)
            for i in indexes:
                result_confidences.append(class_confidences[i])
                result_class_ids.append(class_id)
                result_boxes.append(class_boxes[i])

        return result_class_ids, result_confidences, result_boxes

    def format_yolov5(self, frame):
        row, col, _ = frame.shape
        max_dim = max(col, row)
        result = np.zeros((max_dim, max_dim, 3), np.uint8)
        result[0:row, 0:col] = frame
        return result

    def detect(self, src, SCORE_THRESHOLD, NMS_THRESHOLD, CONFIDENCE_THRESHOLD):
        self.score_threshold = SCORE_THRESHOLD
        self.nms_threshold = NMS_THRESHOLD
        self.confidence_threshold = CONFIDENCE_THRESHOLD

        class_list = self.load_classes()
        inputImage = self.format_yolov5(src)
        lock.acquire()
        outs = self.inference(inputImage)
        lock.release()
        class_ids, confidences, boxes = self.wrap_detection(inputImage, outs[0])
        name = []
        for (classid, confidence, box) in zip(class_ids, confidences, boxes):
            color = np.random.choice(256, size=3)
            cv2.rectangle(src, box, color, 2)
            cv2.rectangle(src, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
            cv2.putText(src, class_list[classid], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0))
            name.append(class_list[classid])

        return src, class_ids, confidences, boxes


class Colors:
    """
    Ultralytics default color palette https://ultralytics.com/.

    This class provides methods to work with the Ultralytics color palette, including converting hex color codes to
    RGB values.

    Attributes:
        palette (list of tuple): List of RGB color values.
        n (int): The number of colors in the palette.
        pose_palette (np.array): A specific color palette array with dtype np.uint8.
    """

    def __init__(self):
        """Initialize colors as hex = matplotlib.colors.TABLEAU_COLORS.values()."""
        hexs = (
            "FF3838",
            "FF9D97",
            "FF701F",
            "FFB21D",
            "CFD231",
            "48F90A",
            "92CC17",
            "3DDB86",
            "1A9334",
            "00D4BB",
            "2C99A8",
            "00C2FF",
            "344593",
            "6473FF",
            "0018EC",
            "8438FF",
            "520085",
            "CB38FF",
            "FF95C8",
            "FF37C7",
        )
        self.palette = [self.hex2rgb(f"#{c}") for c in hexs]
        self.n = len(self.palette)
        self.pose_palette = np.array(
            [
                [255, 128, 0],
                [255, 153, 51],
                [255, 178, 102],
                [230, 230, 0],
                [255, 153, 255],
                [153, 204, 255],
                [255, 102, 255],
                [255, 51, 255],
                [102, 178, 255],
                [51, 153, 255],
                [255, 153, 153],
                [255, 102, 102],
                [255, 51, 51],
                [153, 255, 153],
                [102, 255, 102],
                [51, 255, 51],
                [0, 255, 0],
                [0, 0, 255],
                [255, 0, 0],
                [255, 255, 255],
            ],
            dtype=np.uint8,
        )

    def __call__(self, i, bgr=False):
        """Converts hex color codes to RGB values."""
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):
        """Converts hex color codes to RGB values (i.e. default PIL order)."""
        return tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))


class YOLO11_ORT(object):
    """
    YOLO11 model for handling detection & pose inference and visualization.
    """
    def __init__(self, config_path, detection_name, cuda=False, vision_type='det'):
        self.cuda = cuda and torch.cuda.is_available()
        self.providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if self.cuda else ['CPUExecutionProvider']
        self.config_path = config_path
        self.detection_name = detection_name
        self.config = self.get_config()
        self.vision_type = vision_type
        assert self.vision_type in ['det', 'pose', 'kpt', 'seg'], "type must be 'det', 'pose', 'kpt' or 'seg'!"
        self.weight_path = self.config["{}".format(self.detection_name)]["path"]["{}_model_path".format(self.vision_type)].replace("\\", "/")
        self.class_path = self.config["{}".format(self.detection_name)]["path"]["{}_class_path".format(self.vision_type)].replace("\\", "/")
        self.INPUT_WIDTH = int(self.weight_path.split("_")[-3])
        self.INPUT_HEIGHT = int(self.weight_path.split("_")[-2])
        self.INPUT_SIZE = (self.INPUT_HEIGHT, self.INPUT_WIDTH)
        self.conf_threshold = float(self.config["{}".format(self.detection_name)]["threshold"]["conf_threshold"])
        self.iou_threshold = float(self.config["{}".format(self.detection_name)]["threshold"]["iou_threshold"])
        self.session = ort.InferenceSession(self.weight_path, providers=self.providers)
        self.input_names = self.session.get_inputs()[0].name
        self.input_width = self.session.get_inputs()[0].shape[2]
        self.input_height = self.session.get_inputs()[0].shape[3]
        self.input_size = (self.input_height, self.input_width)
        self.output_names = self.session.get_outputs()[0].name

        # Load the class names from the COCO dataset
        # self.classes = yaml_load(check_yaml("coco8.yaml"))["names"]
        self.classes = self.load_classes()

        # Generate a color palette for the classes
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.colors = Colors()
        self.limb_color = self.colors.pose_palette[[9, 9, 9, 9, 7, 7, 7, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16]]
        self.kpt_color = self.colors.pose_palette[[16, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9]]
        self.skeleton = [
                    [16, 14],
                    [14, 12],
                    [17, 15],
                    [15, 13],
                    [12, 13],
                    [6, 12],
                    [7, 13],
                    [6, 7],
                    [6, 8],
                    [7, 9],
                    [8, 10],
                    [9, 11],
                    [2, 3],
                    [1, 2],
                    [1, 3],
                    [2, 4],
                    [3, 5],
                    [4, 6],
                    [5, 7],
                ]
        
    def get_config(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    
    def load_classes(self):
        class_list = []
        with open(self.class_path, "r", encoding="utf-8") as f:
            class_list = [cname.strip() for cname in f.readlines()]
        return class_list

    def draw_detections(self, img, box, score, class_id):
        """
        Draws bounding boxes and labels on the input image based on the detected objects.

        Args:
            img: The input image to draw detections on.
            box: Detected bounding box.
            score: Corresponding detection score.
            class_id: Class ID for the detected object.

        Returns:
            None
        """
        # Extract the coordinates of the bounding box
        x1, y1, w, h = box

        # Retrieve the color for the class ID
        color = self.color_palette[class_id]

        # Draw the bounding box on the image
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)

        # Create the label text with class name and score
        # label = f"{self.classes[class_id]}: {score:.2f}"
        label = f"{class_id}: {score:.2f}"

        # Calculate the dimensions of the label text
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        # Calculate the position of the label text
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10

        # Draw a filled rectangle as the background for the label text
        cv2.rectangle(
            img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color, cv2.FILLED
        )

        # Draw the label text on the image
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, input):
        """
        Preprocesses the input image before performing inference.

        Returns:
            image_data: Preprocessed image data ready for inference.
        """
        if isinstance(input, str):
            self.img = cv2.imread(input)
        elif isinstance(input, Image.Image):
            self.img = self.pil2cv(input)
        else:
            assert isinstance(input, np.ndarray), f'input is not np.ndarray and is {type(input)}!'
            self.img = input

        # Get the height and width of the input image
        self.img_height, self.img_width = self.img.shape[:2]

        # Convert the image color space from BGR to RGB
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        # Resize the image to match the input shape
        img = cv2.resize(img, (self.input_width, self.input_height))

        # Normalize the image data by dividing it by 255.0
        image_data = np.array(img) / 255.0

        # Transpose the image to have the channel dimension as the first dimension
        image_data = np.transpose(image_data, (2, 0, 1))  # Channel first

        # Expand the dimensions of the image data to match the expected input shape
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)

        # Return the preprocessed image data
        return image_data

    def det_postprocess(self, input_image, output):
        """
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.

        Args:
            input_image (numpy.ndarray): The input image.
            output (numpy.ndarray): The output of the model.

        Returns:
            numpy.ndarray: The input image with detections drawn on it.
        """
        # Transpose and squeeze the output to match the expected shape
        outputs = np.transpose(np.squeeze(output[0]))

        # Get the number of rows in the outputs array
        rows = outputs.shape[0]

        # Lists to store the bounding boxes, scores, and class IDs of the detections
        boxes = []
        scores = []
        class_ids = []

        # Calculate the scaling factors for the bounding box coordinates
        x_factor = self.img_width / self.input_width
        y_factor = self.img_height / self.input_height

        # Iterate over each row in the outputs array
        for i in range(rows):
            # Extract the class scores from the current row
            classes_scores = outputs[i][4:]

            # Find the maximum score among the class scores
            max_score = np.amax(classes_scores)

            # If the maximum score is above the confidence threshold
            if max_score >= self.confidence_thres:
                # Get the class ID with the highest score
                class_id = np.argmax(classes_scores)

                # Extract the bounding box coordinates from the current row
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]

                # Calculate the scaled coordinates of the bounding box
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                # Add the class ID, score, and box coordinates to the respective lists
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        # Apply non-maximum suppression to filter out overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)

        # Iterate over the selected indices after non-maximum suppression
        for i in indices:
            # Get the box, score, and class ID corresponding to the index
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]

            # Draw the detection on the input image
            self.draw_detections(input_image, box, score, class_id)

        # Return the modified input image
        return input_image
    
    def det_detect(self, img_path):
        """
        Performs inference using an ONNX model and returns the output image with drawn detections.

        Returns:
            output_img: The output image with drawn detections.
        """
        
        # Preprocess the image data
        img_data = self.preprocess(img_path)

        # Run inference using the preprocessed image data
        outputs = self.session.run(None, {self.model_inputs[0].name: img_data})
        output = self.det_postprocess(self.img, outputs)

        return output
    
    def cv2pil(self, image):
        assert isinstance(image, np.ndarray), f'Input image type is not cv2 and is {type(image)}!'
        if len(image.shape) == 2:
            return Image.fromarray(image)
        elif len(image.shape) == 3:
            return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            return None

    def pil2cv(self, image):
        assert isinstance(image, Image.Image), f'Input image type is not PIL.image and is {type(image)}!'
        if len(image.split()) == 1:
            return np.asarray(image)
        elif len(image.split()) == 3:
            return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        elif len(image.split()) == 4:
            return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGBA2BGR)
        else:
            return None
        
    def xywh2xyxy(self, xywh):
        xyxy = np.copy(xywh)
        xyxy[:, 0] = xywh[:, 0] - xywh[:, 2] / 2
        xyxy[:, 1] = xywh[:, 1] - xywh[:, 3] / 2
        xyxy[:, 2] = xywh[:, 0] + xywh[:, 2] / 2
        xyxy[:, 3] = xywh[:, 1] + xywh[:, 3] / 2
        return xyxy

    def nms(self, boxes, scores, keypoints, iou_threshold=0.45, candidate_size=200):
        """
        Args:
            boxex (N, 4): boxes in corner-form.
            scores (N, 1): scores.
            iou_threshold: intersection over union threshold.
            candidate_size: only consider the candidates with the highest scores.
        Returns:
            picked: a list of indexes of the kept boxes
        """
        picked = []
        indexes = np.argsort(scores)
        indexes = indexes[::-1]
        indexes = indexes[:candidate_size]

        while len(indexes) > 0:
            current = indexes[0]
            picked.append(current)
            if len(indexes) == 1:
                break
            current_box = boxes[current, :]
            indexes = indexes[1:]
            rest_boxes = boxes[indexes, :]
            iou = self.iou_of(
                rest_boxes,
                np.expand_dims(current_box, axis=0),
            )
            indexes = indexes[iou <= iou_threshold]

        return boxes[picked, :], scores[picked], keypoints[picked, :]


    def iou_of(self, boxes0, boxes1, eps=1e-5):
        """Return intersection-over-union (Jaccard index) of boxes.
        Args:
            boxes0 (N, 4): ground truth boxes.
            boxes1 (N or 1, 4): predicted boxes.
            eps: a small number to avoid 0 as denominator.
        Returns:
            iou (N): IoU values.
        """
        overlap_left_top = np.maximum(boxes0[..., :2], boxes1[..., :2])
        overlap_right_bottom = np.minimum(boxes0[..., 2:], boxes1[..., 2:])

        overlap_area = self.area_of(overlap_left_top, overlap_right_bottom)
        area0 = self.area_of(boxes0[..., :2], boxes0[..., 2:])
        area1 = self.area_of(boxes1[..., :2], boxes1[..., 2:])
        return overlap_area / (area0 + area1 - overlap_area + eps)


    def area_of(self, left_top, right_bottom):
        """Compute the areas of rectangles given two corners.
        Args:
            left_top (N, 2): left top corner.
            right_bottom (N, 2): right bottom corner.

        Returns:
            area (N): return the area.
        """
        hw = np.clip((right_bottom - left_top), a_min=0.0, a_max=1.0)
        return hw[..., 0] * hw[..., 1]
    
    def pose_postprocess(self, preds, width_radio, height_radio, filter_threshold=0.25, iou_threshold=0.45):
        preds = preds.transpose([1, 0])

        preds = preds[preds[:, 4] > filter_threshold]
        if len(preds) > 0:
            boxes = preds[:, :4]
            boxes = self.xywh2xyxy(boxes)
            scores = preds[:, 4]
            keypoints = preds[:, 5:]

            boxes, scores, keypoints = self.nms(boxes, scores, keypoints, iou_threshold=iou_threshold)

            boxes[:, 0] *= width_radio
            boxes[:, 1] *= height_radio
            boxes[:, 2] *= width_radio
            boxes[:, 3] *= height_radio

            keypoints = keypoints.reshape([-1, 17, 3])
            keypoints[:, :, 0] *= width_radio
            keypoints[:, :, 1] *= height_radio

        else:
            boxes = np.array([])
            scores = np.array([])
            keypoints = np.array([])

        return boxes, scores, keypoints
    
    def draw_kpts(self, img, kpts, shape=(640, 640), radius=5, kpt_line=True):
        """
        Plot keypoints on the image.

        Args:
            img (ndarray): Original image
            kpts (tensor): Predicted keypoints with shape [17, 3]. Each keypoint has (x, y, confidence).
            shape (tuple): Image shape as a tuple (h, w), where h is the height and w is the width.
            radius (int, optional): Radius of the drawn keypoints. Default is 5.
            kpt_line (bool, optional): If True, the function will draw lines connecting keypoints
                                    for human pose. Default is True.

        Note:
            `kpt_line=True` currently only supports human pose plotting.
        """
        nkpt, ndim = kpts.shape
        is_pose = nkpt == 17 and ndim in {2, 3}
        kpt_line &= is_pose  # `kpt_line=True` for now only supports human pose plotting
        for i, k in enumerate(kpts):
            color_k = [int(x) for x in self.kpt_color[i]] if is_pose else self.colors(i)
            x_coord, y_coord = k[0], k[1]
            if x_coord % shape[1] != 0 and y_coord % shape[0] != 0:
                if len(k) == 3:
                    conf = k[2]
                    if conf < 0.5:
                        continue
                cv2.circle(img, (int(x_coord), int(y_coord)), radius, color_k, -1, lineType=cv2.LINE_AA)

        if kpt_line:
            ndim = kpts.shape[-1]
            for i, sk in enumerate(self.skeleton):
                pos1 = (int(kpts[(sk[0] - 1), 0]), int(kpts[(sk[0] - 1), 1]))
                pos2 = (int(kpts[(sk[1] - 1), 0]), int(kpts[(sk[1] - 1), 1]))
                if ndim == 3:
                    conf1 = kpts[(sk[0] - 1), 2]
                    conf2 = kpts[(sk[1] - 1), 2]
                    if conf1 < 0.5 or conf2 < 0.5:
                        continue
                if pos1[0] % shape[1] == 0 or pos1[1] % shape[0] == 0 or pos1[0] < 0 or pos1[1] < 0:
                    continue
                if pos2[0] % shape[1] == 0 or pos2[1] % shape[0] == 0 or pos2[0] < 0 or pos2[1] < 0:
                    continue
                cv2.line(img, pos1, pos2, [int(x) for x in self.limb_color[i]], thickness=2, lineType=cv2.LINE_AA)

        return img

    def pose_detect(self, img_path):
        """
        Performs inference using an ONNX model and returns the output image with drawn detections.

        Returns:
            output_img: The output image with drawn detections.
        """
        
        # Preprocess the image data
        img_data = self.preprocess(img_path)

        # Run inference using the preprocessed image data
        outputs = self.session.run(None, {self.input_names: img_data})

        boxes, scores, keypoints = self.pose_postprocess(
            outputs[0][0],
            width_radio=self.img_width / self.input_width,
            height_radio=self.img_height / self.input_height,
        )

        for b, s, k in zip(boxes, scores, keypoints):
            b = list(map(round, b))
            self.img = self.draw_kpts(self.img, k, self.img.shape[:-1], radius=5, kpt_line=True)
            cv2.rectangle(self.img, (b[0], b[1]), (b[2], b[3]), (255, 0, 255), 2)
            cv2.putText(self.img, "Person: {:.2f}".format(s), (b[0], b[1] - 5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        return self.img


if __name__ == '__main__':
    pass
    
    


    
    

    



















    