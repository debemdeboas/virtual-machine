; LOAD DATA INTO MEMORY BEFORE START
LDI R0, 120
STD [255], R0
LDI R0, 0 ; SET BACK TO DEFAULT VALUE (0)

; MAIN PROGRAM
LDI R0, 256 ; OUTPUT MEMORY BLOCK
LDD R7, [255] ; LOAD THE VALUE STORED IN POSITION 255
LDI R2, 15 ; SKIP TO LINE 16 IF R7 >= 0
JMPIG R2, R7
JMPIE R2, R7
LDI R3, -1
STX [R0], R3
STOP
; WRITE `R1` NUMBERS OF THE FIB. SEQUENCE
LDI R4, 1
SUB R4, R7
LDI R5, 27
JMPIE R5, R4
LDI R4, 2
SUB R4, R7
LDI R5, 31
JMPIE R5, R4
JMP 37
; WRITE 0 TO MEMORY AND STOP
LDI R3, 0
STX [R0], R3
STOP
; WRITE 0, 1 TO MEMORY AND STOP
LDI R3, 0
STX [R0], R3
ADDI R3, 1
ADDI R0, 1
STX [R0], R3
STOP
; WRITE FIB SEQUENCE `R7` TIMES
LDI R1, 0
LDI R2, 1
STX [R0], R1
ADDI R0, 1
STX [R0], R2
ADDI R0, 1
LDI R6, 46 ; LOOP CONTROL
LDI R5, 1 ; LOOP COUNTER
SUBI R7, 2 ; REMOVE 2 ENTRIES FROM `FOR` CLAUSE TO COMPENSATE FOR THE ALREADY-WRITTEN 0, 1
; START LOOP
LDI R3, 0
ADD R3, R1 ; R3 = R1
LDI R1, 0
ADD R1, R2 ; R1 = R2
ADD R2, R3
STX [R0], R2
ADDI R0, 1
SUB R7, R5 ; FOR --
JMPIG R6, R7
STOP
; WITH FIB-CHECKER AND 120 ENTRIES:
;0 is a Fibonacci number
;1 is a Fibonacci number
;1 is a Fibonacci number
;2 is a Fibonacci number
;3 is a Fibonacci number
;5 is a Fibonacci number
;8 is a Fibonacci number
;13 is a Fibonacci number
;21 is a Fibonacci number
;34 is a Fibonacci number
;55 is a Fibonacci number
;89 is a Fibonacci number
;144 is a Fibonacci number
;233 is a Fibonacci number
;377 is a Fibonacci number
;610 is a Fibonacci number
;987 is a Fibonacci number
;1597 is a Fibonacci number
;2584 is a Fibonacci number
;4181 is a Fibonacci number
;6765 is a Fibonacci number
;10946 is a Fibonacci number
;17711 is a Fibonacci number
;28657 is a Fibonacci number
;46368 is a Fibonacci number
;75025 is a Fibonacci number
;121393 is a Fibonacci number
;196418 is a Fibonacci number
;317811 is a Fibonacci number
;514229 is a Fibonacci number
;832040 is a Fibonacci number
;1346269 is a Fibonacci number
;2178309 is a Fibonacci number
;3524578 is a Fibonacci number
;5702887 is a Fibonacci number
;9227465 is a Fibonacci number
;14930352 is a Fibonacci number
;24157817 is a Fibonacci number
;39088169 is a Fibonacci number
;63245986 is a Fibonacci number
;102334155 is a Fibonacci number
;165580141 is a Fibonacci number
;267914296 is a Fibonacci number
;433494437 is a Fibonacci number
;701408733 is a Fibonacci number
;1134903170 is a Fibonacci number
;1836311903 is a Fibonacci number
;2971215073 is a Fibonacci number
;4807526976 is a Fibonacci number
;7778742049 is a Fibonacci number
;12586269025 is a Fibonacci number
;20365011074 is a Fibonacci number
;32951280099 is a Fibonacci number
;53316291173 is a Fibonacci number
;86267571272 is a Fibonacci number
;139583862445 is a Fibonacci number
;225851433717 is a Fibonacci number
;365435296162 is a Fibonacci number
;591286729879 is a Fibonacci number
;956722026041 is a Fibonacci number
;1548008755920 is a Fibonacci number
;2504730781961 is a Fibonacci number
;4052739537881 is a Fibonacci number
;6557470319842 is a Fibonacci number
;10610209857723 is a Fibonacci number
;17167680177565 is a Fibonacci number
;27777890035288 is a Fibonacci number
;44945570212853 is a Fibonacci number
;72723460248141 is a Fibonacci number
;117669030460994 is a Fibonacci number
;190392490709135 is a Fibonacci number
;308061521170129 is a Fibonacci number
;498454011879264 is a Fibonacci number
;806515533049393 is a Fibonacci number
;1304969544928657 is a Fibonacci number
;2111485077978050 is a Fibonacci number
;3416454622906707 is a Fibonacci number
;5527939700884757 is a Fibonacci number
;8944394323791464 is a Fibonacci number
;14472334024676221 is a Fibonacci number
;23416728348467685 is a Fibonacci number
;37889062373143906 is a Fibonacci number
;61305790721611591 is a Fibonacci number
;99194853094755497 is a Fibonacci number
;160500643816367088 is a Fibonacci number
;259695496911122585 is a Fibonacci number
;420196140727489673 is a Fibonacci number
;679891637638612258 is a Fibonacci number
;1100087778366101931 is a Fibonacci number
;1779979416004714189 is a Fibonacci number
;2880067194370816120 is a Fibonacci number
;4660046610375530309 is a Fibonacci number
;7540113804746346429 is a Fibonacci number
;12200160415121876738 is a Fibonacci number
;19740274219868223167 is a Fibonacci number
;31940434634990099905 is a Fibonacci number
;51680708854858323072 is a Fibonacci number
;83621143489848422977 is a Fibonacci number
;135301852344706746049 is a Fibonacci number
;218922995834555169026 is a Fibonacci number
;354224848179261915075 is a Fibonacci number
;573147844013817084101 is a Fibonacci number
;927372692193078999176 is a Fibonacci number
;1500520536206896083277 is a Fibonacci number
;2427893228399975082453 is a Fibonacci number
;3928413764606871165730 is a Fibonacci number
;6356306993006846248183 is a Fibonacci number
;10284720757613717413913 is a Fibonacci number
;16641027750620563662096 is a Fibonacci number
;26925748508234281076009 is a Fibonacci number
;43566776258854844738105 is a Fibonacci number
;70492524767089125814114 is a Fibonacci number
;114059301025943970552219 is a Fibonacci number
;184551825793033096366333 is a Fibonacci number
;298611126818977066918552 is a Fibonacci number
;483162952612010163284885 is a Fibonacci number
;781774079430987230203437 is a Fibonacci number
;1264937032042997393488322 is a Fibonacci number
;2046711111473984623691759 is a Fibonacci number
;3311648143516982017180081 is a Fibonacci number