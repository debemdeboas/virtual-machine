LDI R1, 0
STD [50], R1
LDI R2, 1
STD [51], R2
LDI R8, 52
LDI R6, 6
LDI R7, 60
LDI R3, 0
ADD R3, R1
LDI R1, 0
ADD R1, R2
ADD R2, R3
STX [R8], R2 ; STX R8, R2 IN THE EXAMPLE
ADDI R8, 1
SUB R7, R8
JMPIG R6, R7
STOP