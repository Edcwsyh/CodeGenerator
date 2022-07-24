#!/usr/bin/env python3
# coding=utf-8

# TODO 可配置项 begin
key_output = "output_file"          #输出文件关键字
key_template = "template_file"      #模板文件关键字
key_param_list = "param_list"       #参数列表关键字
key_annotation = "annotation"       #注释关键字
key_block = "\$\[Block]"

output_buf_size = 512               #输出缓冲区大小
generate_head = True                #是否生成文件头(包含时间信息)

#文件头模板
file_head_template = "{annotation} Generate by Edcwsyh/CodeGenerate\n{annotation} Generate time : {currentTime}\n{annotation} Github : https://github.com/Edcwsyh/CodeGenerator.git\n\n"
# 可配置项 end
