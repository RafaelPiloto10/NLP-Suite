@echo off
setlocal
ECHO STEP3 will setup a shortcut that by typing NLP in command line/prompt will 1. activate the NLP python environment and 2. change the directory to the NLP/src directory.
echo(
:PROMPT
SET /P AREYOUSURE=Do you wish to continue? [y/n]
IF /I "%AREYOUSURE%" NEQ "y" GOTO END
@echo off
cd %~dp0 && python "..\src\NLP_setup_shortcut_add.py"
:PROMPT
echo(
ECHO Installation completed!
ECHO The NLP shortcut has been added to the environment variables.
ECHO Double click on NLP_environment_shortcut_remove.bat to remove the shortcut.
echo(
SET /P ENDPROMPT=Press Return to close this window
EXIT 0
