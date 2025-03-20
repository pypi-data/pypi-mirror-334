from PIL import Image
import os
import sys
import argparse


def convert_images(input_path, initial_extension, final_extension):
	"""
	Converts all images in a folder (single layer) that are ```initial_extension``` format, to ```final_extension```.

	### Parameters:
	- ```input_path```: The folder to convert.
	- ```initial_extension```: The image type to convert.
	- ```final_extension```: The image type to convert to.
	"""

	# Prefixes extensions with dots, of not already.
	if not final_extension.startswith("."): final_extension = "." + final_extension 
	if not initial_extension.startswith("."): initial_extension = "." + initial_extension 

	# Get images of correct type in folder
	Images = sorted([f for f in os.listdir(input_path) if f.lower().endswith(initial_extension.lower())])

	# Abort if no images found.
	if len(Images) < 1:
		print("No suitable images found.")
		return

	# Create output folder.
	outputPath = os.path.join(input_path, "Output")
	os.makedirs(outputPath, exist_ok=True)

	for image in Images:
		withoutExtension = image.partition('.')[0] 
		im = Image.open(os.path.join(input_path, image))
		im.save(os.path.join(outputPath, f"{withoutExtension}{final_extension}"), final_extension[1:].upper())
	
	print("Complete!\n")


def _script():
	"""	Will be called by package if command issued via terminal."""

	if len(sys.argv) == 3:
		folderPath = os.getcwd()
		convert_images(folderPath, sys.argv[1], sys.argv[2])
	else:
		print("Expected two arguments (initial_extension, final_extension)")
