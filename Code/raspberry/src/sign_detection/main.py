import PIL.Image as Image
import torch
from torch.autograd import Variable
import csv

from sign_detection.model import Net
from sign_detection.data import data_jitter_hue, data_jitter_brightness, data_jitter_saturation, data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center, data_grayscale, data_transforms

LABELS_PATH = './image_detection/labels.csv'
PICS_DIR = '../captured_pics'
MODEL_PATH = './image_detection/model/model_40.pth'

labels = None
model = None


def load_model():
    global model
    state_dict = torch.load(MODEL_PATH)
    model = Net()
    model.load_state_dict(state_dict)
    model.eval()


def set_labels():
    global labels
    with open(LABELS_PATH, 'r') as f:
        reader_obj = csv.reader(f)
        labels = []
        for row in reader_obj:
            labels.append(row[1])
    labels.pop(0)


def init():
    load_model()
    set_labels()


# todo: add griding. return None if prob of a sign is extremely low.
def predict_pic(pic_name):
    global model, labels

    def pil_loader(path):
        # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                return img.convert('RGB')

    transforms = [data_transforms, data_jitter_hue, data_jitter_brightness, data_jitter_saturation,
                  data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center]

    output = torch.zeros([1, 43], dtype=torch.float32)
    with torch.no_grad():
        for i in range(0, len(transforms)):
            data = transforms[i](pil_loader(PICS_DIR + '/' + pic_name))
            data = data.view(1, data.size(0), data.size(1), data.size(2))
            data = Variable(data)
            output = output.add(model(data))
        pred = output.data.max(1, keepdim=True)[1]

    return pred, labels[pred]


def get_speed_limit(speed_limits, signs):
    if len(speed_limits) > 1:
        last_speed_lim = speed_limits[-1][1]
    else:
        last_speed_lim = 999999
    if len(signs) > 1:
        last_sign = signs[-1][1]
    else:
        last_sign = None
    
    # Check labels.csv to see the numbers
    if last_sign == 6:
        return 120
    elif last_sign == 32:
        return 120
    elif last_sign == 0:
        return min(20, last_speed_lim)
    elif last_sign == 1:
        return min(30, last_speed_lim)
    elif last_sign == 2:
        return min(50, last_speed_lim)
    elif last_sign == 3:
        return min(60, last_speed_lim)
    elif last_sign == 4:
        return min(70, last_speed_lim)
    elif last_sign == 5:
        return min(80, last_speed_lim)
    elif last_sign == 7:
        return min(100, last_speed_lim)
    elif last_sign == 8:
        return min(120, last_speed_lim)
    else:
        return last_speed_lim

