 
setlocal enabledelayedexpansion

for /f "delims=" %%a in ('dir /b Zip*') do (
   set filename=%%a 
   set dirname=!filename:~0,-4!
   md !dirname! >nul 2>&1 
   echo  "%%a"
   echo  filename
  expand -r "%%a"  filename
)

endlocal