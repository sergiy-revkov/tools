!ifndef __TRACER__
!define __TRACER__

!define LOG_FILE_NAME "$DESKTOP\operations_log.txt"
!define INTERNAL_DEBUGPRINT `System::Call kernel32::OutputDebugString(ts)`

!define DebugPrint '!insertmacro DebugPrint'
!macro DebugPrint DpMsg
	Push "${DpMsg}"
	Call DebugPrint
!macroend



var dp_msg
Function DebugPrint
	Pop $dp_msg
	FileOpen $0 ${LOG_FILE_NAME} a
	FileSeek $0 0 END
	FileWrite $0 "$dp_msg$\r$\n"
	FileClose $0

	${INTERNAL_DEBUGPRINT} "$dp_msg"
FunctionEnd

!endif
