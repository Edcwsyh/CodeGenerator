#!/usr/bin/env python3
# coding=utf-8

import ConfigReader
import sys
import Generator

generator = Generator.Generator()

if __name__ == "__main__" :
    # __判断传入参数
    if len( sys.argv ) != 2 :
        print( 'Usage : ',sys.argv[0],' [config file]' )
        exit()
    # 读取配置文件
    generator.read_config( sys.argv[1] )
    # 生成代码
    generator.generate()
    
