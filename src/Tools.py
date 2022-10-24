#!/usr/bin/env python3
# coding=utf-8

from enum import Enum

class Color : 
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4

class PrintColorState : 
    ENABLE = 1      # 开启
    DISABLE = 2     # 关闭

# 是否开启颜色打印, 若输出终端异常, 请关闭该选项
envPrintColorState = PrintColorState.ENABLE

def get_color_txt( color ) : 
    switcher = {
        Color.RED : "\033[31m", 
        Color.GREEN : "\033[32m",       
        Color.YELLOW : "\033[33m", 
        Color.BLUE : "\033[34m", 
    }
    return switcher.get( color )

def print_color(string, color) : 
    if envPrintColorState == PrintColorState.ENABLE : 
        newString = get_color_txt( color ) + string + "\033[0m"
        print( newString )
    else : 
        print( string )
