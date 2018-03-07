'''parser.py: parses through files, unzips them and extracts important pieces of data according to rules predefined
_author_	= Sigal Sax
_date_ 		= July 2017
_version_ 	= Python 2.7
'''
import os
import zipfile
import py7zlib
import re
import sys
from string import whitespace
def printFileName(f):
	print(f)
def is_7zfile(cls, filepath):
    '''
    Class method: determine if file path points to a valid 7z archive.
    '''
    is7z = False
    fp = None
    try:
        fp = open(filepath, 'r')
        archive = py7zlib.Archive7z(fp)
        n = len(archive.getnames())
        is7z = True
    except:
		if (is7z):
			zippedPath= os.path.join(zippedPath,archive)
			walktree(zippedPath, count, pathFolder)
    return is7z

def walktree(path, count, pathFolder):
	flagMacros=""
	flagPMTerm=""
	flagVersion=""
	spawn=""
	crashedFileLog= r"C:\Users\Administrator\Desktop\crashedLog.txt"
	crashedFormatMisalignment= r"C:\Users\Administrator\Desktop\formatMisalignmentRule4.txt"
	#try:
	fldr= os.listdir(path)
	mylist = os.listdir(path)
	subPath=""
	for f in fldr:
		subPath = os.path.join(path, f)
	#	if (f.endswith(".7z")):
		#	zipfile.ZipFile.extractall(f)
		#	print("HELLO 7ZIP")
		#	archive = py7zlib.Archive7z(f)
		#	names = archive.filenames

		if f.endswith(".zip"):
			try:
				zip_ref = zipfile.ZipFile(subPath, 'r')
				#	extract returns the path
				zip_ref.extractall(path)
				fileName = os.path.splitext(f)[0]
				if fileName in str(mylist):
					zippedPath= os.path.join(path, fileName)
					walktree(zippedPath, count, pathFolder)
			except:
				print(os.path.join(path, f))
				text_file= open(crashedFileLog, 'a')
				text_file.write(os.path.join(path, f) + " ### Unable to unzip folder ### \n")
				text_file.close()
				continue

		elif is_7zfile(f, subPath):
			print("I am 7zip")

		elif os.path.isdir(subPath):
			count+=1
			walktree(subPath, count, pathFolder)
		else:
			if (f.endswith(".txt") or f.endswith(".au3") or f.endswith(".docx") or f.endswith(".iim") or f.endswith(".vbs")
			 	or f.endswith(".ini") or f.endswith(".dll") or f.endswith(".exe") or f.endswith(".msi") or f.endswith(".xml")
				or f.startswith(".")  or f.endswith(".pdf") or f.endswith(".xpi") or f.endswith(".js") or f.endswith(".pdb")):
				print(os.path.relpath(subPath, f))

	if ruleZero(mylist):
		flagPMTerm= "PMTerminalPlugin"
		print(flagPMTerm)
		if ruleFive(mylist, subPath):
			print("RULE 5")
	if ruleOne(mylist):
		flagMacros= "iMacrosPlugin" #write to file that this plugin is iMacros
		print(flagMacros)
	if ruleTwo(mylist):
		flagVersion="Version 8+"
		print(flagVersion)

	if ruleThree(mylist, subPath)!= -1:
		print("Rule Three")
	if ruleFour(mylist, subPath, crashedFormatMisalignment):
		print("Rule Four")
'''
except:
	text_file= open(crashedFileLog, 'w')
	text_file.write(subPath)
	text_file.close()
	sys.exit("I found a file I was unable to unzip")
'''
def searchFive(file, nextPath):
	for word in file.read().split("\n"):
		wordWithoutSpace=word.split(" ")
		afterEqual= wordWithoutSpace[0].split("=")
		if (afterEqual[0] == ("AllowManualChange")):
			print(afterEqual)
			answerAllowMan= afterEqual[1]
			print(answerAllowMan)
		if (afterEqual[0] == ("RCAllowManualReconciliation")):
			answerRC= afterEqual[1]
			print(answerRC)
		if (afterEqual[0] == ("VFAllowManualVerification")):
			answerVF= afterEqual[1]
			print(answerVF)

def ruleFive(mylist, subPath):
	for f in mylist:
		firstWord=filter(None, re.split("([A-Z][^A-Z]*)", f))
		nextPath=os.path.dirname(subPath)
		if (firstWord[0]==("Policy-") and f.endswith(".ini")):
			nextPath= os.path.join(nextPath, f)
			file = open(nextPath)
			searchFive(file, nextPath)
			return True
	return False

#traverse header
def searchFour (file, nextPath, crashedFormatMisalignment, f):
	header=[]
	type_Header=[]
	for line in file.read().split('#'):
		x= line.translate(None, whitespace)
		header.append(x)
		while '' in header:
			header.remove('')
	# name of product
	product=header[0]

	print("PRODUCT: ", product)
	for letter in header[1].split("."):
		type_=letter[:]
		type_Header.append(type_)

	# two different formats for Process.ini files, this part accounts for both
	# tries one format and if outofbounds, attempts second
	# if line starts with 'v'.xxx, then the date is
	try:
		if (type_Header[0].startswith("v") or type_Header[0].startswith("V")):
			version=type_Header[0]
			print("VERSION: ", version)
			date=type_Header[1]
			print("DATE: ", date)
		if (type_Header[0].isdigit()):
			print ("DATE: ", header[1])
	except:
		print(os.path.join(path, f))
		text_fileFormat= open(crashedFormatMisalignment, 'a')
		text_fileFormat.write(os.path.join(path, f) + " ### Format INCORRECT ### \n")
		text_fileFormat.close()
		pass

	try:
		headerColSplit= header[1].split(":")
		product=headerColSplit[1]
		print("PRODUCT: ", product)
		if not header[2]:
			version=("VERSION: " + "N/A")
		else:
			versionColSplit= header[2].split(":")
			version= versionColSplit[1]
			print("VERSION: ", version)
	except:
		version=("VERSION: " + "N/A")


def ruleFour(mylist, subPath, crashedFormatMisalignment):
	for f in mylist:
		words= filter(None, re.split("([A-Z][^A-Z]*)", f))
		if (words[-1]==("Process.ini")):
			nextPath=os.path.dirname(subPath)
			nextPath= os.path.join(nextPath, f)
			#nextPath+"\\"+f
			file = open(nextPath)
			searchFour (file, nextPath, crashedFormatMisalignment, f)
			return True
	return False

def searchThree(file, nextPath, target):
	for word in file.read().split(" "):
		for compare in re.findall(target, word):
			executeable = word.split("(spawn)")
			if executeable[-1].endswith(".exe") or executeable[-1].endswith(".exe\""):
				executeableInfo= executeable[-1]
				print(executeableInfo)


def ruleThree(mylist, subPath):
	for f in mylist:
		words= filter(None, re.split("([A-Z][^A-Z]*)", f))
		if (words[-1]==("Process.ini")):
			nextPath=os.path.dirname(subPath)
			nextPath= os.path.join(nextPath,f)
			print(nextPath)
			file = open(nextPath)
			searchThree(file, nextPath, "spawn")
			#searchFour (file, nextPath)
			return True
	return -1

# Version 8+
def ruleTwo(mylist):
	for f in mylist:
		firstWord=filter(None, re.split("([A-Z][^A-Z]*)", f))
		if (firstWord[0]==("Policy-") and f.endswith(".xml")):
			return True

#iMacrosPlugin
def ruleOne(mylist):
	for f in mylist:
		if f.endswith(".iim"):
			return True
		else:
			return False

#PMTerminalPlugin
def ruleZero(mylist):
	firstFlag=False
	secondFlag=False
	containsList=[]
	for f in mylist:
		lastWord=filter(None, re.split("([A-Z][^A-Z]*)", f))
		if (lastWord[-1]==("Process.ini")):
			containsList.append(lastWord[-1])
			firstFlag=True
		elif (lastWord[-1]==("Prompts.ini")):
			containsList.append(lastWord[-1])
			secondFlag=True
	if len(containsList)>=2:
		return True
	else:
		return False

if __name__ == "__main__":
	path = "C:\\Users\\Administrator\\Desktop\\"
	pathFolder= open ("C:\Users\Administrator\Desktop\crashedLog.txt", "r")
	formatRuleFour= open (r"C:\Users\Administrator\Desktop\formatMisalignmentRule4.txt", "r")
	count=0
	walktree (path, count, pathFolder)
