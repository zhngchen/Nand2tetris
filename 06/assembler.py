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
    if instruction == '' or instruction.startswith('('):   # 标号也跳过
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
    global n     # 变量分配
    # 将int值转换成15位二进制字符串
    def value_to_binary(i):
        res = bin(i).replace('0b', "")

        return (15 - len(res)) * '0' + res
    
    if lst == []:
        return ""
    # 遇到的是变量要处理
    if lst[0] == '@':
        if lst[1][0].isalpha():    # 首字母
            v = lst[1]
            if v in symbol_table:
                lst[1] = symbol_table[v]
            else:
                symbol_table[v] = str(n)
                lst[1] = str(n)
                n += 1
        
        return '0' + value_to_binary(int(lst[1]))

    else:
        return "111" + comp_table[lst[1]] + dest_table[lst[0]] + jump_table[lst[2]]





# 处理Symbol(Label, pre-defined, variable)


# 创建symbol_table
symbol_table = {
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
    "SCREEN": "16384",
    "KBD": "24576",
}

for i in range(16):
    symbol_table["R" + str(i)] = str(i)


n = 16


# 读取文件 输出文件
def assembler(path):
    # 添加标号到symbol_table
    def first_pass():
        i = 0
        with open(path) as f:
            for line in f:
                s = strip(line)
                if s.startswith('('):
                    symbol_table[s[1:-1]] = str(i)
                # 确定i值，空白和标号跳过
                if not(s == "" or s.startswith('(')):
                    i += 1
    
    first_pass()
    
    name = os.path.basename(path).split(".")[0] + ".hack"
    with open(path) as f:
        with open(name, 'w') as g:
            for line in f:
                lst = parser(strip(line))
                res = translate(lst)
                if res != '':
                    g.write(res + '\n')




if __name__ == "__main__":
    
    # file_paths = [
    #               r"C:\code_learn\com_sys_couresa\Max.asm",
    #               r"C:\code_learn\com_sys_couresa\Pong.asm",
    #               r"C:\code_learn\com_sys_couresa\Rect.asm"]

    # for path in file_paths:
    #     assembler(path)
    
    file_path = r"C:\code_learn\com_sys_couresa\Rect.asm"
    assembler(file_path)
