#!/usr/bin/env python3
# coding=utf-8

import ConfigReader
import TemplateReader
import Env
import re
import os
import datetime
from Tools import print_color
from Tools import Color

class Generator : 
    def __init__( self ) : 
        self.inputBuf = list()
        self.outputBuf = str()
        self.config = dict()
        self.file = object()

    ##
    # @description debug_info 调试函数
    #
    # @return 
    def debug_info( self ) : 
        print( 'config : ',self.config )
        print( 'input buffer : ',self.inputBuf )
        print( 'output buffer : ',self.outputBuf )

    ##
    # @description read_config 读取配置文件
    #
    # @param fileName 文件路径
    #
    # @return 
    def read_config( self, fileName ) : 
        self.config = ConfigReader.load_config( fileName )

    ##
    # @description read_template 读取模板文件
    #
    # @return 
    def read_template( self, index ) : 
        if self.config is None : 
            print_color( 'The config is None! ', Color.RED )
            exit()
        self.inputBuf = TemplateReader.load_template( self.config[Env.key_template][index] )

    ##
    # @description generate_line 对该行的每一个tag进行替换
    #
    # @param line 输入行
    # @param paramIndex 参数索引
    #
    # @return 
    def generate_line( self, line, paramIndex ) :
        if re.search( "\${.*}", line ) :
            # 获取该行的tag列表
            res = re.compile( r'\${(.*?)[}]', re.S)
            tag = re.findall( res, line )[0]
            # 获取该tag的参数列表 
            paramList = self.config[Env.key_param_list][tag]
            if paramList is None or len( paramList ) == 0: 
                # 为空直接返回
                return ""
            fullTag = '${' + tag + '}'
            # 对tag进行替换
            # 若元素不足, 则取最后一个
            if len( paramList ) > paramIndex : 
                line = line.replace( fullTag, paramList[paramIndex] )
            else :
                line = line.replace( fullTag, paramList[-1] )
            # 递归, 对第2个tag进行替换
            return self.generate_line( line, paramIndex )
        return line

    ##
    # @description get_block 获取一个代码块
    #
    # @param it 调用方的循环迭代器
    #
    # @return 
    def get_block( self, it ) : 
        # 将代码块拼接成行
        block = str()
        for line in it : 
            if re.search( Env.key_block, line ) : 
                break
            block += line
        return block;

    def handle_line( self, line ) : 
        # 获取tag列表
        res = re.compile( r'\${(.*?)[}]', re.S)
        tag_list = re.findall( res, line )
        maxParamNum = 0 
        # 遍历, 找出参数最多的tag并记录该tag的参数数量
        for tag in tag_list :
            paramList = self.config[Env.key_param_list][tag]
            if paramList is None or len( paramList ) == 0: 
                print_color( 'warning : The tag param is empty!, tag name : ' + tag, Color.YELLOW )
                continue
            maxParamNum = max( maxParamNum, len( paramList ) )
        # 循环生成minParamNum行代码
        for index in range( 0, maxParamNum ) : 
            # 将该行的tag替换为param
            resLine = self.generate_line( line, index )
            self.outputBuf += resLine #将生成的行添加到输出缓冲区

    def generate(self) : 
        if self.verify() is False : 
            print_color( 'error : template file num : ' + str( len( self.config[Env.key_template] ) ) + 'output file num : ' + str( len( self.config[Env.key_output] ) ), Color.RED )
            exit()
        for index in range( 0, len( self.config[Env.key_template] ) ) : 
            self.read_template( index )
            self.generate_single_file( index )

    ##
    # @description generate_simple 生成单个文件
    #
    # @return 
    def generate_single_file( self, index ) :
        self.file = open( self.config[Env.key_output][index], 'w' )
        if Env.generate_head : 
            self.generate_file_head()
        inputIter = iter(self.inputBuf)
        for line in inputIter :
            # 判断该行是否需要替换生成
            if re.search( "\${.*}", line ) :
                self.handle_line( line )
            elif re.search( Env.key_block, line ) : 
                block = self.get_block( inputIter )
                self.handle_line( block )
            else :
                self.outputBuf += line #无需替换, 直接添加到缓冲区
            # 若缓冲区已满, 则调用输出函数写入文件
            if len( self.outputBuf ) > Env.output_buf_size :
                self.output()
        self.output()
        print_color( "Generate to file : " + self.config[Env.key_output][index], Color.GREEN )
        self.file.close()
        

    def output( self ) : 
        self.file.write( self.outputBuf ) #写入文件
        self.outputBuf = str() #清空缓冲区

    def generate_file_head( self ) : 
        # 获取当前时间 
        now = datetime.datetime.now()
        currentTime = now.strftime( '%Y-%m-%d %H:%M:%S' )
        # 获取注释符号 
        annotation = self.config[Env.key_annotation]
        formatList = {"annotation" : self.config[Env.key_annotation], "currentTime" : currentTime }
        self.file.write( Env.file_head_template.format( **formatList ) )

    ##
    # @description verify 验证Config生成文件的有效性
    #
    # @return bool
    def verify(self) : 
        return len( self.config[Env.key_output] ) == len( self.config[Env.key_template] )

