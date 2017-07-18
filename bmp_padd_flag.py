#!/usr/bin/env python

def read1(offset, ref, file):
	file.seek(offset,ref)
	a = ord(file.read(1))
	return a
		
def read2(offset,ref, file):
	file.seek(offset,ref)
	a = ord(file.read(1))
	b = ord(file.read(1))
	return a + 0x100*b

def read4(offset, ref, file):
	file.seek(offset,ref)
	a = ord(file.read(1))
	b = ord(file.read(1))
	c = ord(file.read(1))
	d = ord(file.read(1))
	return a + 0x100*b + 0x10000*c + 0x1000000*c

def write1(offset, ref, file, value):
	file.seek(offset, ref)
	a = chr(value)
	file.write(a)	

def write2(offset, ref, file, value):
	file.seek(offset, ref)
	a = chr(value%0x100)
	value = value/0x100
	b = chr(value%0x100)

	file.write(a)	
	file.write(b)	

def write4(offset, ref, file, value):
	file.seek(offset, ref)
	a = chr(value%0x100)

	value = value/0x100
	b = chr(value%0x100)

	value = value/0x100
	c = chr(value%0x100)
	
	value = value/0x100
	d = chr(value%0x100)

	file.write(a)	
	file.write(b)	
	file.write(c)	
	file.write(d)	
	
def paddCalc(width, bpp):
	
	relevantSize = width*bpp/8
	rowSize = ((relevantSize*8 + 31)/32)*4
	return relevantSize, rowSize, rowSize - relevantSize

#File name here 
file = open("1pbxe4.bmp", "r+b")

width = read4(0x12, 0, file)
height = read4(0x16, 0, file)
bpp = read2(0x1c, 0, file)
offset = read4(0x0a, 0, file)

print("Width")
print(width)
print("Height")
print(height)
print("Bpp")
print(bpp)

relevantSize, rowSize, paddSize = paddCalc(width, bpp)

if paddSize == 0:
	write4(0x12, 0, file, width - 1)
	width = read4(0x12, 0, file)
	relevantSize, rowSize, paddSize = paddCalc(width, bpp)


file.seek(offset + relevantSize, 0)
for i in range(0, height):
	for j in range(0, paddSize):
		write1(0x00, 1, file, 0)
	file.seek(relevantSize, 1)
#***************	
#Write flag here
#***************
flag = "artie.com/nascar/arg-checkered-flag-url.gif"

#**************************
#Write a final message here
#**************************
finalMessage = '1 - Um espirito nobre engrandece o menor dos homens. 2 - So strings nem sempre vai te ajudar. 3 - Ja olhou a imagem?'

i = 0
if len(flag) < height*paddSize:
	file.seek(offset + relevantSize, 0)
	for c in flag:
		#print(c)
		write1(0x00, 1, file, ord(c))
		i = i + 1
		if i == paddSize:
			file.seek(relevantSize, 1)
			i = 0

	for c in finalMessage:
		write1(0x00, 2, file, ord(c))
else:
	print("Flag too long")
