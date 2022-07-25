#!/usr/bin/env python3
# coding=utf-8

from colorama import Style

def print_color(string, color) : 
    print( color + string + Style.RESET_ALL )
