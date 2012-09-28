import os.path
import subprocess
import re


depFile = os.path.join(os.getcwd(),'dependencyList.txt')
if os.path.isfile(depFile):
	print 'processing dependencies file: ' + os.path.normpath(depFile)
	depVersions = ''
else:
	exit(1)

# loop over lines in file and request info for each
f=open(depFile,'r')
dr=None
for line in f:
	# check if line starts with *, this indicates that the
	# dependency is optional (not required on every system).
	# In this case, we'll check below whether it is present to
	# avoid fail if it isn't
	if line[0]=='*':
		qNotRequired = True
		line = line[1:].strip() # remove * and strip whitespace
	else:
		qNotRequired = False
		line = line[0:].strip() # strip whitespace
	
	# check line isn't empty
	if not line:
		continue

	# create branch location
	branchLoc = os.path.normpath(os.path.join(os.getcwd(),line))

	# if not required to exist, skip if doesn't exist
	if qNotRequired and not os.path.isdir(branchLoc):
		continue
	
	# detect if SVN
	if os.path.isdir(os.path.join(branchLoc,'.svn')):
		# run subprocess to run svnversion to get revision of
		# svn branch
		revNo = subprocess.Popen(["svnversion"], cwd=branchLoc, stdout=subprocess.PIPE).communicate()[0].strip()
		CVS = 'SVN'
	
	elif os.path.isdir(os.path.join(branchLoc,'.bzr')):
		# run subprocess to run bzr revno to get revision of branch
		revNo = subprocess.Popen(["bzr", "revno"], cwd=branchLoc, stdout=subprocess.PIPE).communicate()[0].strip()
		CVS = 'BZR'

	elif os.path.isdir(os.path.join(branchLoc,'.git')):
		# run subprocess to run git to get revision of branch
		revNo = subprocess.Popen(["git", "--git-dir", os.path.join(branchLoc,'.git'), "rev-parse", "HEAD"], stdout=subprocess.PIPE).communicate()[0].strip()
		isDirty = subprocess.call(["git", "diff", "--quiet"], cwd=branchLoc)
		if isDirty:
			revNo += ' *DIRTY*'
		CVS = 'GIT'
	
	else:
		raise RuntimeError("cannot determine type of repo '%s'" % branchLoc)
	
	# open file only here if so we don't have one if there's nothing to write
	if dr is None:
		dr = open(".dep_revs", "w")

	print '  ' + CVS + ': ' + line + ': rev. ' + revNo
	dr.write(line + '\t' + CVS + '\t' + revNo + '\n')

f.close()
if dr is not None:
	dr.close()
else:
	print '  empty...'
	exit(1)	# signal no .dep_revs was created
