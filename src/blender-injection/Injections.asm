; ASSEMBLY CODE

.DATA

    EXTERN PrepareForInvokeInterpreter : PROC

    PUBLIC InvokeForceStdOut
    PUBLIC InvokePythonInterpreter


.CODE

; Args   : (RCX, RDX) (RSI = Context)
; Restore: (RCX = QWORD PTR [RBX+08H]; RCX = QWORD PTR [RCX])
InvokeForceStdOut PROC
    SUB RSP, 28h

    MOV RCX, RSI
    CALL PrepareForInvokeInterpreter
	MOV RCX, [RBX+08h]       ; store [RBX+08h] (path of dropped file) into RCX
    MOV RCX, QWORD PTR [RCX] ; store pointer of RCX into RCX, for next instructions (overwritten)

    ADD RSP, 28h
    RET
InvokeForceStdOut ENDP

;

; Args: (RCX, RDX, R8)
InvokePythonInterpreter PROC
    SUB RSP, 28h

    MOV RAX, RCX
    MOV RCX, RDX
    MOV RDX, R8
    MOV R8 , R9
    CALL RAX

    ADD RSP, 28h
	RET
InvokePythonInterpreter ENDP

END