import gxcv

import os
import cv2
import shutil
import numpy as np
from PIL import Image




if __name__ == '__main__':
    print(gxcv.__version__)

    """ ======== CV ======== """
    # iou = gxcv.cv.utils.cal_iou(bbx1=[0, 0, 10, 10], bbx2=[2, 2, 12, 12])
    # gxcv.cv.utils.extract_one_gif_frames(gif_path="")
    # gxcv.cv.utils.extract_one_video_frames(video_path="", gap=5)
    # gxcv.cv.utils.extract_videos_frames(base_path="", gap=5, save_path="")
    # gxcv.cv.utils.convert_to_jpg_format(data_path="")
    # gxcv.cv.utils.convert_to_png_format(data_path="")
    # gxcv.cv.utils.convert_to_gray_image(data_path="")
    # gxcv.cv.utils.convert_to_binary_image(data_path="", thr_low=88)
    # gxcv.cv.utils.crop_image_according_labelbee_json(data_path="", crop_ratio=(1, 1.2, 1.5, ))
    # gxcv.cv.utils.crop_ocr_rec_img_according_labelbee_det_json(data_path="")
    # gxcv.cv.utils.crop_image_according_yolo_txt(data_path="", CLS=(0, ), crop_ratio=(1.0, ))  # 1.0, 1.1, 1.2, 1.5, 2.0, 2.5, 3.0
    # gxcv.cv.utils.random_crop_gen_cls_negative_samples(data_path="", random_size=(196, 224, 256, 288, 384), randint_low=1, randint_high=4, hw_dis=100, dst_num=1000)
    # gxcv.cv.utils.seg_object_from_mask(base_path="")






