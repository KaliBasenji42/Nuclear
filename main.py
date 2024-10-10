
import urllib.request
import os

# Varibles

run = True
inp = ''
URL = ('https://www-nds.iaea.org/relnsd/v1/data?' +
       'fields=ground_states&nuclides=all')
filePath = "Data.txt"
data = ['None']
neededData = ['z', 'n', 'symbol', 'abundance', 'half_life_sec', 'atomic_mass',
              'decay_1', 'decay_1_%',
              'decay_2', 'decay_2_%',
              'decay_3', 'decay_3_%']

inpProt = 0
inpNeut = 0

# Functions

def lc_read_csv(url):
  req = urllib.request.Request(url)
  req.add_header('User-Agent', 
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
  content = urllib.request.urlopen(req)
  return content  
  

def strToInt(string):
    
    out = '0'
    
    for char in string:
        
        if char.isnumeric(): out = out + char
        
    
    return int(out)
    

def removeNum(string):
  
  out = ''
  
  for char in string:
    
    if not(char.isnumeric()): out = out + char
    
  
  return out
  

def printArray(array, index):
  
  print('')
  
  if len(array) > len(index): print('Mapping Error')
  
  else:
    
    for i in range(len(array)):
      
      print(str(index[i]) + ': ' + str(array[i]))
      
    
  

def loadAllData(path):
  
  global data
  data = []
  row = []
  cell = ''
  rowStep = 0
  
  source = [False, False] # File, URL
  
  print('\nLoading Data...')
  file = open(path, 'r+')
  
  try: file = open(path, 'r+')
  except: print('\nFile Error')
  else:
      source[0] = True
  
  try: str(lc_read_csv(URL).read())
  except: print('\nURL Error')
  else:
    source[1] = True
    dataStr = str(lc_read_csv(URL).read())[2:]
  
  if not(source[0] or source[1]):
    data = ['None']
    return '\nNo Source Avaliable'
  
  if source[0] and source[1]:
    print('\nData loaded from Internet, writing to file')
    
    file = open(path, 'w')
    file.write(dataStr)
    file.close()
  
  elif source[0]:
    print('\nLoading data from file')
    
    file = open(path, 'r')
    dataStr = file.read()
    file.close()
  
  else:
    print('\nUsing data from Internet')
  
  for char in dataStr:
    
    rowStep += -1
    
    if char == '\\':
      
      data.append(row)
      row = []
      cell = ''
      rowStep = 1
      
    elif char == ',':
      
      row.append(cell)
      cell = ''
      
    elif rowStep < 0:
      
      cell += char
      
    
  
  return '\nData Recorded!'
  

def filter(dataTypes):
  
  global data
  out = []
  rowPos = 0
  recordRows = []
  
  print('\nFiltering Data...')
  
  for row in data:
    
    columnPos = 0
    
    newRow = []
    
    for cell in row:
      
      if rowPos == 0:
        
        for dataType in dataTypes:
          
          if dataType == cell: recordRows.append(columnPos)
          
        
      
      for num in recordRows:
        
        if num == columnPos: newRow.append(cell)
        
      
      columnPos += 1
      
    
    out.append(newRow)
      
    rowPos += 1
    
  
  data = out
  
  print('\nFiltered to:\n')
  
  return(data[0])
  

def loadData(path):
  
  print(loadAllData(path))
  #print(data)
  print(filter(neededData))
  

def getInfo(inp):
  
  global data
  weightInp = strToInt(inp)
  symInp = removeNum(inp)
  
  for row in data:
    
    z = ''
    n = ''
    sym = ''
    
    for column in range(len(row)):
      
      if data[0][column] == 'z': z = row[column]
      if data[0][column] == 'n': n = row[column]
      if data[0][column] == 'symbol': sym = row[column]
      
    
    weight = strToInt(z) + strToInt(n)
    
    if weight == weightInp and sym == symInp: return row
    
    
  return []
  

def getInfoZN(inpZ, inpN):
    
  global data
  for row in data:
    
    z = ''
    n = ''
    
    for column in range(len(row)):
      
      if data[0][column] == 'z': z = row[column]
      if data[0][column] == 'n': n = row[column]
      
    
    if z == inpZ and n == inpN: return row
    
    
  return []
  

# Instructions

print('Data from www-nds.iaea.org (live charts).')
print('Enter \'quit\' to quit.')
print('Enter \'load\' to load data from the internet.')
print('Enter symbol then weight (U235) to get info...')
print('or enter number of protons, then neutrons')

# Input Loop

while run:
  
  inp = input('\nInput: ')
  
  if inp == 'quit': run = False
  
  elif inp == 'load': loadData(filePath)
  
  elif inp.isnumeric():
    
    inpProt = inp
    
    inpNeut = input('Neutrons: ')
    
    printArray(getInfoZN(inpProt, inpNeut), data[0])
    
  
  else: printArray(getInfo(inp), data[0])
  
