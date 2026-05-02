.data
a: .word 1, 2, 3, 4, 5
b: .half 7, 6, 5, 4, 5
c: .byte 6, 5, 4, 3, 2
d: .string "a casa é azul."


.text
inicio: auipc, t0, 0
jalr t6, 8(t0)
lui t1, 0x1001
addi t2, zero, 4
add t6, t2, zero
beq t2, t6, f
g: sub t6, t6, t6
f: add t6, t6, t2
bne t2, t6, g
sll t1, t1, t2
lw t2, 0(t1)
sw t2, 32(t1)
add t3, t2, t1
sub t3, t1, t3
and t4, t1, t2
or t4, t1, t2
xor t4, t1, t2
slt t6, t2, t6
andi t6, t2, 1
ori t6, t2, 0
xori t6, t2, 1
jal rotulo
beq t1, t2, rotulo
lhu t5, 32(t1)
rotulo: slti t1, t2, -1
