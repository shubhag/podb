#!/usr/bin/python
import bisect

tempCount = 0
maxitem = 32
root = "dat/podb0"

def printTofile(numKeys, isleaf, parentfilename, key, value, fname):
	f = open(fname, 'w+')
	keyvalue = str(key) + '\n'
	indexvalue = str(value) + '\n'
	data =  [str(numKeys) +'\n' , str(isleaf) + '\n', str(parentfilename) + '\n', keyvalue , indexvalue]
	f.writelines(data)
	f.closed

def printToOpenFile(numKeys, isleaf, parentfilename, keyvalue, ptrvalue, f):
	filedata = [numKeys, isleaf ,parentfilename, keyvalue, ptrvalue]
	f.seek(0)
	f.truncate()
	f.writelines(filedata)
	f.closed

def split_array(array):
    half = len(array)/2
    return array[:half], array[half:]

def searchforkey(key, value, filename, parentfilename):
	global tempCount
	global maxitem
	global root
	f = open(filename, 'r+')
	data = f.readlines()
	isleaf = data[1].rstrip()
	# parentfilename = data[2].rstrip()
	if isleaf == '1':
		keyvalue = data[3].rstrip().split(' ')
		indexvalue = data[4].rstrip().split(' ')
		numKeys = int(data[0].rstrip())
		index = bisect.bisect_left(keyvalue, key)
		keyvalue.insert(index, key)
		indexvalue.insert(index,value)
		numKeys += 1
		if numKeys <= maxitem : 
			printToOpenFile(str(numKeys) + '\n', data[1] ,data[2], ' '.join(keyvalue) + '\n', ' '.join(indexvalue) + '\n', f)
		else:
			keyvalue1, keyvalue2 = split_array(keyvalue)
			indexvalue1, indexvalue2 = split_array(indexvalue)
			numKeys1 = numKeys/2
			numKeys2 = numKeys - numKeys1
			parentKeyValue = keyvalue1[-1]
			newleaffile = 'dat/podb' + str(tempCount)
			tempCount = tempCount + 1
			if parentfilename == '-1':
				parentfilename = 'dat/podb' + str(tempCount)
				root = parentfilename
				tempCount = tempCount + 1
				printToOpenFile(str(numKeys1)+'\n', data[1],parentfilename + '\n',' '.join(keyvalue1) + '\n' , ' '.join(indexvalue1) + '\n' , f )
				printTofile(numKeys2,1,parentfilename,' '.join(keyvalue2), ' '.join(indexvalue2), newleaffile)
				printTofile(1,0,-1,parentKeyValue, filename + ' ' + newleaffile, parentfilename )
			else:
				printToOpenFile(str(numKeys1) + '\n', data[1] ,parentfilename +'\n', ' '.join(keyvalue1) + '\n', ' '.join(indexvalue1) + '\n', f)
				printTofile(numKeys2,1,parentfilename,' '.join(keyvalue2), ' '.join(indexvalue2), newleaffile)
				# print filename, newleaffile, parentKeyValue , parentfilename , "63", numKeys
				recurBreak(filename, newleaffile, parentKeyValue, parentfilename)
	else:
		keyvalue = data[3].rstrip().split(' ')
		ptrvalue = data[4].rstrip().split(' ')
		index = bisect.bisect_left(keyvalue, key)
		ptr = ptrvalue[index]
		# if ptr != 'NULL':
		f.closed
		print key, value, ptr , "71"
		searchforkey(key, value, ptr, parentfilename)
		# else:
		# 	print True
		# 	leaffile = 'podb' + str(tempCount)
		# 	tempCount += 1
		# 	ptrvalue[index] = leaffile
		# 	printToOpenFile(data[0], data[1] ,data[2], ' '.join(keyvalue) + '\n', ' '.join(ptrvalue) + '\n', f)
		# 	printTofile(1,1,filename,key, value, leaffile)

def recurBreak(leafl, leafr, key, filename ):
	global maxitem
	global tempCount
	global root
	f = open(filename, 'r+')
	data = f.readlines()
	numKeys = int(data[0].rstrip()) + 1
	keyvalue = data[3].rstrip().split(' ')
	ptrvalue = data[4].rstrip().split(' ')
	print ptrvalue, leafl, leafr, "90"
	index = ptrvalue.index(leafl)
	keyvalue.insert(index, key)
	ptrvalue.insert(index+1, leafr)
	#print index, keyvalue, ptrvalue, leafl, leafr, key
	if numKeys <= maxitem:
		printToOpenFile(str(numKeys) + '\n', data[1] ,data[2], ' '.join(keyvalue)+'\n', ' '.join(ptrvalue) + '\n', f)
	else:
		length = len(keyvalue)
		parentKeyValue = keyvalue.pop(length/2);
		length = len(keyvalue)
		keyvalue1, keyvalue2 = split_array(keyvalue)
		ptrvalue1, ptrvalue2 = split_array(ptrvalue)
		# print keyvalue1, keyvalue2, ptrvalue1, ptrvalue2
		numKeys1 = len(keyvalue1)
		numKeys2 = len(keyvalue2)
		siblingfile = 'dat/podb' + str(tempCount)
		tempCount = tempCount + 1
		parentfilename = data[2].rstrip()
		if parentfilename != '-1':
			printToOpenFile(str(numKeys1) + '\n', data[1] ,data[2], ' '.join(keyvalue1) + '\n', ' '.join(ptrvalue1) + '\n', f)
			printTofile(numKeys2,0,data[2].rstrip(),' '.join(keyvalue2), ' '.join(ptrvalue2), siblingfile)
			recurBreak(filename, siblingfile, parentKeyValue, parentfilename)
		else:
			parentfilename = 'dat/podb' + str(tempCount)
			root = parentfilename
			tempCount = tempCount + 1
			printToOpenFile(str(numKeys1)+'\n', data[1],parentfilename + '\n',' '.join(keyvalue1) + '\n' , ' '.join(ptrvalue1) + '\n' , f )
			printTofile(numKeys2,0,parentfilename,' '.join(keyvalue2), ' '.join(ptrvalue2), siblingfile)
			printTofile(1,0,-1,parentKeyValue, filename + ' ' + siblingfile, parentfilename )

def insert(key,value):
	global tempCount
	global root
	if tempCount == 0 :
		rootfile = 'dat/podb' + str(tempCount)
		tempCount = tempCount + 1
		printTofile(1,1,-1,key, value, rootfile)
	else:
		print root, key, value , "127"
		searchforkey(key, value, root, '-1')

if __name__ == '__main__':
	# insert('1','aasfd')
	# insert('2','as')	
	# insert('1.5','as')	
	# insert('0.5','as')	
	# insert('3','ffd')
	# insert('1','aasfd')
	# print root
	a = 0 
	with open("assgn2_bplus_data.txt", "r") as queryfile:
		for line in queryfile:
			a += 1
			indices = line.rstrip().split('\t')
			# if indices[0] == '0':
			# 	print a
			insert(indices[0], indices[1])