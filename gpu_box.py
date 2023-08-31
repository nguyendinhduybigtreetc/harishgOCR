import os
import shutil
from time import sleep
import cv2

from ultralytics import YOLO

import file_name_utils

# Load a model
model = YOLO('model/best.pt')

path_cardname = file_name_utils.CARDNAME_FOLDER
def cropbox():

    sleep(0.3)
    for filename in os.listdir(path_cardname):
        file_path = os.path.join(path_cardname, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    sleep(0.3)

    results = model.predict('tmppdf',
                            project=path_cardname, name='detect',
                            save=True,
                            save_crop=True,
                            hide_labels=True,
                            hide_conf=True,
                            line_thickness=1)  # predict on an image

    sleep(0.3)


def gpuFixSize():
    directory = 'cardimage/detect/crops/cardname'

    # iterate over files in
    # that directory
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                img = cv2.imread(f)
                height, width, channels = img.shape
                if width > 792:
                    y = 0
                    x = width - 792
                    h = height
                    w = width
                    crop_img = img[y:y + h, x:x + w]
                    cv2.imwrite(f, crop_img)

    directory = 'cardimage/detect/crops/cardnamedelete'
    if os.path.exists(directory):
        # iterate over files in
        # that directory
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                img = cv2.imread(f)
                height, width, channels = img.shape
                if width > 792:
                    y = 0
                    x = width - 792
                    h = height
                    w = width
                    crop_img = img[y:y + h, x:x + w]
                    cv2.imwrite(f, crop_img)