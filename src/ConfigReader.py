#!/usr/bin/env python3
# coding=utf-8

import json
import Env
import os

def load_config(fileName) : 
    with open( fileName, 'r') as file : 
        print( 'load config file : ', fileName )
        data = json.load( file )
        # 对目标文件路径以及目标文件路径进行替换
        # 支持绝对路径和相对路径
        for index in range( 0, len( data[Env.key_template] ) ) : 
            if data[Env.key_template][index][0] != '/' : 
                data[Env.key_template][index] = os.path.dirname( fileName ) + '/' + data[Env.key_template][index]
        for index in range( 0, len( data[Env.key_output] ) ) : 
            if data[Env.key_output][index][0] != '/' : 
                data[Env.key_output][index] = os.path.dirname( fileName ) + '/' + data[Env.key_output][index]
        return data
