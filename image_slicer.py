 #!/usr/bin/env python
#encoding=UTF-8

__author__ = "MopperWhite"
__copyright__ = "Copyright 2016, MopperWhite"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "mopperwhite@gmail.com"
__status__ = "Development"

import os, sys
import numpy as np
import Image

def slice_image(filename, min_hight_g = 1, max_hight_g = 2):
    image = Image.open(filename)
    width, height = image.size

    low_h = int(width * min_hight_g)
    high_h = int(width * max_hight_g)

    row_var = [np.var( map(np.array, (
                image.getpixel((j, i))
                for j in xrange(width))
            ), axis = 0)
        for i in xrange(height)]
    slicable_rows = [ i
        for i, vec in zip(xrange(height), row_var)
        if np.linalg.norm(vec) < 1e-2 ]

    cont_ranges = []
    start_row = None
    last_row = None
    for r in slicable_rows:
        if start_row is None:
            start_row = r
        elif r - last_row > 1:
            cont_ranges.append((start_row, last_row))
            start_row = r
        last_row = r
    if start_row is not None:
        cont_ranges.append((start_row, last_row))

    cont_range_centers = [(s+e)/2 for s, e in cont_ranges]

    parts = []
    last_row = 0
    for r in cont_range_centers:
        parts.append((last_row, r))
        last_row = r
    parts.append((last_row, height - 1))

    start_row = None
    img_parts = []
    for start, end in parts:
        if start_row is None:
            start_row = start
        part_height = end - start_row 
        if low_h <= part_height  <= high_h or ( part_height > high_h and start_row == start ):
            img_parts.append(image.crop((0, start_row, width, end)))
            start_row = None
        elif part_height > high_h:
            img_parts.append(image.crop((0, start_row, width, start)))
            start_row = start
    img_parts.append(image.crop((0, start_row, width, height - 1)))
    return img_parts

def slice_and_save(filename, min_hight_g = 1, max_hight_g = 2):
    base_n, ext_n = os.path.splitext(filename)
    img_parts = slice_image(filename, min_hight_g, max_hight_g)
    for i, img in zip(xrange(len(img_parts)), img_parts):
        img.save("%s-%d%s"%(base_n, i, ext_n))
    return ["%s-%d%s"%(base_n, i, ext_n) for i in xrange(len(img_parts))]

if __name__ == '__main__':
    slice_and_save(sys.argv[1] if len(sys.argv) > 1 else "in.jpg")
