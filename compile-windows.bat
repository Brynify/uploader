pyinstaller --clean --win-private-assemblies -F -w uploader.py
xcopy oggenc2.exe dist\oggenc2.exe
pause