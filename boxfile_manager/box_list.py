from re import compile
from os import listdir, curdir

BOX_PATTERN = compile(r'^hypernode.*.release-.*.box$')


def list_boxes():
    dir_files = listdir(curdir)
    return filter(BOX_PATTERN.match, dir_files)
