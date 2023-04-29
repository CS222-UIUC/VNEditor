@echo off
echo run linter script, please wait...
black ./
echo generating linter and coverage report...
>code_report.txt (
  echo Generated In: %date% %time%
  echo LINTER REPORT
  echo:
  echo check ./kernel
  pylint ./kernel --rcfile=./lint_disable.rc
  echo check ./module
  pylint ./module --rcfile=./lint_disable.rc
  echo check ./utils
  pylint ./utils --rcfile=./lint_disable.rc
  echo check server.py
  pylint server.py --rcfile=./lint_disable.rc
  echo COVERAGE REPORT
  echo:
  cd test
  coverage run -m -a unittest test_config_manager.py
  coverage run -m -a unittest test_db_manager.py
  coverage run -m -a unittest test_file_utils.py
  coverage run -m -a unittest test_game_slot.py
  coverage run -m -a unittest test_engine.py
  coverage run -m -a unittest test_engine_io.py
  coverage report -m
)
echo clean directory...
del test.db
del .coverage
echo code result been pushed into 'code_report.txt'


pause