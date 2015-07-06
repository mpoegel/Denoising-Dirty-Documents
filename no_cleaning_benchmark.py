# ------------------------------------------------------------------------------
# Author: Matt Poegel
# Date:   2015-07-04
#
# Description: Establish a benchmark by not cleaning the files at all
# ------------------------------------------------------------------------------

import os
from PIL import Image
import numpy as np
import pandas as pd


def image_df_from_array(image_array, image_number):
	size = image_array.shape
	image_df = pd.DataFrame([(x,y) for x in range(size[0]) for y in range(size[1])],
		columns = ['row', 'col'])
	image_df['row_offset'] = image_df['row'] + 1
	image_df['col_offset'] = image_df['col'] + 1
	image_df['pixel_value'] = image_array[image_df.row, image_df.col]
	image_df['value'] = image_df['pixel_value'] / 255
	image_df['id'] = image_number + '_' + image_df.row_offset.astype('str') + \
	 	'_' + image_df.col_offset.astype('str')
	return image_df[['id', 'value']]

def image_df_from_path(test_image_path):
	print('Working image ' + test_image_path)
	image_number = os.path.basename(test_image_path).split('.')[0]
	image_array = np.asarray(Image.open(test_image_path))
	return image_df_from_array(image_array, image_number)

def process_images(test_images_dir, submission_file, num_files=None):
	test_image_paths = [os.path.join(test_images_dir, relative_path) for
		relative_path in os.listdir(test_images_dir)]
	if (num_files):
		test_image_paths = test_image_paths[0:num_files]
	for (i, test_image_path) in enumerate(test_image_paths):
		df = image_df_from_path(test_image_path)
		if (i == 0):
			df.to_csv(submission_file, index=False)
		else:
			df.to_csv(submission_file, index=False, header=False)

# ------------------------------------------------------------------------------
if (__name__ == '__main__'):
	with open('./submissions/no_cleaning_benchmark.csv', 'w') as submission_file:
		process_images('./test/', submission_file)
