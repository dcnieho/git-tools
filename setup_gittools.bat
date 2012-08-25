@echo off
xcopy pre-commit ..\.git\hooks /Y

:: now cd to parent and add a git command to run script that sets all dependencies to expected version

cd ..

git config alias.getdeps "!python git-tools/checkoutDeps.py"

echo setup done, use 'git getdeps' to set all deps to expected state
