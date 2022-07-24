#!/usr/bin/env python3
# coding=utf-8

import os

def load_template( fileName ) : 
    with open( fileName, 'r' ) as file : 
        print( 'load template file : ', fileName )
        return file.readlines()
    
