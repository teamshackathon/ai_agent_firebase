setlocal enabledelayedexpansion

REM Get the current timestamp
for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
    set hour=%%a
    set minute=%%b
    set second=%%c
    set millisecond=%%d
)
set timestamp=%date%_%hour%-%minute%-%second%-%millisecond%

REM Remove invalid characters from the timestamp
set timestamp=%timestamp:/=-%
set timestamp=%timestamp::=-%
set timestamp=%timestamp: =%

REM Create a directory with the timestamp
set export_dir=./seeds/%timestamp%
mkdir "%export_dir%"

REM Export Firebase emulator data to the new directory
firebase emulators:export "%export_dir%" --project manabiyaai

endlocal