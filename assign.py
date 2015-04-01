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

def printToOpenFile(numKeys, isleaf, keyvalue, ptrvalue, f):
	filedata = [numKeys, isleaf ,keyvalue, ptrvalue]
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
		printTofile(1,1,key, value, rootfile)
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
				printToOpenFile(str(numKeys) + '\n', data[1], ' '.join(keyvalue)+ '\n', ' '.join(indexvalue) + '\n', f)			
				return -1
			else:
				keyvalue1, keyvalue2 = split_array(keyvalue)
				indexvalue1, indexvalue2 = split_array(indexvalue)
				numKeys1 = numKeys/2
				numKeys2 = numKeys - numKeys1
				parentKeyValue = keyvalue1[-1]
				newleaffile = 'dat/podb' + str(tempCount)
				tempCount = tempCount + 1
				printToOpenFile(str(numKeys1)+'\n', data[1],' '.join(keyvalue1) + '\n' , ' '.join(indexvalue1) + '\n' , f )
				printTofile(numKeys2,1,' '.join(keyvalue2), ' '.join(indexvalue2), newleaffile)
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
if __name__ == '__main__':
	f = open('bplustree.config', 'r')
	data = f.readline()
	# maxitem = int(data.rstrip())
	f.close()
	maxitem = 32
	a = 0 
	filename1 = -1
	filename2 = -1
	# with open("querysample.txt", "r") as queryfile:
	# 	for line in queryfile:
	# 		indices = line.rstrip().split('\t')
	# 		if indices[0] == '0':
	# 			# print a
	# 			a += 1
	# 			print a
	# 			insert(indices[1], indices[2], root)
	with open("assgn2_bplus_data.txt", "r") as queryfile:
		for line in queryfile:
			a +=1
			print a
			indices = line.rstrip().split('\t')
			print insert(indices[0], indices[1], root)
	print tempCount