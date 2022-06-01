import PIL.Image as Image
import torch
from torch.autograd import Variable
import csv

from sign_detection.model import Net
from sign_detection.data import data_jitter_hue, data_jitter_brightness, data_jitter_saturation, data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center, data_grayscale, data_transforms

LABELS_PATH = './sign_detection/labels.csv'
PICS_DIR = '../captured_pics/'
MODEL_PATH = './sign_detection/model/model_40.pth'
# Probability threshold to accept a predicted sign in a picture
GRID_INIT_SIZE = 30
GRID_SIZE_MUL = 1.2
GRID_STEP_TO_SIZE_RATIO = 0.2
PROB_THRESHOLD = 0.95
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


# todo: add griding. return None if prob of a sign is low.
def predict_sign(pic_name):
    global model, labels

    def load_pic(path):
        with Image.open(path) as img:
            img.load()
            return img.convert('RGB')

    def eval_pic(pic: Image):
        output = torch.zeros(size=[1, 43], dtype=torch.float32)
        for i in range(0, len(transforms)):
            data = transforms[i](pic)
            data = data.view(1, data.size(0), data.size(1), data.size(2))
            data = Variable(data)
            output = output.add(model(data))
        # Remove unimportant classes in a crude way
        for i in [e for e in list(range(43)) if e not in [0, 1, 2, 3, 4, 5, 7, 8]]:
            output.data[0][i] = -999999
        # print(output.data)
        prediction = output.data.max(1, keepdim=True)        
        pred = int(prediction[1])
        prob = 1 + float(prediction[0])
        return pred, prob, labels[pred]

    def process_pic(pic: Image):
        img = Image.new('RGB', (pic.size))
        for x in range(pic.width):
            for y in range(pic.height):
                r, g, b = pic.getpixel((x, y))
                if r > 50 and g < 200 and b < 200:
                    img.putpixel((x, y), (b, g, r))
                else:
                    img.putpixel((x, y), (r, g, b))
        return img

    transforms = [data_transforms, data_jitter_hue, data_jitter_brightness, data_jitter_saturation,
                  data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center]

    pic = load_pic(PICS_DIR + pic_name)
    pic = process_pic(pic)
    pic.show()
    grid_size = GRID_INIT_SIZE
    grid_step = int(grid_size * GRID_STEP_TO_SIZE_RATIO)
    while True:
        for y in range(0, pic.height - grid_size, grid_step):
            for x in range(0, pic.width - grid_size, grid_step):
                print(x, y)
                cropped_pic = pic.crop((x, y, x + grid_size, y + grid_size))
                pred_label, prob, name = eval_pic(cropped_pic)
                if prob > PROB_THRESHOLD:
                    cropped_pic.show()
                    return pred_label, prob, name
        grid_size = int(grid_size * GRID_SIZE_MUL)
        grid_step = int(grid_size * GRID_STEP_TO_SIZE_RATIO)
        if grid_size > pic.width or grid_size > pic.height:
            break


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
        return 999999
    elif last_sign == 32:
        return 999999
    elif last_sign == 0:
        return 20
    elif last_sign == 1:
        return 30
    elif last_sign == 2:
        return 50
    elif last_sign == 3:
        return 60
    elif last_sign == 4:
        return 70
    elif last_sign == 5:
        return 80
    elif last_sign == 7:
        return 100
    elif last_sign == 8:
        return 120
    else:
        return last_speed_lim
