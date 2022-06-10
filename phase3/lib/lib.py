def add_readInteger():
    return """
.text
lib_ReadInteger:
.text            
    li $v0, 5
    syscall
    sub $sp, $sp, 8
    sw $v0, 0($sp)
    jr   $ra
    """

def add_readLine():
    return """
.text
    lib_ReadLine:
    li $a0, 255
    li $v0, 9
    syscall  # malloc
    move $a0, $v0
    li $v0, 8
    li $a1, 255
    syscall
    sub $sp, $sp, 8
    sw $a0, 0($sp)
    jr   $ra
    """

def add_string_concat():
    return """
lib_strcopier:
    or $t0, $a0, $zero
    or $t1, $a1, $zero
lib_strcopier_loop:
    lb $t2, 0($t0)
    beq $t2, $zero, lib_strcopier_end
    addiu $t0, $t0, 1
    sb $t2, 0($t1)
    addiu $t1, $t1, 1
    b lib_strcopier_loop
lib_strcopier_end:
    or $v0, $t1, $zero
    jr $ra
    """

def add_new_array():
    return """
    lib_new_array:
        lw $a0, 0($sp)
        move $t0, $a0
        sll $a0, $a0, 3
        addi $a0, $a0, 8
        li $v0, 9
        syscall
        sw $t0, 0($v0)
        addi $v0, $v0, 8
        sw $v0, 0($sp)
        jr $ra
    """

def add_array_cp():
    return """
    lib_array_cp:
        lw $t0, 0($sp)
        lw $t1, 8($sp)
        lw $t2, -8($t0)
        lw $t3, -8($t1)
        add $a0, $t2, $t3
        sub $sp, $sp, 8
        sw $a0, 0($sp)
        sw $ra, -8($sp)
        jal lib_new_array
        lw $ra, -8($sp)
        lw $a0, 0($sp)
        lw $t0, 8($sp)
        lw $t1, 16($sp)
        lw $t2, -8($t0)
        lw $t3, -8($t1)
        addi $t7, $a0, 0        #dest array iterator
    array_cp_loop1:
        lw $t4, 0($t1)
        sw $t4, 0($t7)
        addiu $t7, $t7, 8
        addiu $t1, $t1, 8
        sub $t3, $t3, 1
        beqz $t3, array_cp_loop2
        j array_cp_loop1
    array_cp_loop2:
        lw $t4, 0($t0)
        sw $t4, 0($t7)
        addiu $t7, $t7, 8
        addiu $t0, $t0, 8
        sub $t2, $t2, 1
        beqz $t2, array_cp_finish
        j array_cp_loop2 
    array_cp_finish:
        jr $ra
        
    lib_array_cp_double:
        lw $t0, 0($sp)
        lw $t1, 8($sp)
        lw $t2, -8($t0)
        lw $t3, -8($t1)
        add $a0, $t2, $t3
        sub $sp, $sp, 8
        sw $a0, 0($sp)
        sw $ra, -8($sp)
        jal lib_new_array
        lw $ra, -8($sp)
        lw $a0, 0($sp)
        lw $t0, 8($sp)
        lw $t1, 16($sp)
        lw $t2, -8($t0)
        lw $t3, -8($t1)
        addi $t7, $a0, 0        #dest array iterator
    array_cp_loopd1:
        l.d $f0, 0($t1)
        s.d $f0, 0($t7)
        addiu $t7, $t7, 8
        addiu $t1, $t1, 8
        sub $t3, $t3, 1
        beqz $t3, array_cp_loopd2
        j array_cp_loopd1
    array_cp_loopd2:
        l.d $f0, 0($t0)
        s.d $f0, 0($t7)
        addiu $t7, $t7, 8
        addiu $t0, $t0, 8
        sub $t2, $t2, 1
        beqz $t2, array_cp_finishd
        j array_cp_loopd2 
    array_cp_finishd:
        jr $ra
    """

def add_access_array():
    return """
    lib_access_array:
        lw $t0, 8($sp)
        lw $t1, 0($sp)
        sll $t1, $t1, 3
        add $t1, $t1, $t0
        lw $t2,0($t1)
        sw $t2, 8($sp)
        addi $sp, $sp, 8
        jr $ra
        
    lib_access_array_double:
        lw $t0, 8($sp)
        lw $t1, 0($sp)
        sll $t1, $t1, 3
        add $t1, $t1, $t0
        l.d $f0,0($t1)
        s.d $f0, 8($sp)
        addi $sp, $sp, 8
        jr $ra
    """

def add_strcmp():
    return """
    lib_strcmp:
        lw $s2, 0($sp)
        lw $s3, 8($sp)
        cmploop:
            lb      $t2,0($s2)
            lb      $t3,0($s3)
            bne     $t2,$t3,cmpne
            beq     $t2,$zero,cmpeq
            addi    $s2,$s2,1
            addi    $s3,$s3,1
            j       cmploop
        cmpne:
            li $t1, 0
            sub $sp, $sp, 8
            sw $t1, 0($sp)
            jr $ra
        cmpeq:
            li $t1, 1
            sw $t1, 8($sp)
            addi $sp, $sp, 8
            jr $ra
    """

def add_itod():
    return """
            .text
                 lib_itod:
                 lw $t0, 0($sp)
                 mtc1.d $t0, $f0
                 cvt.d.w $f0, $f0
                 s.d $f0, 0($sp)
                 jr   $ra
            """

def add_dtoi():
    return """
        .text
            lib_dtoi:
            l.d $f0, 0($sp)
            round.w.d $f0, $f0
            mfc1 $t0, $f0
            sw $t0, 0($sp)
            jr   $ra
        """

def add_itob():
    return """
        .text
            lib_itob:
            lw $t0, 0($sp)
            li $t1, 0
            beqz $t0, itob_false
            li $t1, 1
            itob_false:
            sw $t1, 0($sp)
            jr $ra
        """


def add_print():
    return """
.text 
    lib_print_bool:
    lw $t0, 0($sp)
    addi $sp, $sp, 8
    la $a0,falseConstString
    beqz $t0,lib_print_false
    la $a0,trueConstString
    lib_print_false:
    li $v0,4
    syscall
    jr $ra
    
    lib_print_double:
    l.d $f12, 0($sp)
    addi $sp, $sp, 8
    cvt.s.d $f12, $f12
    li $v0, 2
    syscall
    jr $ra
    
    lib_print_int:
    li $v0, 1
    lw $a0, 0($sp)
    addi $sp, $sp, 8
    syscall
    jr $ra
    
    lib_print_string:
    li $v0, 4
    lw $a0, 0($sp)
    addi $sp, $sp, 8
    syscall
    jr $ra
    
    print_newline_char:
    li $v0, 4
    la $a0, newLineChar
    syscall
    jr $ra 
    
.data
    newLineChar: .asciiz "\\n"
    trueConstString: .asciiz "true"
    falseConstString: .asciiz "false"
.text

    """
