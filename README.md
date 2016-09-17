# simple_image_slicer

A python script for slicing a very high image to several parts. In each part, only few polygon cut off. And the height of each part will be close to the width of the original image.

用来切微博长图和各种奇怪漫画的脚本。

会选择整行都是同一种颜色的行分割。

每块的长度会尽量控制在图片宽度的一到两倍。

## Sample

### As a command line script

```Bash
python image_slicer.py a_very_high_image_which_might_be_from_weibo.png
```

### As a python module

```Python
import image_slicer

image_slicer.slice_image('in.png')

# Some Image objects will be returned.

image_slicer.slice_and_save('in.png')

# In this way, the parts above will be saved with numbers. And the names of files will get returned.
```

## Dependences

* Python2.7
* PIL
* numpy
