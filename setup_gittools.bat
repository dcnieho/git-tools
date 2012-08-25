@echo off


IF EXIST ..\.git\hooks (
    xcopy pre-commit ..\.git\hooks /Y
    goto :setupDeps
) ELSE IF EXIST ..\.git (
    SET /p gitLink=<..\.git
)

IF "%gitLink%" EQU "" (
    echo !! cannot resolve location to put pre-commit hook, do it manually
    goto:setupDeps
)
:: build path to copy to
SET gitLink=../%gitLink:~8%/hooks
SET gitLink=%gitLink:/=\%
xcopy pre-commit %gitLink% /Y


:setupDeps
:: now cd to parent and add a git command to run script that sets all dependencies to expected version
cd ..
git config alias.getdeps "!python git-tools/checkoutDeps.py"

echo setup done, use 'git getdeps' to set all deps to expected state
