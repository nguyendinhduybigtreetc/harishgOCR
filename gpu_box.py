import os
import shutil
from time import sleep

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