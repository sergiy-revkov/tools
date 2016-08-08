#include "stdafx.h"
#include <Windows.h>

LPCTSTR g_default_message = TEXT("dout default message");

int _tmain(int argc, _TCHAR* argv[])
{
	const TCHAR* msg = g_default_message;
	if (argc > 1)
	{
		msg = argv[1];
	}

	OutputDebugString(msg);

	return 0;
}

