for /f %%i in ('dir /s /b bank\migrations\*.py ^| findstr /vile "*__init__.py"') do dir /s /b "%%i"
pause