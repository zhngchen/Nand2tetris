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

(LOOP)
@SCREEN
D = A
@addr
M = D    // addr = SCREEN

@color
M = 0   // color = 0 (white)

@KBD
D = M
@DISPLAY
D;JEQ   // if KBD = 0 goto DISPLAY

@color
M = -1  // if KBD != 0   color = 1 then DISPLAY

(DISPLAY)
@8192
D = A
@SCREEN
D = D + A
@addr
D = D - M
@LOOP
D;JEQ     // if addr = 8192 + SCREEN then goto LOOP

@color
D = M
@addr
A = M
M = D  // RAM[addr] = color

@addr
M = M + 1  // addr += 1

@DISPLAY
0;JMP    // goto DISPLAY(infinite loop)






