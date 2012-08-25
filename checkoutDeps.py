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
    # detect if SVN
    if os.path.isdir(os.path.join(branchLoc,'.svn')):
	# run svn update
	os.execlp("svn", "svn", "update", "-r%s"%args[2])
	
    elif os.path.isdir(os.path.join(branchLoc,'.bzr')):
	# run bzr 
	os.execlp("bzr", "bzr", "revert", "-r%s"%args[2], "--no-backup")

    elif os.path.isdir(os.path.join(branchLoc,'.git')):
	# run subprocess to run git to get revision of branch
        retcode = subprocess.Popen(["git", "checkout", args[2]], cwd=branchLoc)
#	retcode = subprocess.call(["git", "--git-dir=\"%s\.git\""%branchLoc, "log"])
	#retcode = subprocess.call(["git", "--git-dir=\"%s\.git\""%branchLoc, "--work-tree=\"%s\""%branchLoc, "checkout", "-q %s"%args[2]])


if retcode==0:
    print '  checkout' + args[0] + ' at rev. ' + args[2] + ' (%s)'%args[1]
else:
    raise RuntimeError('  UNSUCSESSFUL: checkout' + args[0] + ' at rev. ' + args[2] + ' (%s)'%args[1])
