#!/usr/bin/env python
#
# Copyright 2012-2014 ihptru (Igor Popov)
#
# This file is part of OpenRA-SHP2GIF, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# shp2gif; OpenRA.Utility to get a PNG from SHP
#Usage:
#    ./shp2gif.py -s <source shp> -p <palette>
#
# ( don't forget to specify a path to OpenRA.Utility.exe in config.py )

from PIL import Image
import getopt
import os
import subprocess
import sys
import re

import images2gif
import config

_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep

_palettes = os.listdir('palette')
palettes = []
for item in _palettes:
    if re.search('^\.', item):
        continue
    palettes.append(item)

try:
    optlist,  args = getopt.getopt(sys.argv[1:], 's:p:')
except getopt.GetoptError, err:
    print err
    exit()

if optlist == []:
    print("Incorrect options!")
    print("Usage:")
    print("   ./shp2gif -s <source shp> -p <palette>")
    print("Where palette is:")
    for item in palettes:
        print("    "+item)
    exit(2)

for  i in range(len(optlist)):
    if optlist[i][0] == "-s":
        source_shp = optlist[i][1]
    if optlist[i][0] == "-p":
        palette = optlist[i][1]

using_dir = os.path.dirname(source_shp) + os.sep
try:
    os.mkdir(using_dir + "pngs")
except:
    pass
os.chdir(using_dir + "pngs")

# get PNG from SHP using OpenRA.Utility
subprocess.Popen(["mono", config.openra_path, "--png", source_shp, _PATH+"palette/"+palette]).wait()
print("created png form shp...")

shpdir = os.listdir(using_dir + "pngs")
frames = 0
for fn in shpdir:
    if fn.split('.')[1] == "png":
        frames = frames + 1

area = []
current_pos = 0
for frame in range(frames):
    cur_frame = str(frame).rjust(4,'0')
    img_path = using_dir + "pngs/" + os.path.basename(source_shp).split('.shp')[0] + "-" + cur_frame + ".png"
    im = Image.open(img_path)
    size = im.size
    # coords: left, bottom, right, top
    box = (current_pos, 0, current_pos+size[0], size[1])
    copy_im = im.copy()
    area.append(copy_im.crop(box))

images2gif.writeGif(_PATH+"preview.gif", area, duration=0.5, loops=0, dither=0)
print("Path to generated GIF: "+_PATH+"preview.gif")
