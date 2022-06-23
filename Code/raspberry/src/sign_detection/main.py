import PIL.Image as Image
import torch
from torch.autograd import Variable
import csv
import random

from sign_detection.model import Net
from sign_detection.data import data_jitter_hue, data_jitter_brightness, data_jitter_saturation, data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center, data_grayscale, data_transforms

# Paths
LABELS_PATH = './sign_detection/labels.csv'
PICS_DIR = '../captured_pics/'
MODEL_PATH = './sign_detection/model/model_40.pth'

# Grid information
GRID_INIT_SIZE = 30
GRID_SIZE_MUL = 1.2
GRID_STEP_TO_SIZE_RATIO = 0.2

# Probability threshold to accept a predicted sign in a picture
PROB_THRESHOLD = 0.95

ACCEPTED_SIGN_LABELS = [0, 1, 2, 3, 4, 5, 7, 8]
RED_THRESHOLD = 0.05

labels = None
model = None


# Loads pre-trained model from model_40.pth
def load_model():
    global model
    state_dict = torch.load(MODEL_PATH)
    model = Net()
    model.load_state_dict(state_dict)
    model.eval()


# Loads labels from labels.csv
def set_labels():
    global labels
    with open(LABELS_PATH, 'r') as f:
        reader_obj = csv.reader(f)
        labels = []
        for row in reader_obj:
            labels.append(row[1])
    labels.pop(0)


# Initializes sign_detection module
def init():
    load_model()
    set_labels()


# Finds a traffic sign in image file with name PIC_NAME and returns the sign's label, probability and name.
# Returns None if no sign with high enough probability was found.
def predict_sign(pic_name):
    global model, labels

    # Loads image in PATH
    def load_pic(path):
        with Image.open(path) as img:
            img.load()
            return img.convert('RGB')

    # Returns sign detected in PIC
    def eval_pic(pic: Image):
        output = torch.zeros(size=[1, 43], dtype=torch.float32)
        for i in range(0, len(transforms)):
            data = transforms[i](pic)
            data = data.view(1, data.size(0), data.size(1), data.size(2))
            data = Variable(data)
            output = output.add(model(data))
        # Remove unimportant classes in a crude way
        for i in [e for e in list(range(43)) if e not in ACCEPTED_SIGN_LABELS]:
            output.data[0][i] = -999999
        prediction = output.data.max(1, keepdim=True)
        pred = int(prediction[1])
        prob = 1 + float(prediction[0])
        return pred, prob, labels[pred]

    # Converts red pixels to blue in PIC.
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

    # Checks if atleast a specified percentage of PIC's pixels are red.
    def does_have_red(pic: Image):
        red_cnt = 0
        for x in range(pic.width):
            for y in range(pic.height):
                r, g, b = pic.getpixel((x, y))
                if r > 50 and g < 200 and b < 200:
                    red_cnt += 1

        pic_size = pic.width * pic.height
        return red_cnt / pic_size > RED_THRESHOLD

    transforms = [data_transforms, data_jitter_hue, data_jitter_brightness, data_jitter_saturation,
                  data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center]

    orig_pic = load_pic(PICS_DIR + pic_name)
    pic = process_pic(orig_pic)
    grid_size = GRID_INIT_SIZE
    grid_step = int(grid_size * GRID_STEP_TO_SIZE_RATIO)
    # Iterate over grids to find a sign.
    while True:
        for y in range(0, pic.height - grid_size, grid_step):
            for x in range(0, pic.width - grid_size, grid_step):
                # Skip the grid if orginal pic doesn't have enough red pixels.
                orig_cropped_pic = orig_pic.crop(
                    (x, y, x + grid_size, y + grid_size))
                if not does_have_red(orig_cropped_pic):
                    continue

                # Check grid to find sign.
                cropped_pic = pic.crop((x, y, x + grid_size, y + grid_size))
                pred_label, prob, name = eval_pic(cropped_pic)
                if prob > PROB_THRESHOLD:
                    return pred_label, prob, name

        # Update grid attributes.
        grid_size = int(grid_size * GRID_SIZE_MUL)
        grid_step = int(grid_size * GRID_STEP_TO_SIZE_RATIO)
        if grid_size > pic.width or grid_size > pic.height:
            break

    return None


# Calculates speed limit according to the last sign.
def get_speed_limit(signs):
    # If signs has no elements, we return None
    if len(signs) > 0:
        last_sign = signs[-1][1]
    else:
        return None

    # NOTE: Check labels.csv to see the numbers
    if last_sign == 0:
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
        assert 1 == 2  # Should not reach here


# Generates a random traffic sign with the probability of RESULT_PROB everytime it is called.
def get_random_sign(result_prob):
    global labels

    labels_to_choose = [-1] + ACCEPTED_SIGN_LABELS
    miss_prob = 1 - result_prob
    sign_prob = result_prob / len(ACCEPTED_SIGN_LABELS)
    weights = [miss_prob] + [sign_prob for _ in ACCEPTED_SIGN_LABELS]
    selected_label = random.choices(labels_to_choose, weights, k=1)[0]
    if selected_label == -1:
        return None
    else:
        return selected_label, 100.0, labels[selected_label]
