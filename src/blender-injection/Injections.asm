; ASSEMBLY CODE

.DATA

    EXTERN DropEventHookCallback : PROC
    EXTERN View3DImaEmptyDropPollHookCallback : PROC

    PUBLIC DropEventHook
    PUBLIC View3DImaEmptyDropPollHook

.CODE

; x64 calling convention
; https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention

; x64 ABI convertion
; https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions

; x64 register convention
; https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/x64-architecture#registers

; Hooking print("drop file: %s", ...) in wm_window.c
;
; Args    : (RCX, RDX) (RSI = bContext, RDI = wmWindow)
; Restore : (RCX = QWORD PTR [RBX+08H]; RCX = QWORD PTR [RCX])
DropEventHook PROC
    SUB  RSP, 28h

    MOV  RCX, RSI
    MOV  R8, RDX
    MOV  RDX, RDI
    CALL DropEventHookCallback
    MOV  RCX, [RBX+08h]       ; store [RBX+08h] (path of dropped file) into RCX
    MOV  RCX, QWORD PTR [RCX] ; store pointer of RCX into RCX, for next instructions (overwritten)

    ADD  RSP, 28h
    RET

    INT  3
    INT  3

DropEventHook ENDP

; Hooking view3d_ima_empty_drop_poll(bContext *C, wmDrag *draw, const wmEvent *event)
;
; Args    : (RCX, RDX, R8)
; Restore : if dropped file is supported, returns true, otherwise; returns false.

; Original Assembly
;
; STATEMENT:
;     MOV  QWORD PTR [RSP+08h], RBX
;     PUSH RDI
;     SUB  RSP, 20h
;     MOV  RBX, R8
;     MOV  RDI, RCX
;
;     CALL view3d_ima_drop_poll
;     TEST AL, AL
;     JZ   RET_FALSE
;
;     LEA  RDX, QWORD PTR [RBX+1Ch]
;     MOV  RCX, RDI
;
;     CALL ED_view3d_give_object_under_cursor
;     TEST RAX, RAX
;     JZ   RET_TRUE
;
;     CMP  WORD PTR [RAX+000000E0h], 0000h
;     JNZ  RET_FALSE
;
;     CMP  WORD PTR [RAX+000003FFh], 00000008h
;     JNZ  RET_FALSE
;
; RET_TRUE:
;     MOV  AL, 01h
;     MOV  RBX, QWIRD PTR [RSP+30h]
;     ADD  RSP, 20h
;     POP  RDI
;     RET
;
; RET_FALSE:
;     MOV  RBX, QWORD PTR [RSP+30h]
;     XOR  AL, AL
;     ADD  RSP, 20h
;     POP  RDI
;     RET
View3DImaEmptyDropPollHook PROC
    MOV  QWORD PTR [RSP+08h], RBX
    PUSH RDI
    SUB  RSP, 20h
    MOV  RBX, R8
    MOV  RDI, RCX

    CALL View3DImaEmptyDropPollHookCallback
    TEST AL, AL
    JZ   RET_FALSE

    ; Return When True
RET_TRUE:
    MOV  AL, 01h
    MOV  RBX, QWORD PTR [RSP+30h]
    ADD  RSP, 20h
    POP  RDI
    RET

    ; Return When False
RET_FALSE:
    MOV  RBX, QWORD PTR [RSP+30h]
    XOR  AL, AL   ; equals to MOV AL, 00h
    ADD  RSP, 20h
    POP  RDI
    RET

View3DImaEmptyDropPollHook ENDP


END