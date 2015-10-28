#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
GenerateRPN.py

A python test project
Generate reverse polish notation for a given math notation.

Example:

(a+b)*c => ab+c*

'''

import os, sys


operatorPiority = { '+':1, '-':1, '*':2, '/':2 }

def linkList( l ):
    retStr = ''
    for s in l:
        retStr += s
    return retStr


def generateRPN( mathNotation ):
    #print( mathNotation )


    stackOperator = [];
    stackNum = [];

    for s in mathNotation:
        #print('Now:',s)
        if s=='(':
            stackOperator.append(s)
        elif s==')':
            while stackOperator[-1] != '(':
                stackNum.append( stackOperator[-1] )
                stackOperator.pop()
            stackOperator.pop()
        elif s in operatorPiority:
            if len(stackOperator)==0 or stackOperator[-1] == '(':
                stackOperator.append(s)
            else :
                while operatorPiority[stackOperator[-1]] >= operatorPiority[s]:
                    stackNum.append( stackOperator[-1] )
                    stackOperator.pop()
                stackOperator.append(s)
        else :
            stackNum.append(s)

    str1 = linkList(stackOperator)
    str2 = linkList(stackNum)
    
    return str2 + str1[::-1] 


if __name__ == '__main__':
    while True:
        mathNotation = input('Please input the mathNotation, if wanna quit, input \'quit\'.\n')
        if mathNotation=='quit':
            break
        else:
            print(generateRPN( mathNotation ))


