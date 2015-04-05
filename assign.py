#!/usr/bin/python
import bisect

tempCount = 0 
root = "dat/podb0"

def printTofile(numKeys, isleaf, key, value, fname):
	f = open(fname, 'w+')
	keyvalue = str(key) + '\n'
	indexvalue = str(value) + '\n'
	data =  [str(numKeys) +'\n' , str(isleaf) + '\n', keyvalue , indexvalue]
	f.writelines(data)
	f.closed

def printToLeaffile(numKeys, isleaf, key, value, sibling, fname):
	f = open(fname, 'w+')
	keyvalue = str(key) + '\n'
	indexvalue = str(value) + '\n'
	siblingFile = str(sibling) + '\n'
	data =  [str(numKeys) +'\n' , str(isleaf) + '\n', keyvalue , indexvalue, siblingFile]
	f.writelines(data)
	f.closed

def printToOpenFile(numKeys, isleaf, keyvalue, ptrvalue, f):
	filedata = [numKeys, isleaf ,keyvalue, ptrvalue]
	f.seek(0)
	f.truncate()
	f.writelines(filedata)
	f.closed

def printToOpenLeafFile(numKeys, isleaf, keyvalue, ptrvalue,sibling, f):
	filedata = [numKeys, isleaf ,keyvalue, ptrvalue, sibling]
	f.seek(0)
	f.truncate()
	f.writelines(filedata)
	f.closed

def split_array(array):
    half = len(array)/2
    return array[:half], array[half:]

def insert(key,value, filename):
	global tempCount
	global maxitem
	global root
	global filename1
	global filename2
	if tempCount == 0 :
		rootfile = 'dat/podb' + str(tempCount)
		tempCount = tempCount + 1
		root = rootfile
		printToLeaffile(1,1,key, value,-1, rootfile)
		return -1
	else:
		f = open(filename, 'r+')
		data = f.readlines()
		isleaf = data[1].rstrip()
		if isleaf == '1':
			keyvalue = data[2].rstrip().split(' ')
			indexvalue = data[3].rstrip().split(' ')
			numKeys = int(data[0].rstrip())
			index = bisect.bisect_left(keyvalue, key)
			keyvalue.insert(index, key)
			indexvalue.insert(index,value)
			numKeys += 1
			if numKeys <= maxitem :
				printToOpenLeafFile(str(numKeys) + '\n', data[1], ' '.join(keyvalue)+ '\n', ' '.join(indexvalue) + '\n', data[4],f)			
				return -1
			else:
				keyvalue1, keyvalue2 = split_array(keyvalue)
				indexvalue1, indexvalue2 = split_array(indexvalue)
				numKeys1 = numKeys/2
				numKeys2 = numKeys - numKeys1
				parentKeyValue = keyvalue1[-1]
				newleaffile = 'dat/podb' + str(tempCount)
				tempCount = tempCount + 1
				printToOpenLeafFile(str(numKeys1)+'\n', data[1],' '.join(keyvalue1) + '\n' , ' '.join(indexvalue1) + '\n' ,newleaffile+'\n', f )
				printToLeaffile(numKeys2,1,' '.join(keyvalue2), ' '.join(indexvalue2), data[4].rstrip(), newleaffile)
				if root == 'dat/podb0':
					parentfilename = 'dat/podb' + str(tempCount)
					root = parentfilename
					tempCount = tempCount + 1
					printTofile(1,0, parentKeyValue, filename + ' ' + newleaffile, parentfilename )
					return -1
				else :
					filename1 = filename
					filename2 = newleaffile
					return parentKeyValue
		else:
			keyvalue = data[2].rstrip().split(' ')
			ptrvalue = data[3].rstrip().split(' ')
			index = bisect.bisect_left(keyvalue, key)
			ptr = ptrvalue[index]
			f.closed
			returnvalue = insert(key, value, ptr)
			if returnvalue != -1 :
				f = open(filename, 'r+')
				data = f.readlines()
				numKeys = int(data[0].rstrip()) + 1
				keyvalue = data[2].rstrip().split(' ')
				ptrvalue = data[3].rstrip().split(' ')
				index = bisect.bisect_left(keyvalue, returnvalue)
				keyvalue.insert(index, returnvalue)
				ptrvalue[index] = filename1
				ptrvalue.insert(index+1, filename2)
				if numKeys <= maxitem:
					printToOpenFile(str(numKeys) + '\n', data[1], ' '.join(keyvalue)+'\n', ' '.join(ptrvalue) + '\n', f)
					return -1
				else:
					parentKeyValue = keyvalue.pop(len(keyvalue)/2)
					length = len(keyvalue)
					keyvalue1, keyvalue2 = split_array(keyvalue)
					ptrvalue1, ptrvalue2 = split_array(ptrvalue)
					numKeys1 = len(keyvalue1)
					numKeys2 = len(keyvalue2)
					siblingfile = 'dat/podb' + str(tempCount)
					tempCount = tempCount + 1
					if root != filename :
						printToOpenFile(str(numKeys1) + '\n', data[1] , ' '.join(keyvalue1) + '\n', ' '.join(ptrvalue1) + '\n', f)
						printTofile(numKeys2,0,' '.join(keyvalue2), ' '.join(ptrvalue2), siblingfile)
						filename1 = filename
						filename2 = siblingfile
						return parentKeyValue
					else:
						parentfilename = 'dat/podb' + str(tempCount)
						root = parentfilename
						tempCount = tempCount + 1
						printToOpenFile(str(numKeys1)+'\n', data[1],' '.join(keyvalue1) + '\n' , ' '.join(ptrvalue1) + '\n' , f )
						printTofile(numKeys2,0,' '.join(keyvalue2), ' '.join(ptrvalue2), siblingfile)
						printTofile(1,0,parentKeyValue, filename + ' ' + siblingfile, parentfilename )
						return -1
			else:
				return -1

def queryKey(key, filename):
	global tempCount
	if tempCount == 0 :
		print "No data inserted at all"
		return
	f = open(filename, 'r+')
	data = f.readlines()
	isleaf = data[1].rstrip()
	keyvalue = data[2].rstrip().split(' ')
	idxvalue = data[3].rstrip().split(' ')
	if isleaf == '1':
		if keyvalue.count(key):
			index = bisect.bisect_left(keyvalue, key)
			print '1', keyvalue[index] , idxvalue[index]
		else:
			print "Not present"
	else:
		index = bisect.bisect_left(keyvalue, key)
		queryKey(key, idxvalue[index])
	f.closed

def searchFile(key, rKey, filename):
	f = open(filename, 'r+')
	data = f.readlines()
	isleaf = data[1].rstrip()
	keyvalue = data[2].rstrip().split(' ')
	idxvalue = data[3].rstrip().split(' ')
	if isleaf == '1':
		index1 = bisect.bisect_left(keyvalue, key)
		index2 = bisect.bisect_right(keyvalue, rKey)
		i = index1
		while i < len(keyvalue) and i < index2 :
			print keyvalue[i] +'\t'+idxvalue[i]
			i += 1
		f.closed
		if index1 == len(keyvalue):
			print "No results found"
		if index2 == len(keyvalue):
			return '-1'
		else:
			return data[4].rstrip() 
	else:
		index = bisect.bisect_left(keyvalue, key)
		f.closed
		return searchFile(key, rKey, idxvalue[index])

def queryTillRight(qright, filename):
	f = open(filename, 'r+')
	data = f.readlines()
	isleaf = data[1].rstrip()
	keyvalue = data[2].rstrip().split(' ')
	idxvalue = data[3].rstrip().split(' ')
	if isleaf == '1':
		index = bisect.bisect_right(keyvalue, qright)
		i = 0
		while i < len(keyvalue) and i < index :
			print keyvalue[i] +'\t'+idxvalue[i]
			i += 1
		f.closed
		if index == len(keyvalue):
			return '-1'
		else:
			return data[4].rstrip()
	else:
		print "Something went wrong"
		return '-1'

def rangeQuery(qcenter, qrange ):
	global tempCount
	if tempCount == 0 :
		print "No data inserted at all"
		return
	queryLeft = str( float(qcenter) - float(qrange) )
	queryRight = str( float(qcenter) + float(qrange) )
	filename = searchFile(queryLeft, queryRight,  root)
	while filename != '-1' :
		filename = queryTillRight(queryRight,filename)

if __name__ == '__main__':
	f = open('bplustree.config', 'r')
	data = f.readline()
	maxitem = int(data.rstrip())
	f.close()
	a = 0 
	filename1 = -1
	filename2 = -1

	# with open("assgn2_bplus_data.txt", "r") as queryfile:
	# 	for line in queryfile:
	# 		a +=1
	# 		# print a
	# 		indices = line.rstrip().split('\t')
	# 		# print indices[0], indices[1]
	# 		insert(indices[0], indices[1],root)
	# querycount = 0
	# with open("assgn2_bplus_data.txt", "r") as queryfile:
	# 	for line in queryfile:
	# 		# a +=1
	# 		# print a
	# 		indices = line.rstrip().split('\t')
	# 		# print indices[0], indices[1]
	# 		queryKey(indices[0], root)
	a = 0
	with open("querysample.txt", "r") as queryfile:
		for line in queryfile:
			a+=1 
			print a
			indices = line.rstrip().split('\t')
			if indices[0] == '0':
				insert(indices[1], indices[2],root)
				print "Inserted"
			elif indices[0] == '1':
				queryKey(indices[1], root)
			elif indices[0] == '2':
				rangeQuery(indices[1], indices[2])
			else:
				print "Inappropriate query type"
