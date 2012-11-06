:: it is assumed that this is run 
@echo off

for /f %%a in ('git rev-parse HEAD') do @set refid=%%a
echo git refid: "%refid%"

:: see if git_refid.h already exists and if it needs to be updated
if exist git_refid.h (
    :: read and check if needs to be updated
    set /p old_file=<git_refid.h
    goto :checkfile) else (
    goto :writefile)

:checkfile
if %old_file:~18,-1% EQU "%refid%" (
    :: no need to update, we're done
    goto :eof)

:: write refid as preproc defined string in header file
:writefile
echo #define GIT_REFID "%refid%" > git_refid.h
