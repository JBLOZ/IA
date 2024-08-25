.text


bgt $t1, $t0, label
li $t2, 1
jal fin
label:
li $t2, 0

fin:
addi $v0, $0, 10