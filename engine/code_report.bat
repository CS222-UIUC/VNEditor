@echo off
echo run linter script, please wait...
black ./
echo generating linter and coverage report
>code_report.txt (
  echo Generated In: %date% %time%
  echo LINTER REPORT
  echo:
  echo check ./engine
  pylint ./engine --rcfile=./lint_disable.rc
  echo check ./module
  pylint ./module --rcfile=./lint_disable.rc
  echo check ./utils
  pylint ./utils --rcfile=./lint_disable.rc
  echo check server.py
  pylint server.py --rcfile=./lint_disable.rc
  echo COVERAGE REPORT
  echo:
  cd test
  coverage run -m unittest game_slot_test.py
  coverage run -m unittest db_manager_test.py
  coverage run -m unittest engine_test.py
  coverage run -m unittest config_manager_test.py
  coverage report -m
)
echo code result been pushed into 'code_report.txt'
pause