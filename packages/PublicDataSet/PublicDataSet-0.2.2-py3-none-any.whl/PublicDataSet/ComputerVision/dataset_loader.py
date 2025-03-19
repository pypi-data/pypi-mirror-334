import os
from PIL import Image
import numpy as np

def load_images_from_directory(directory):
    images = []
    for filename in os.listdir(directory):
        img_path = os.path.join(directory, filename)
        img = Image.open(img_path).convert("RGB")
        img_array = np.array(img)
        images.append(img_array)
    return images

def load_dataset(train_path, test_path):
    train_images = load_images_from_directory(train_path)
    test_images = load_images_from_directory(test_path)
    return train_images, test_images