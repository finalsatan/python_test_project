#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
AddNum2Pic.py

A python test project
Add a number to a picture.

'''

import os, sys
from PIL import Image, ImageFont, ImageDraw

def addNum2Pic( picPath, num):
    print( picPath )
    print( num )

    pic = Image.open( picPath )
    w, h = pic.size
    fontsize = min( w, h ) // 6
    x = w - fontsize
    draw = ImageDraw.Draw( pic )
    font = ImageFont.truetype( "/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize )
    draw.text( ( x, 0 ), str(num), font=font, fill="red" )
    del draw
    pic.save("newHead.jpg")
    pic.show()

if __name__ == '__main__':
    addNum2Pic( 'head.jpg', 8 );


