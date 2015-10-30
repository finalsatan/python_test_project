#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
GenDiscountCoupon.py

A python test project
Generate 200 discount coupon.

'''

import os
import sys
import random
from datetime import datetime

RandomASC = list( range( ord('0'), ord('9')+1 ) ) + list( range( ord('a'), ord('z')+1 ) ) + list( range( ord('A'), ord('Z')+1 ) )

def genDiscountCoupon( length ):
    
    coupon = ''
    genTime = ''
    for i in range(length):
        coupon += chr( random.choice( RandomASC ) )
    genTime = str( datetime.now() )
    return coupon, genTime

if __name__ == '__main__':
    
    f = open('DiscountCoupon.txt', 'w')
    for i in range(200):
        coupon,genTime = genDiscountCoupon(8)
        f.write( str(i) + ' ' + coupon + ' ' + genTime + '\n' )

    f.close()


