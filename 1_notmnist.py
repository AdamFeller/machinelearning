# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 14:51:55 2016

@author: fella
"""

# These are all the modules we'll be using later. Make sure you can import them
# before proceeding further.
import matplotlib.pyplot as plt
import numpy as np
import os
import tarfile
import urllib
import sys
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
#import cPickle as pickle
import pickle as pickle

url = 'http://yaroslavvb.com/upload/notMNIST/'

def maybe_download(filename, expected_bytes):
  """Download a file if not present, and make sure it's the right size."""
  if not os.path.exists(filename):
    filename, _ = urllib.request.urlretrieve(url + filename, filename)
  statinfo = os.stat(filename)
  if statinfo.st_size == expected_bytes:
    print ('Found and verified', filename)
  else:
    raise Exception(
      'Failed to verify' + filename + '. Can you get to it with a browser?')
  return filename

#train_filename = maybe_download('notMNIST_large.tar.gz', 247336696)
test_filename = maybe_download('notMNIST_small.tar.gz', 8458043)

num_classes = 10

def extract(filename):
  tar = tarfile.open(filename)
  root = os.path.splitext(os.path.splitext(filename)[0])[0]  # remove .tar.gz
  if not os.path.isdir(root):
    print ('Extracting data for %s. This may take a while. Please wait.' % root)
    sys.stdout.flush()
    tar.extractall()
    tar.close()
  data_folders = [os.path.join(root, d) for d in sorted(os.listdir(root)) if d != '.DS_Store']
  if len(data_folders) != num_classes:
    raise Exception(
      'Expected %d folders, one per class. Found %d instead.' % (
        num_classes, len(data_folders)))
  print (data_folders)
  return data_folders
  
#train_folders = extract(train_filename)
test_folders = extract(test_filename)


image_size = 28  # Pixel width and height.
pixel_depth = 255.0  # Number of levels per pixel.


def load(data_folders, min_num_images, max_num_images):
  dataset = np.ndarray(
    shape=(max_num_images, image_size, image_size), dtype=np.float32)
  labels = np.ndarray(shape=(max_num_images), dtype=np.int32)
  label_index = 0
  image_index = 0
  for folder in data_folders:
    print (folder)
    for image in os.listdir(folder):
      if image_index >= max_num_images:
        raise Exception('More images than expected: %d >= %d' % (
          image_index, max_num_images))
      image_file = os.path.join(folder, image)
      try:
        image_data = (ndimage.imread(image_file).astype(float) -
                      pixel_depth / 2) / pixel_depth
        if image_data.shape != (image_size, image_size):
          raise Exception('Unexpected image shape: %s' % str(image_data.shape))
        dataset[image_index, :, :] = image_data
        labels[image_index] = label_index
        image_index += 1
      except IOError as e:
        print ('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')
    label_index += 1
  num_images = image_index
  dataset = dataset[0:num_images, :, :]
  labels = labels[0:num_images]
  if num_images < min_num_images:
    raise Exception('Many fewer images than expected: %d < %d' % (
        num_images, min_num_images))
  print ('Full dataset tensor:', dataset.shape)
  print ('Mean:', np.mean(dataset))
  print ('Standard deviation:', np.std(dataset))
  print ('Labels:', labels.shape)
  return dataset, labels
  
#train_dataset, train_labels = load(train_folders, 450000, 550000)
test_dataset, test_labels = load(test_folders, 18000, 20000)

import string
from random import randint
i = randint(0,len(test_dataset))

def letterVal(number):
    letters = list(string.ascii_lowercase[:len(np.unique(test_labels))])
    return letters[number]

chartTitle = ('letter :', letterVal(test_labels[i]), 'Index :', i)
plt.imshow(test_dataset[i])
plt.suptitle(chartTitle)
plt.show()

from collections import Counter
tally=Counter()

for elem in test_labels:
    tally[elem] += 1
#np.random.seed(133)
#def randomize(dataset, labels):
#  permutation = np.random.permutation(labels.shape[0])
#  shuffled_dataset = dataset[permutation,:,:]
#  shuffled_labels = labels[permutation]
#  return shuffled_dataset, shuffled_labels
#train_dataset, train_labels = randomize(train_dataset, train_labels)
#test_dataset, test_labels = randomize(test_dataset, test_labels)
