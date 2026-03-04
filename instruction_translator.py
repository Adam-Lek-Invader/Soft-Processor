#params
mode = 0; #0-bin, 1-dec, 2-hex

def imm_to_val(imm:str):
    if(imm.find("0x") != -1):
        return int(imm,16)
    elif(imm.find("0b") != -1):
        return int(imm,2)
    else:
        return int(imm,10)

def to_pure_ins(txt:str):
    #komentarze
    i = txt.find("//")
    if(i == -1):
        buff = txt
    else:
        buff = txt[0:i]
    #numery linijek
    i = buff.find(":")
    if(i == -1):
        buff = buff
    else:
        buff = buff[i+1:]
    buff = buff.strip()
    buff = buff.replace(",", " ")
    buff = buff.split()
    if(len(buff) == 1):
        return buff[0]
    return buff

def to_bin_conv(val,nb):
    bin_val = format(val, 'b')
    if(nb < len(bin_val)):
        return None
    while(nb > len(bin_val)):
        bin_val = '0' + bin_val;
    return bin_val

def make_instruction(pc_op,alu_op,rx_op,imm_op,ry_op,rd_op,d_op,imm):
    bin_ins = "000000"
    bin_ins = bin_ins + to_bin_conv(pc_op,2)
    '''
    01 => jz/jump
    11 => jnz
    '''
    bin_ins = bin_ins + "00"
    bin_ins = bin_ins + to_bin_conv(alu_op,2)
    bin_ins = bin_ins + "0"
    bin_ins = bin_ins + to_bin_conv(rx_op,3)
    bin_ins = bin_ins + to_bin_conv(imm_op,1)
    bin_ins = bin_ins + to_bin_conv(ry_op,3)
    bin_ins = bin_ins + to_bin_conv(rd_op,1)
    bin_ins = bin_ins + to_bin_conv(d_op,3)
    bin_ins = bin_ins + to_bin_conv(imm,8)
    
    dec_val = int(bin_ins,2)
    return (bin_ins, dec_val, hex(dec_val))
 
nop = make_instruction(pc_op=0,
                       alu_op=0,#jakakolowiek wartosc
                       rx_op=6,
                       imm_op=0,
                       ry_op=6,
                       rd_op=0,#jakkolwiek bo d_op zamyka rejestry
                       d_op=6,
                       imm=0)

def ins_to_code(pure_ins, mode:int):    
    if(type(pure_ins) == str):
        nop = make_instruction(pc_op=0,
                               alu_op=0,#jakakolowiek wartosc
                               rx_op=6,
                               imm_op=0,
                               ry_op=6,
                               rd_op=0,#jakkolwiek bo d_op zamyka rejestry
                               d_op=6,
                               imm=0)
        return nop[mode]
    else:
        ins = pure_ins[0].lower()
        if(ins == "jump"):
            Rnum = int(pure_ins[1].strip()[1])
            jump = make_instruction(pc_op=1,
                                   alu_op =3,#przejscie imm_mux
                                   rx_op  =6,# 0 == 0
                                   imm_op = 0,# ry_op
                                   ry_op  = Rnum,
                                   rd_op  =0,#jakkolwiek bo d_op zamyka rejestry
                                   d_op   =6,#nic nie ma zapisywac do R0-5
                                   imm    =0)#jakakolwiek
            return jump[mode]
        elif(ins == "movi"):
            Rnum = int(pure_ins[1].strip()[1])
            imm_val = pure_ins[2].strip()
            imm_val = imm_to_val(imm_val)
            movi = make_instruction(pc_op=0,
                                   alu_op =1,#dodawanie (do zera)
                                   rx_op  =6,# 0
                                   imm_op = 1,#war. z ins
                                   ry_op  = 6,#jakakolwiek
                                   rd_op  =0,#zapis z alu
                                   d_op   =Rnum,#
                                   imm    =imm_val)#jakakolwiek
            return movi[mode]
        elif(ins == "mov"):
            Rnum_to = int(pure_ins[1].strip()[1])
            Rnum_fr = int(pure_ins[2].strip()[1])
            mov = make_instruction(pc_op=0,
                                   alu_op =1,#dodawanie (do zera)
                                   rx_op  =Rnum_fr,# R_fr
                                   imm_op = 0,#war. z ins
                                   ry_op  = 6,# +0
                                   rd_op  =0,#zapis z alu
                                   d_op   =Rnum_to,#
                                   imm    =0)#jakakolwiek
            return mov[mode]
        elif(ins == "jumpi"):
            imm_val = pure_ins[1].strip()
            imm_val = imm_to_val(imm_val)
            jumpi = make_instruction(pc_op=1,
                                   alu_op =3,#przejscie imm_mux
                                   rx_op  =6,# 0 == 0
                                   imm_op = 1,# z imm
                                   ry_op  = 6, #jakkolwiek
                                   rd_op  =0,#jakkolwiek bo d_op zamyka rejestry
                                   d_op   =6,#nic nie ma zapisywac do R0-5
                                   imm    =imm_val)#jakakolwiek
            return jumpi[mode]
        elif(ins == "jz"):
            Rnum = int(pure_ins[1].strip()[1])
            imm_val = pure_ins[2].strip()
            imm_val = imm_to_val(imm_val)
            jz = make_instruction(pc_op=1,
                                   alu_op =3,#przejscie imm_mux
                                   rx_op  =Rnum,# Rx == 0
                                   imm_op = 1,# z imm
                                   ry_op  = 6, #jakkolwiek
                                   rd_op  =0,#jakkolwiek bo d_op zamyka rejestry
                                   d_op   =6,#nic nie ma zapisywac do R0-5
                                   imm    =imm_val)#jakakolwiek
            return jz[mode]
        elif(ins == "jnz"): #nie dziala
            Rnum = int(pure_ins[1].strip()[1])
            imm_val = pure_ins[2].strip()
            imm_val = imm_to_val(imm_val)
            jnz = make_instruction(pc_op=3,
                                   alu_op =3,#przejscie imm_mux
                                   rx_op  =Rnum,# Rx == 0
                                   imm_op = 1,# z imm
                                   ry_op  = 6, #jakkolwiek
                                   rd_op  =0,#jakkolwiek bo d_op zamyka rejestry
                                   d_op   =6,#nic nie ma zapisywac do R0-5
                                   imm    =imm_val,)#jakakolwiek
            return jnz[mode]
        elif(ins == "add"):
            Rnum_to = int(pure_ins[1].strip()[1])
            Rnum1 = int(pure_ins[2].strip()[1])
            Rnum2 = int(pure_ins[3].strip()[1])
            add = make_instruction(pc_op=0,
                                   alu_op =1,#dodawanie
                                   rx_op  =Rnum1,# R_fr
                                   imm_op = 0,#z rejestru
                                   ry_op  = Rnum2,# +0
                                   rd_op  =0,#zapis z alu
                                   d_op   =Rnum_to,#
                                   imm    =0)#jakakolwiek
            return add[mode]
        elif(ins == "addi"):
            Rnum_to = int(pure_ins[1].strip()[1])
            Rnum1 = int(pure_ins[2].strip()[1])
            imm_val = pure_ins[3].strip()
            imm_val = imm_to_val(imm_val)
            addi = make_instruction(pc_op=0,
                                   alu_op =1,#dodawanie
                                   rx_op  =Rnum1,# R_fr
                                   imm_op = 1,#z imm
                                   ry_op  = 6,# jakkolwiek
                                   rd_op  =0,#zapis z alu
                                   d_op   =Rnum_to,#
                                   imm    =imm_val)#jakakolwiek
            return addi[mode]
        elif(ins == "and"):
            Rnum_to = int(pure_ins[1].strip()[1])
            Rnum1 = int(pure_ins[2].strip()[1])
            Rnum2 = int(pure_ins[3].strip()[1])
            #and jest zabrana nazwa
            ins_and = make_instruction(pc_op=0,
                                   alu_op =0,#AND
                                   rx_op  =Rnum1,# 
                                   imm_op = 0,#z rejestru
                                   ry_op  = Rnum2,# 
                                   rd_op  =0,#zapis z alu
                                   d_op   =Rnum_to,#
                                   imm    =0)#jakakolwiek
            return ins_and[mode]
        elif(ins == "andi"):
            Rnum_to = int(pure_ins[1].strip()[1])
            Rnum1 = int(pure_ins[2].strip()[1])
            imm_val = pure_ins[3].strip()
            imm_val = imm_to_val(imm_val)
            andi = make_instruction(pc_op=0,
                                   alu_op =0,#AND
                                   rx_op  =Rnum1,# R_fr
                                   imm_op = 1,#z imm
                                   ry_op  = 6,# jakkolwiek
                                   rd_op  =0,#zapis z alu
                                   d_op   =Rnum_to,#
                                   imm    =imm_val)
            return andi[mode]
        elif(ins == "load"):
            Rnum_to = int(pure_ins[1].strip()[1])
            Rnum_addres = int(pure_ins[2].strip()[1])
            load = make_instruction(pc_op=0,
                                   alu_op =3,#przepis z ry
                                   rx_op  =6,#jakkolwiek 
                                   imm_op = 0,#z rejestru
                                   ry_op  = Rnum_addres,# 
                                   rd_op  =1,#zapis z pam. danych
                                   d_op   =Rnum_to,#
                                   imm    =0)#jakakolwiek
            return load[mode]
        elif(ins == "loadi"):
            Rnum_to = int(pure_ins[1].strip()[1])
            imm_val = pure_ins[2].strip()
            imm_val = imm_to_val(imm_val)
            load = make_instruction(pc_op=0,
                                   alu_op =3,#przepis z ry
                                   rx_op  =6,#jakkolwiek 
                                   imm_op = 1,#z imm
                                   ry_op  = 6,#jakkolwiek 
                                   rd_op  =1,#zapis z pam. danych
                                   d_op   =Rnum_to,#
                                   imm    =imm_val)#
            return load[mode]
        
    
all_ins = dict()
all_ins["nop"] = nop  


with open(r"program.asm","rt") as f_asm:
    with open("program.mc", "wt") as f_bin:
        f_bin.write("memory_initialization_radix = 2;\n memory_initialization_vector = \n")
        for i,ins in enumerate(f_asm):
            try:
                pure_ins = to_pure_ins(ins)
                #f_bin.write("assign program["+str(i+1)+"] = 32'b"+str(ins_to_code(pure_ins, mode))+";\n")
                f_bin.write(str(ins_to_code(pure_ins, mode)) + "\n")
            except:
                print(f"error code: {ins}")
        f_bin.write(";")

