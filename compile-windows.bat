rmdir /S /Q dist
pyinstaller --clean --win-private-assemblies -F -w uploader.pyw
xcopy /Q oggenc2.exe dist\oggenc2.exe /Y
xcopy /Q /E documentation dist /Y
xcopy /Q /E lib dist /Y
rmdir /S /Q build
pause