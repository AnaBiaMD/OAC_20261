regis_global = {
"zero":"x0", "ra":"x1", "sp":"x2", "gp":"x3", "tp":"x4",
 "t0":"x5","t1":"x6", "t2":"x7",
 "s0":"x8","fp":"x8","s1":"x9",
 'a0': 'x10', 'a1': 'x11', 'a2': 'x12',
 'a3': 'x13', 'a4': 'x14', 'a5': 'x15',
 'a6': 'x16', 'a7': 'x17','s2': 'x18', 's3': 'x19',
 's4': 'x20', 's5': 'x21', 's6': 'x22',
 's7': 'x23', 's8': 'x24', 's9': 'x25',
 's10': 'x26', 's11': 'x27',
 "t3":"x28","t4":"x29","t5":"x30","t6":"x31"
}
inst_global = { #PRIMEIRO: MATEMÁTICA SEM SER IMEDIATA
    "add":{
        "opcode":"0110011",
        "funct3":"0x0",
         "funct7":"0x00"
    },
    "sub":{
        "opcode":"0110011",
        "funct3":"0x0",
         "funct7":"0x20"
    },
    "and":{
        "opcode":"0110011",
        "funct3":"0x7",
         "funct7":"0x00"
    },
    "or":{
        "opcode":"0110011",
        "funct3":"0x6",
         "funct7":"0x0"
    },
    "xor":{
        "opcode":"0110011",
        "funct3":"0x4",
         "funct7":"0x00"
    },
    "sll":{
        "opcode":"0110011",
        "funct3":"0x1",
         "funct7":"0x00"
    },
    "srl":{
        "opcode":"0110011",
        "funct3":"0x5",
         "funct7":"0x00"
    },
        "slt":{
        "opcode":"0110011",
        "funct3":"0x2",
         "funct7":"0x00"
    },
    "addi":{ #A PARTIR DAQUI MATEMÁTICA IMEDIATA
        "opcode":"0010011",
        "funct3":"0x0"
    },
        "andi":{
        "opcode":"0010011",
        "funct3":"0x7"
    },
        "ori":{
        "opcode":"0010011",
        "funct3":"0x6"
    },
        "xori":{
        "opcode":"0010011",
        "funct3":"0x4"
    }
}

non_immediate_math_instructs = ["add","sub","and","or","xor","srl","sll"]
immediate_math_instructs = ["addi","xori","ori","andi"]

def encoder_reg_opcode(reg):
    global inst_global
    global regis_global
    instrucao_out = inst_global[reg[0]]
    regis = reg[1:]
    reg_out = []
    for i in regis:
        try:
            reg_out.append(regis_global[i])
        except:
            reg_out.append(i)
    return instrucao_out,reg_out,reg[0]


with open("entrada.asm", "r",encoding="utf-8") as f:
    linhas = f.readlines()

data = []
text = []
aux = ""
for i in range(len(linhas)):
    l = linhas[i].strip()
    if l == ".data":
        aux = "data"
    elif l == ".text":
        aux = "text"
    elif l != "":
        linha_atual = [x.replace(",","") for x in l.split()]
        linha_atual.insert(0,i+1)
        if aux == "text":
            text.append(linha_atual)
        else:
            data.append(linha_atual)
    else:
        print(f"Linha {i} pulada. Motivo: Linha Vazia")
    
# CONVERSIONS HANDLERS
def reg_to_bin(reg):
    num = int(reg.replace("x", ""))
    return format(num, "05b")

def hex_to_bin(valor,bits):
    if isinstance(valor, str) and valor.startswith("0x"):
        valor = int(valor, 16)
    return format(valor, f"0{bits}b")

def int_to_bin(valor, bits):
    valor = int(valor)
    if valor < 0: # máscara de 12 bits para casos negativos como -5
        valor = valor & ((1 << bits) - 1)
    return format(valor, f"0{bits}b")

def not_immediate_math(inst,reg):
    return hex_to_bin(inst["funct7"],7) + reg_to_bin(reg[2])+reg_to_bin(reg[1])+hex_to_bin(inst["funct3"],3)+reg_to_bin(reg[0])+ inst["opcode"]
def immediate_math(inst,reg):
    return int_to_bin(reg[2],12)+reg_to_bin(reg[1])+hex_to_bin(inst["funct3"],3)+reg_to_bin(reg[0])+ inst["opcode"]


def TEXT_OUTPUT(text):
    global inst_global
    aux = -1
    for i in text:
        aux+=1
        if i[1] not in inst_global:
            print(f"Linha {i[0]} pulada. Motivo: Instrução não reconhecida.")
            continue
        inst_now,regis_now,instruct_name = encoder_reg_opcode(i[1:])
        if instruct_name in non_immediate_math_instructs:
            binario = not_immediate_math(inst_now,regis_now)
        elif instruct_name in immediate_math_instructs:
            binario = immediate_math(inst_now,regis_now)
        hexadecimal = format(int(binario, 2), "08X")

        print(f"{format(aux, "08X")} : {hexadecimal} % {i[0]}: {' '.join(i[1:])} %")
TEXT_OUTPUT(text)