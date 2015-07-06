# ------------------------------------------------------------------------------
# Author: Matt Poegel
# Date:   2015-07-05
#
# Description: Clean the images using a threshold technique
# ------------------------------------------------------------------------------

import os
from PIL import Image
import numpy as np
import pandas as pd
import random as r
from sklearn.metrics import mean_squared_error
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r.seed(12)

def histogram_from_image(image_df, id_num):
	print('Creating Histogram for ' + id_num)
	num_bins = 50
	n, bins, patches = plt.hist(image_df.value, num_bins)
	median = np.median(image_df.value)
	std = np.std(image_df.value)
	plt.axvline(median, color='r', ls='--', lw=2, alpha=0.5)
	plt.axvline(median - std, color='g', ls='--', lw=2, alpha=0.5)
	plt.xlabel('Pixel Value')
	plt.ylabel('Pixel Count')
	plt.savefig('./figures/histo_' + id_num + '.png', bbox_inches='tight')
	plt.close()

def threshold_model(train_dir, train_clean_dir):
	print('Creating Model')
	# make an array of all the files
	train_paths = [os.path.join(train_dir, relative_path) for
		relative_path in os.listdir(train_dir)]
	train_clean_paths = [os.path.join(train_clean_dir, relative_path) for
		relative_path in os.listdir(train_clean_dir)]
	# divide the training set into a train set and an eval set
	r.shuffle(train_paths)
	div = int(len(train_paths) * 0.90)
	train_set_paths = train_paths[:div]
	test_set_paths = train_paths[div:]
	# create the model using the train set
	medians = []
	for path in train_set_paths:
		df = image_df_from_path(path)
		medians.append(np.median(df.value) - np.std(df.value))
	t = np.median(medians)
	# test the model on the subset
	error = 0
	for path in test_set_paths:
		df = image_df_from_path(path)
		df.value[ df.value >= t ] = 1
		clean_path = path.replace(train_dir, train_clean_dir)
		clean_df = image_df_from_path(clean_path)
		rmse = mean_squared_error(df.value, clean_df.value) ** 0.5
		error += rmse
		histogram_from_image(df, 'train_orig')
		histogram_from_image(clean_df, 'train_cleaned_by_model')
		break;
	error /= len(test_set_paths)
	return t, error

def image_df_from_array(image_array, image_number, ids=False):
	size = image_array.shape
	image_df = pd.DataFrame([(x,y) for x in range(size[0]) for y in range(size[1])],
		columns = ['row', 'col'])
	image_df['row_offset'] = image_df['row'] + 1
	image_df['col_offset'] = image_df['col'] + 1
	image_df['pixel_value'] = image_array[image_df.row, image_df.col]
	image_df['value'] = image_df['pixel_value'] / 255
	if (ids):
		image_df['id'] = image_number + '_' + image_df.row_offset.astype('str') + \
		 	'_' + image_df.col_offset.astype('str')
		return image_df[['id', 'value']]
	else:
		return image_df

def image_df_from_path(test_image_path, ids=False):
	print('Working image ' + test_image_path)
	image_number = os.path.basename(test_image_path).split('.')[0]
	image_array = np.asarray(Image.open(test_image_path))
	return image_df_from_array(image_array, image_number, ids)

def process_images(test_images_dir, t, submission_file, num_files=None):
	test_image_paths = [os.path.join(test_images_dir, relative_path) for
		relative_path in os.listdir(test_images_dir)]
	if (num_files):
		test_image_paths = test_image_paths[0:num_files]
	for (i, test_image_path) in enumerate(test_image_paths):
		df = image_df_from_path(test_image_path, ids=True)
		df.value[ df.value >= t] = 1
		if (i == 0):
			df.to_csv(submission_file, index=False)
		else:
			df.to_csv(submission_file, index=False, header=False)

# ------------------------------------------------------------------------------
if (__name__ == '__main__'):

	# df_dirty = image_df_from_path('./train/2.png')
	# df_clean = image_df_from_path('./train_cleaned/2.png')
	# histogram_from_image(df_dirty, '2_dirty')
	# histogram_from_image(df_clean, '2_clean')

	t, error = threshold_model('./train/', './train_cleaned/')
	print('threshold = ' + str(t))
	print('error = ' + str(error))

	with open('./submissions/threshold.csv', 'w') as submission_file:
		process_images('./test/', t, submission_file)
