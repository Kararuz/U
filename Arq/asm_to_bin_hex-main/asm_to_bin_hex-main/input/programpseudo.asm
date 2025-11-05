addi x5, x5, 10

la x5, 8

lb x5, 0(x5)
lh x5, 0(x5)
lw x5, 0(x5)

sb x5, label1(x6)
sh x5, label1(x6)
sw x5, label1(x6)

nop
li x5, 100
mv x5, x6
not x5, x6
neg x5, x6
seqz x5, x6
snez x5, x6
sltz x5, x6
sgtz x5, x6

beqz x5, label1
bnez x5, label1
blez x5, label1
bgez x5, label1

bgt x5, x6, label1
ble x5, x6, label1
bgtu x5, x6, label1
bleu x5, x6, label1

j label1
jal label1
jr x5
jalr x5
ret
call label1
tail label1

label1:
 addi x0, x0, 0
label2:
 addi x0, x0, 0