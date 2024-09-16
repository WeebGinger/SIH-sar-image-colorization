import os
import csv
from pathlib import Path
from src.components.data_retriever import label_images

root_directory = '/Users/ginger/Developer/python/Projects/sar-colorization/Data/v_2/agri'  # Current directory, change this if your folders are elsewhere
output_csv = 'image_labels.csv'

label_images(root_directory, output_csv)
