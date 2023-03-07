@echo off
black ./
echo start pylinter to check format...
>linter_result.txt (
  echo Generated In: %date% %time%
  echo:
  echo check ./engine
  pylint ./engine
  echo check ./module
  pylint ./module
  echo check ./utils
  pylint ./utils
)
echo linter result been pushed into 'linter_result.txt'
pause