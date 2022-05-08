from glob import glob
from tqdm import tqdm
import os
import PIL.Image as Image
import torch
from torch.autograd import Variable
import csv

from model import Net
from data import data_jitter_hue, data_jitter_brightness, data_jitter_saturation, data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center, data_grayscale, data_transforms

LABELS_PATH = 'labels.csv'
labels = None


def set_labels():
    global labels
    with open(LABELS_PATH, 'r') as f:
        reader_obj = csv.reader(f)
        labels = []
        for row in reader_obj:
            labels.append(row[1])
    labels.pop(0)


def predict_pics():
    state_dict = torch.load('model/model_40.pth')
    model = Net()
    model.load_state_dict(state_dict)
    model.eval()

    pics_dir = 'data/pics'

    def pil_loader(path):
        # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                return img.convert('RGB')

    transforms = [data_transforms, data_jitter_hue, data_jitter_brightness, data_jitter_saturation,
                  data_jitter_contrast, data_rotate, data_hvflip, data_shear, data_translate, data_center]
    output_file = open('data/pred.csv', 'w')
    output_file.write('Filename,ClassId\n')

    for f in tqdm(os.listdir(pics_dir)):
        output = torch.zeros([1, 43], dtype=torch.float32)
        with torch.no_grad():
            for i in range(0, len(transforms)):
                data = transforms[i](pil_loader(pics_dir + '/' + f))
                data = data.view(1, data.size(0), data.size(1), data.size(2))
                data = Variable(data)
                output = output.add(model(data))
            pred = output.data.max(1, keepdim=True)[1]
            file_id = f
            output_file.write('%s,%s\n' % (file_id, labels[pred]))
            print(f'')

    output_file.close()


def main():
    set_labels()
    predict_pics()


if __name__ == '__main__':
    main()
