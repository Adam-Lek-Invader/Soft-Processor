0: movi R4, 0b00000001 //zapala LED0 ins=0 0cykli
1: movi R0, 207		//do przepelnienia 255+1=0 | 2ins => 49 iteracji i odrazu dodanie 0-(50-1)=255-48=207
2: addi R0, R0, 1
3: jnz R0, 2	//for 1s
4: movi R4, 0b00000010
5: andi R0, R5, 0x1	//przygotowanie do przyrownania czy sw0 - przypisanie obecnych stanow	POCZ PETL
6: jnz R0, 10	//skok jesli jest 1
7: andi R0, R5, 0x1
8: jz R0, 7	//powrot do poczatku while gdy bylo 0
9: jnz R0, 12	//skok poza petle while wszystkie 
10:andi R0, R5, 0x1	//petla 1 - sw bylo 1
11:jnz R0, 10			//while R5 != 0											//KONIEC PETL
12:movi R4, 0b00000100 //zapala LED0 0cykli
13:movi R0, 207		//do przepelnienia 255+1=0 | 2ins => 49 iteracji i odrazu dodanie 0-(50-1)=255-48=207
14:addi R0, R0 1
15:jnz R0, 14	//for 1s
16:movi R4, 0b00001000
17: andi R0, R5, 0x2	//przygotowanie do przyrownania czy sw1 - przypisanie obecnych stanow	POCZ PETL
18: jnz R0, 22	//skok do while == 1 jesli jest 1
19: andi R0, R5, 0x2	//gdy sw1 bylo 0
20: jz R0, 19	//powrot do poczatku while gdy bylo 0
21: jnz R0, 24	//skok poza petle while wszystkie 
22:andi R0, R5, 0x2	//petla 1 - sw bylo 1
23:jnz R0, 22			//while R5 != 0											//KONIEC PETL
24:jumpi 0 //RESTART