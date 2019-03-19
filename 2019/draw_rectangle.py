# Code to parse Amazon Mechanical Turk output.
# Input: Json output from Mechanical Turk.
# Output: Images with annotations.
# Author : @Jayant Gupta
# Date : 03/18/2019

#MIT License

# Copyright (c) [2019] [Jayant Gupta]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw
import numpy as np

import csv
import re
import ast

with open("mTurk.csv") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	flag = 0
	for row in csv_reader:
#		print(row)
		if flag == 0:
			file_index = row.index('Input.image_url')
			polygon_data_index = row.index('Answer.annotatedResult.polygons')
			flag = 1
		else:
			print("Processing: " + row[file_index].split('/')[-1])
			image_name = row[file_index].split('/')[-1]

		# Open the image
			image = Image.open(image_name)
		# Draw on top of the image
			draw = ImageDraw.Draw(image)
		# Draw rectangle on the image.
		# Read the polygon
			polygon_data = row[polygon_data_index]

		# Use regex to extract the coordinates.
			regex = r"\{(.*?)\}"
			print(polygon_data)
			try:
				polygon_data = polygon_data.split("[")[2]
			except:
				continue
			matches = re.finditer(regex, polygon_data, re.MULTILINE | re.DOTALL)
			points = [] # List to store the points as dictionary item.
			for matchNum, match in enumerate(matches):
				for groupNum in range(0, len(match.groups())):
					points.append(match.group(groupNum))
			point_tuples = [] # List to store the points as tuple.
			switch = 0
			for point in points:
			  point = ast.literal_eval(point)
			  point_tuples.append(tuple((point['x'], point['y'])))
			# Draw the polygon around the urban garden.
			draw.polygon(point_tuples)

		# Display the image
			image.show()
			input("Press enter to continue...")
