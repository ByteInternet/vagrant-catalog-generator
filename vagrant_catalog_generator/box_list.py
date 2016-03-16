from re import compile
from os import listdir


def list_boxes(box_name, boxfiles_directory):
    box_pattern = compile(r'^{}.*.release-.*.box$'.format(box_name))
    dir_files = listdir(boxfiles_directory)
    return filter(box_pattern.match, dir_files)
