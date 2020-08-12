// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// repeative code.can be avoided with varialbe to control color wanted to display
(LOOP)
@SCREEN
D = A
@addr
M = D   // addr = SCREEN

@KBD
D = M
@ALL_WHITE
D;JEQ         // if KBD = 0;screen is white

@ALL_BLACK
D;JNE        // if KBD != 0; screen is black


(ALL_WHITE)
@8192
D = A
@SCREEN
D = D + A
@addr
D = D - M
@LOOP
D;JEQ  // if addr = 8192 + SCREEN goto LOOP

@addr
A = M
M = 0  // RAM[addr] = 0

@addr
M = M + 1   // addr += 1

@ALL_WHITE
0;JMP


(ALL_BLACK)
@8192
D = A
@SCREEN
D = D + A
@addr
D = D - M
@LOOP
D;JEQ  // if addr = 8192+SCREEN goto LOOP

@addr
A = M
M = -1  // RAM[addr] = 0

@addr
M = M + 1   // addr += 1

@ALL_BLACK
0;JMP
