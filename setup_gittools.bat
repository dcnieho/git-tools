@echo off
IF EXIST ..\.git\hooks (
    xcopy pre-commit ..\.git\hooks /Y
) ELSE (
    :: note, if ..\.git is a file, it contains the link to where the real .git folder can be found. so <that link>\hooks is where we should copy to in that case
    echo !!you need to copy pre-commit by hand to .git/modules/^<module name^>/hooks
)

:: now cd to parent and add a git command to run script that sets all dependencies to expected version

cd ..

git config alias.getdeps "!python git-tools/checkoutDeps.py"

echo setup done, use 'git getdeps' to set all deps to expected state
