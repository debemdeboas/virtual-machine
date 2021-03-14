; GIVEN `N` (INT) AT POSITION `M` IN MEMORY:
;   IF N < 0: RET -1, STOP
;   ELSE CALCULATE THE FACTORIAL OF N (N!)
LDI R8, 1
LDI R9, 47
TRAP R8, R9

; MAIN PROGRAM
LDD R0, [47]
LDI R1, -1
LDI R7, 30 ; OUTPUT ADDRESS
JMPIL R7, R0 ; END THE PROGRAM IF R0 < 0
; R0 = 0, RETURN 1
LDI R1, 1
JMPIE R7, R0 ;
; CALCULATE $R0!$
LDI R1, 0 ; USE AUX VAR TO KEEP ORIGINAL VALUE
LDI R2, 1 ; LOOP COUNTER
LDI R3, -1 ; LOOP CONTROL
LDI R6, 22 ; LOOP START ADDRESS
ADD R1, R0 ; R1 = R0
ADD R3, R0 ; R3 = R0 - 1
; START LOOP
MULT R1, R2
ADDI R2, 1
SUBI R3, 1
JMPIE R7, R3 ; END LOOP IF R3 = 0
JMPIL R7, R3 ; END LOOP IF R3 < 0
JMPI R6

; OUTPUT
STD [50], R1 ; SAVE OUTPUT TO MEMORY
LDI R8, 2
LDI R9, 50
TRAP R8, R9
STOP