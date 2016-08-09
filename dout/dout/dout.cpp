#include "stdafx.h"
#include <Windows.h>

LPCTSTR g_default_message = TEXT("dout was installed successfully.");

int install_itself();

int _tmain(int argc, _TCHAR* argv[])
{
	const TCHAR* msg = g_default_message;

	if (argc > 1)
	{
		msg = argv[1];
	} 
	else
	{
		if (install_itself() != ERROR_SUCCESS)
		{
			OutputDebugString(TEXT("dout: failed to self install"));
		}
		else
		{
			MessageBox(NULL, msg, TEXT("dout"), 0);
		}
	}

	OutputDebugString(msg);

	return 0;
}

