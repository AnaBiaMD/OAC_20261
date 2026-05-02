RISCV_DEPTH = 16384
RISCV_WIDTH = 32


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
inst_global = { #R INSTRUCTIONS
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
    "addi":{ #I INSTRUCTIONS
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
    },
    "slti":{
        "opcode":"0010011",
        "funct3":"0x2"
    }, # I_LOAD INSTRUCTIONS
        "lw":{
        "opcode":"0000011",
        "funct3":"0x2"
    },
        "lhu":{
        "opcode":"0000011",
        "funct3":"0x5"
    }, #S TYPES
    "sw":{
        "opcode":"0100011",
        "funct3":"0x2"
    }, #U TYPES
    "lui":{
        "opcode":"0110111",
    },
    "auipc":{
        "opcode":"0010111",
    }, #J TYPES
        "jal":{
        "opcode":"1101111",
    },
        "jalr":{
        "opcode":"1100111",
        "funct3":"0x0"
    }, #B TYPE
            "beq":{
        "opcode":"1100011",
        "funct3":"0x0"
    },
        "bne":{
        "opcode":"1100011",
        "funct3":"0x1"
    },
}

R_TYPE = ["add","sub","and","or","xor","srl","sll"]
I_TYPE = ["addi","xori","ori","andi","slti"]
I_LOAD_TYPE =["lw","lhu"]
S_TYPE= ["sw"]
U_TYPE= ["lui","auipc"]
J_TYPE = ["jal","jalr"]
B_TYPE= ["beq","bne"]

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
    if valor < 0: # máscara para casos negativos como -5
        valor = valor & ((1 << bits) - 1)
    return format(valor, f"0{bits}b")

def R_TYPE_FUNCT(inst,reg):
    return hex_to_bin(inst["funct7"],7) + reg_to_bin(reg[2])+reg_to_bin(reg[1])+hex_to_bin(inst["funct3"],3)+reg_to_bin(reg[0])+ inst["opcode"]
def I_TYPE_FUNCT(inst,reg):
    return int_to_bin(reg[2],12)+reg_to_bin(reg[1])+hex_to_bin(inst["funct3"],3)+reg_to_bin(reg[0])+ inst["opcode"]
def I_LOAD_TYPE_FUNCT(inst,reg):
    global regis_global
    rd = reg[0]
    offset, rs1 = reg[1].split("(")
    rs1 = rs1.replace(")", "")
    rs1 = regis_global[rs1]
    imm = int_to_bin(offset,12)
    return (
        imm +
        reg_to_bin(rs1) +
        hex_to_bin(inst["funct3"], 3) +
        reg_to_bin(rd) +
        inst["opcode"]
    )
def U_TYPE_FUNCT(inst,reg):
    if reg[1][0:2]=="0x":
        imm = hex_to_bin(reg[1],20) # 20 bits 
    else:
        imm = int_to_bin(reg[1],  20) 
    return (
        imm +
        reg_to_bin(reg[0]) +
        inst["opcode"]
    )
def S_TYPE_FUNCT(inst,reg):
    # Possível bug com negativo?
    offset, rs1 = reg[1].split("(")
    rs1 = rs1.replace(")", "")
    rs1 = regis_global[rs1]
    imm =  int_to_bin(offset,12)
    imm1 = imm[:7]
    imm2 = imm[7:]
    return (
        imm1 +
        reg_to_bin(reg[0]) +
        reg_to_bin(rs1) +
        hex_to_bin(inst["funct3"], 3) +
        imm2 +
        inst["opcode"]
    )

def J_TYPE_FUNCT(inst,reg):
    #Break into UJ format
    imm = int_to_bin(reg[1], 21)
    imm20   = imm[0]
    imm10_1 = imm[10:20]
    imm11   = imm[9]
    imm19_12 = imm[1:9]
    return (
        imm20 +
        imm10_1 +
        imm11 +
        imm19_12 +
        reg_to_bin(reg[0]) +
        inst["opcode"]
    )
def B_TYPE_FUNCT(inst, reg, offset):
    imm = int_to_bin(offset, 13)  # 13 bits (porque inclui bit de sinal)

    imm12   = imm[0]
    imm10_5 = imm[2:8]
    imm4_1  = imm[8:12]
    imm11   = imm[1]
    rs1 = reg_to_bin(reg[0])
    rs2 = reg_to_bin(reg[1])
    return (
        imm12 +
        imm10_5 +
        rs2 +
        rs1 +
        hex_to_bin(inst["funct3"], 3) +
        imm4_1 +
        imm11 +
        inst["opcode"]
    )

def build_labels(text):
    labels = {}
    pc = 0

    for i in text:
        token = i[1]

        if token.endswith(":"):
            labels[token[:-1]] = pc
        else:
            pc += 4

    return labels
def TEXT_OUTPUT(text,arquivo):
    aux_labels = {}
    print("Iniciando saída _text")
    saida_nome = arquivo[:-4]+ "_text.mif"
    pc = 0
    labels = build_labels(text)
    with open(saida_nome, "w") as f:
        f.write(f"DEPTH = {RISCV_DEPTH}\n")
        f.write(f"WIDTH = {RISCV_WIDTH}\n")
        f.write("ADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n")
        global inst_global
        aux = -1
        for i in text:
            aux += 1
            if aux > RISCV_DEPTH:
                print(f"Limite de Instruções Atingido. Parando na linha {i[0]}")
                break
            if i[1] not in inst_global and i[1][-1]!=":":
                try:
                    i[2]
                    print(f"Linha {i[0]} pulada. Motivo: Instrução não reconhecida.")
                except:
                    print(f"Linha {i[0]} pulada. Motivo: Instrução incompleta.")
                continue
            if i[1][-1]==":":
                aux_labels[str(i[0])] = i[1]
                i.pop(1)
            inst_now, regis_now, instruct_name = encoder_reg_opcode(i[1:])
            if instruct_name in R_TYPE: binario = R_TYPE_FUNCT(inst_now,regis_now)
            elif instruct_name in I_TYPE: binario = I_TYPE_FUNCT(inst_now,regis_now)
            elif instruct_name in I_LOAD_TYPE: binario = I_LOAD_TYPE_FUNCT(inst_now,regis_now)
            elif instruct_name in U_TYPE: binario = U_TYPE_FUNCT(inst_now,regis_now)
            elif instruct_name in S_TYPE: binario = S_TYPE_FUNCT(inst_now,regis_now)
            elif instruct_name in B_TYPE:
                rs1 = regis_now[0]
                rs2 = regis_now[1]
                label = regis_now[2]

                offset = labels[label] - pc

                binario = B_TYPE_FUNCT(inst_now, [rs1, rs2], offset)
            elif instruct_name in J_TYPE:
                if len(regis_now) == 1:
                    rd = "x1"
                    label = regis_now[0]
                else:
                    rd = regis_now[0]
                    label = regis_now[1]

                offset = labels[label] - pc

                binario = J_TYPE_FUNCT(inst_now, [rd, offset])
            hexadecimal = format(int(binario, 2), "08X")
            if str(i[0]) in aux_labels:
                f.write(f"{format(aux, "08X")} : {hexadecimal};   % {i[0]}: {aux_labels[str(i[0])]} {i[1]} {', '.join(i[2:])} %\n")
            else:
                f.write(f"{format(aux, "08X")} : {hexadecimal};   % {i[0]}: {i[1]} {', '.join(i[2:])} %\n")
        
            pc += 4
        f.write("END;")
        print("Escrita do arquivo _text.mif finalizada.")

while True:
    arquivo = input("Para sair, digite Sair. Nome do arquivo com extensão: ")
    if arquivo == "Sair":
        exit()
    try:
        with open(arquivo, "r",encoding="utf-8") as f:
            linhas = f.readlines()
        print("Arquivo aberto com sucesso! Começando leitura.")
    except:
        print("Não existe este arquivo. Você colocou a extensão?")
        continue

    data = []
    text = []
    aux = ""
    for i in range(len(linhas)):
        l = linhas[i].strip()
        if l == ".data":
            aux = "data"
            print("Lendo .data.")
        elif l == ".text":
            aux = "text"
            print("Lendo .text")
        elif l != "":
            linha_atual = [x.replace(",","") for x in l.split()]
            linha_atual.insert(0,i+1)
            if aux == "text":
                text.append(linha_atual)
            else:
                data.append(linha_atual)
        else:
            print(f"Linha {i} pulada. Motivo: Linha Vazia")
    TEXT_OUTPUT(text,arquivo)