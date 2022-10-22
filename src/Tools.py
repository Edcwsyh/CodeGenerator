#!/usr/bin/env python3
# coding=utf-8

from enum import Enum

class Color : 
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4

def get_color_txt( color ) : 
    switcher = {
        Color.RED : "\033[31m", 
        Color.GREEN : "\033[32m", 
        Color.YELLOW : "\033[33m", 
        Color.BLUE : "\033[34m", 
    }
    return switcher.get( color )

def print_color(string, color) : 
    newString = get_color_txt( color ) + string + "\033[0m"
    print( newString )
