.text


li $v0, 5
syscall
move $t0, $v0

mult $t0, $t0
mflo $s0

li $t1, 5
mult  $s0, $t1
mflo $s1


li $t2, 2
mult $t0, $t2
mflo $s2


add $s0, $s1, $s2
addi $s0, $s0, 3

move $a0, $s0
li $v0, 1
syscall




