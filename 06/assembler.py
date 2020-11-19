# 最开始的版本，假设无Symbols
# 全部使用function即可，似乎没有必要使用oop
# 假设所以输入合理，无语法错误
import re
import os


#  将一个语句拆成有效的部分。处理的是一行字符串
    # A-insturction: @value  => [@, value]
    # C-insturction: dest = comp; jump => [dest, comp, jump] dest and jump may be null.

# 处理blank lines.// 开头的省略
def strip(s):
    s = s.strip()  # 空白行已被处理，注释前的空格也已处理
    if s.startswith("//"):
        s = ""
    
    if "//" in s:
        s = s[0:(s.index("//"))]
    
    s = s.replace(" ", "")
    return s

# parser 接受指令返回一个list装载了各个有效的部分.
def parser(instruction):
    # 要注意此情况
    if instruction == '':
        return []

    if instruction.startswith("@"):
        return ['@', instruction[1::]]   # A instruction
    else:
        fields =  re.split(r"=|;", instruction)
        if '=' not in instruction:
            fields.insert(0, "null")
        if ";" not in instruction:
            fields.append("null")
        
        return fields




# 将parser拆成的部分翻译成二进制

# c instuction table
comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


dest_table = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump_table = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }

# 翻译到binary code
def translate(lst):
    # 将int值转换成15位二进制字符串
    def value_to_binary(i):
        res = bin(i).replace('0b', "")

        return (15 - len(res)) * '0' + res
    
    if lst == []:
        return ""

    if lst[0] == '@':
        return '0' + value_to_binary(int(lst[1]))
    else:
        return "111" + comp_table[lst[1]] + dest_table[lst[0]] + jump_table[lst[2]]





# TODO 处理Symbol(Label, pre-defined, variable)



# 读取文件 输出文件
def assembler(path):
    name = os.path.basename(path).split(".")[0] + ".hack"
    with open(path) as f:
        with open(name, 'w') as g:
            for line in f:
                lst = parser(strip(line))
                res = translate(lst)
                if res != '':
                    g.write(res + '\n')




if __name__ == "__main__":
    
    file_paths = [r"C:\code_learn\com_sys_couresa\assem\Add.asm",
                  r"C:\code_learn\com_sys_couresa\assem\MaxL.asm",
                  r"C:\code_learn\com_sys_couresa\assem\PongL.asm",
                  r"C:\code_learn\com_sys_couresa\assem\RectL.asm"]

    for path in file_paths:
        assembler(path)
    
