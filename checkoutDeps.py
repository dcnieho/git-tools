import os.path
import subprocess

depFile = os.path.join(os.getcwd(),'.dep_revs')
if os.path.isfile(depFile):
    print 'processing dependencies file: ' + os.path.normpath(depFile)
    depVersions = ''
else:
    print 'nothing to do, file .dep_revs not found'
    exit(0)

# loop over lines in file and request info for each
f=open(depFile,'r')
for line in f:
    line = line.strip() # strip whitespace
    args = line.split('\t')

    # create branch location
    branchLoc = os.path.normpath(os.path.join(os.getcwd(),args[0]))

    # check if exists
    if not os.path.isdir(branchLoc):
        raise RuntimeError("repo does not exist: '%s'" % branchLoc)
    
    # now issue checkout/update/etc command
    print '  checkout ' + args[0] + ' at rev. ' + args[2] + ' (%s)'%args[1]
    # detect which VCS
    if os.path.isdir(os.path.join(branchLoc,'.svn')) and args[1]=='SVN':
	# run svn update
	proc = subprocess.Popen(["svn", "update", "-r%s"%args[2]], cwd=branchLoc)
	
    elif os.path.isdir(os.path.join(branchLoc,'.bzr')) and args[1]=='BZR':
	# run bzr 
	proc = subprocess.Popen(["bzr", "revert", "-r%s"%args[2], "--no-backup"], cwd=branchLoc)

    elif os.path.isdir(os.path.join(branchLoc,'.git')) and args[1]=='GIT':
	# run subprocess to run git to get revision of branch
        proc = subprocess.Popen(["git", "checkout", "-q", args[2]], cwd=branchLoc)
    
    proc.wait()

    if proc.returncode==0:
        print '    OK'
    else:
        raise RuntimeError('  UNSUCSESSFUL: checkout ' + args[0] + ' at rev. ' + args[2] + ' (%s)'%args[1])

exit(0)
