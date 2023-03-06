@echo off
echo start linter to check format...
>linter_result.txt (
  echo Generated on: %date% %time%
  echo:

  REM YOUR LINTER TEST START HERE
  echo test 1
  echo result 1
  echo:
  echo test 2
  echo result 2
  REM YOUR LINTER TEST  END  HERE
)
echo linter result been pushed into 'linter_result.txt'
pause