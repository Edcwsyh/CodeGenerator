# 这是一个根据配置文件生成代码的脚本  

## 代码结构:  
src--  
&emsp;&emsp;|- ConfigReader.py 配置读取器  
&emsp;&emsp;|- Env.py 环境变量  
&emsp;&emsp;|- Generator.py 代码生成器  
&emsp;&emsp;|- CodeGen.py 主脚本  
&emsp;&emsp;|- TemplateReader.py 代码模板读取器  

## 原理介绍  
CodeGenerator 主要依赖一个Json格式的配置文件及代码模板文件(tmpl)来生成代码,   
它的主要原理是在模板文件当中预先定义要符号(tag), 随后将该符号替换为配置文件中对应的参数  
CodeGenerator是基于每一行来生成的, 它暂时不支持对某一块代码进行生成

以下面代码为例:  
### 模板文件 Foo.tmpl  
`case ${ID} : ${Func}( parm1, parm2 )  `

### 配置文件 config.json  
`{`  
&emsp; `"template_file" : "Foo.tmpl",`&emsp; 模板文件, 支持相对路径和绝对路径  
&emsp; `"output_file" : "Foo.cpp",` &emsp; &emsp; 生成的文件, 支持相对路径和绝对路径  
&emsp; `"annotation" : "//",`&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp; 生成的文件注释符号, 主要用于生成生成信息(如文件生成时间)  
&emsp; `"param_list" : {`&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; 参数列表, 该参数键值与模板文件中的符号一一对应  
&emsp;&emsp; `"ID" : [ "1", "2", "3" ],`&emsp;&emsp; 符号的参数列表, 配置多个参数将生成多行代码  
&emsp;&emsp; `"Func" : [ "Func1", "Func2" ]`  
&emsp; `}`  
`}`  
    
执行 `CodeGen.py ./config.json` (假设配置文件与脚本在同一目录下)  
CodeGenerator 将在脚本所在目录生成一个名为Foo.cpp的文件  
它的大致内容如下所示:  
### 生成文件 Foo.cpp  
`case 1 : Func1( parm1, parm2 )`  
`case 2 : Func2( parm1, parm2 )`  
`case 3 : Func2( parm1, parm2 )`  

## 代码块生成
CodeGenerator支持针对代码块的生成,使用方法是在要生成的代码块首位添加`$[Block]`标识符, 以下面代码为例:   
`$[Block]`  
`case ${ID} : `  
&emsp;&emsp;`${Func}( parm1, parm2 )`  
`$[Block]`  
生成的代码也会变成 :  
`case 1 :`  
&emsp;&emsp; `Func1( parm1, parm2 )`  
`case 2 :`  
&emsp;&emsp; `Func2( parm1, parm2 )`  
`case 3 :`  
&emsp;&emsp; `Func2( parm1, parm2 )` 

但仍然存在一定的不足, 例如, 在`$[Block]`标识的作用域中尝试使用一个新的`$[Block]`来进行嵌套代码生成将会失败,目前的一个想法是模仿xlm语法将`$[Block]`的结束符号改为`$[\Block]`来标识代码块的结束

example为一个完整的使用示例，使用`CodeGen.py ../example/conf.json`即可生成代码  

写在最后的一些建议:  
之所以写这个生成工具, 主要是为了应对实际开发中经常要编写重复代码的问题  
但事实上, 使用CodeGenerator也会陷入需要频繁改动配置文件的问题  
这当然不是我们想要的结果, 一个正确的使用方法是, 自己编写一个解析脚本, 通过读取其他文件来生成配置文件, 再调用CodeGenerator来生成实际代码.  
例如编写以protobuf为传输协议的系统时, 我们可以写一个脚本来解析protobuf, 为对应的message生成处理函数, 再结合代码模板与配置文件来生成代码.  
