import gspread
import json
import os 
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties
import numpy as np
import statistics

import sys, getopt

from private_api_keys import *
from oauth2client.service_account import ServiceAccountCredentials


now = datetime.now()
month_number = now.strftime("%m")
print('THE CURRENT MONTH IS ', month_number)

#from datetime import datetime
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
#if len(sys.argv)== 2:
#    print('Argument Number 2: ', str(sys.argv[1])) 


def updateDatabase(path):
  
    if not os.path.isfile(path) or time.time() - getModificationTimeSeconds(path) > 1:
        print('Updating from Google.')
        updateFromGoogle()
    else:
        print('Less than one hour since last refresh, skipping pull from google.')
       

def updateFromGoogle():
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(servCreds, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheetName).worksheet(rangeWorksheet)
        list_of_hashes = sheet.get_all_records()

        with open('data.txt', 'w') as outfile:            
            json.dump(list_of_hashes, outfile)        
    except:
        print('Exception thrown in updateFromGoogle')
        return
    
    print('Local HypeMan RANGE grade database updated from Google Sheets.') 

def getModificationTimeSeconds(path):
    ct = time.time()
    try: 
        modification_time = os.path.getmtime(path) 
        #print("Last modification time since the epoch:", modification_time) 
    except OSError: 
        print("Path '%s' does not exists or is inaccessible" %path) 
        return ct-4000
  
    return modification_time

def calculateGradeBombing(curList):   
    #print('***** calculateGradeBombing *****') 
    gradeCell = {}
    #gradeCell['bombGrade'] = -1
    gradeCell['icon'] = ''
    gradeCell['bg'] = '#FFFFFF'
    
    missionTime =''
    missionDate =''
    missionTheatre =''

    pt = float(-1.0)    
    for i in curList:

        # skip strafes
        if 'N/A' in i['impactQuality']:
            continue
        
        #print('skipping strafe runs')        

        try:
            #print('TRTNG TO CALCULATE SCORE')
            tmp = float(i['bombScore'])
            if tmp > pt:
                pt = tmp
                
            if tmp == 5 and not '5' in gradeCell['icon']:
                gradeCell['icon']+= '5'
            elif tmp == 4 and not '4' in gradeCell['icon']:
                gradeCell['icon']+= '4'
            elif tmp == 3 and not '3' in gradeCell['icon']:
                gradeCell['icon']+= '3'
            elif tmp == 2 and not '2' in gradeCell['icon']:
                gradeCell['icon']+= '2'
            elif tmp == 1 and not '1' in gradeCell['icon']:
                gradeCell['icon']+= '1'
        except:
            pt=0
    
    gradeCell['bg'] = colorFromPoints(pt)
    gradeCell['score'] = pt
    
  #  if not gradeCell['score']:
  #      print('what')
    return gradeCell
    
def colorFromPoints(g):
    colors=['red','blue','peru','yellow','limegreen','black','orange','pink'] 
    redcolor = '#ED1B24'
    browncolor = '#835C3B'
    orangecolor = '#d17a00'
    yellowcolor = '#b6c700'
    greencolor = '#0bab35'
    bluecolor = '#01A2EA'
    blankcell='#FFFFFF'
    blackcolor = '#000000'
    color = 'blankcell'
    lightgray = '#708090'
    royalblue = '#4169E1'
    
    if g == -1:             
        color=blankcell
    elif g == 0 :
        color=lightgray#BLACK
    elif g == 1:
        color=colors[0] #RED
    elif g == 2.0:                
        color=colors[6] #ORANGE  
    elif g == 3.0:
        color = colors[3] #YELLOW
    elif g == 4.0:
        color = colors[4] #GREEN 
    elif g == 5:                
        color = royalblue #BLUE
    else:
        color = blankcell
        
    return color
      
    
def calculateGradeStrafing(curList):
   #print('***** calculateGradeStrafing *****') 
    gradeCell = {}
    #gradeCell['strafeScore'] = -1
    gradeCell['icon'] = ''
    gradeCell['bg'] = '#FFFFFF'
    
    missionTime =''
    missionDate =''
    missionTheatre =''

    pt = float(-1.0)    
    for i in curList:

        # skip strafes
        if 'N/A' in i['strafeQuality']:
            continue
        
        #print('skipping strafe runs')        

        try:
            #print('TRTNG TO CALCULATE SCORE')
            tmp = float(i['strafeScore'])
            if tmp > pt:
                pt = tmp
                
            if tmp == 5 and not '5' in gradeCell['icon']:
                gradeCell['icon']+= '5'
            elif tmp == 4 and not '4' in gradeCell['icon']:
                gradeCell['icon']+= '4'
            elif tmp == 3 and not '3' in gradeCell['icon']:
                gradeCell['icon']+= '3'
            elif tmp == 2 and not '2' in gradeCell['icon']:
                gradeCell['icon']+= '2'
            elif tmp == 1 and not '1' in gradeCell['icon']:
                gradeCell['icon']+= '1'
            elif tmp == 0 and not '0' in gradeCell['icon']:
                gradeCell['icon']+= '0'
        except:
            pt=0
    
    gradeCell['bg'] = colorFromPoints(pt)
    gradeCell['score'] = pt
    
  #  if not gradeCell['score']:
  #      print('what')
    return gradeCell
    
def calculateGrade(curList, attackType):
    #print('***** calculateGrade *****') 

    if attackType == 'Bombing Run':
        return calculateGradeBombing(curList)                       

    if attackType == 'Strafing Run':        
        return calculateGradeStrafing(curList)    

        
                

def calculatePilotRow(data, name, ruleset):    
    #print('***** calculatePilotRow *****') 
 
    #print(name)
    boardRow = [];
    
    uniqueDates = []
    for i in reversed(data):
        #grade = grade0
        if name == i['pilot']:
            if i['osTime'] not in uniqueDates:
                uniqueDates.append(i['osTime'])
    
    for i in uniqueDates:
        #print(i)
        curList = [];
        for j in data:
            if name == j['pilot'] and j['osTime'] == i:
                curList.append(j)
        
        ithPilotGrade = calculateGrade(curList,attackType)
        
        boardRow.append(ithPilotGrade)
        
            
#            if not haveDate:
#                curDate = i['ServerDate']
#                haveDate = True            
#                
#            if curDate == i['ServerDate']:
#                curList.append(i)
#                
#            else:
#                curDate = i['ServerDate']
#                grade = calculateGrade(curList, grade0)
#                boardRow.append(grade)
#                curList = [];
#                curList.append(i)       
                
    #print(boardRow)           
    return boardRow

def CalculateAverageScore(pilotRow):
    #print('***** CalculateAverageScore *****') 
    # IDEAS FOR RANGE SCORES: Shack = 5.0, Excellent= 4.0, Good = 3.0, Ineffective = 2.0, Poor = 1.0
    score = 0.0
    for i in pilotRow:
        score = score + i['score']
    
    finalscore = score/len(pilotRow)
    #print(finalscore)
    return finalscore
        
def plotSquadron(pilotRowDictonary, options):
    #print('***** plotSquadron *****') 

    #print('PlotSquadron')
    maxLength = 0
    for i in pilotRowDictonary:
        if len(i) > maxLength:
            maxLength = len(i)
    if maxLength < options['maxRows']:
        maxLength = options['maxRows']

    fig = plt.figure(figsize=(6, 3), dpi=250)
    ax = fig.add_subplot(1,1,1)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])
    
    tb = Table(ax, bbox=[0, 0, 1, 1])
    #tb.scale(0.25, 1)     
    tb.auto_set_font_size(False)
    n_cols = maxLength+2
    n_rows = len(pilots)+1
    width, height = 100 / n_cols, 100.0 / n_rows
    #height = height/10
    shack='💥'
    goldstar = '⭐'
    #unicorn='✈️'
    #case3 = '⚸'
    case3 = '•'
    case2 = '⊙'
    blankcell='#FFFFFF'
    blankcell='#FFFFFF'
     #colors=['red','orange','orange','yellow','lightgreen']  #078a21
    #colors=['#a00000','#835C3B','#d17a00','#b6c700','#0bab35','#057718','#057718']
    #colors=['#a00000','#d17a00','#d17a00','#b6c700','#0bab35','#057718','#057718']
    colors=['red','deepskyblue','peru','yellow','limegreen','black']       
    # redcolor = '#a00000'
    # browncolor = '#835C3B'
    # orangecolor = '#d17a00'
    # yellowcolor = '#b6c700'
    # greencolor = '#0bab35'
    # bluecolor = '#01A2EA'
    
    try:
        minDate = data[-1]['ServerDate']
        maxDate = data[0]['ServerDate']
    except:
        minDate =''
        maxDate = ''
        
    textcolor = '#000000'
    edgecolor = '#708090'
    cell = tb.add_cell(0,0,10*width,height,text='Callsign',loc='center',facecolor=blankcell) #edgecolor='none'
    cell.get_text().set_color(textcolor)    
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
    cell.set_edgecolor(edgecolor)
    cell.set_linewidth(0.5)
    #cell.set_fontsize(24)
    cell = tb.add_cell(0,1,width,height,text='',loc='center',facecolor=blankcell) #edgecolor='none'
    cell.get_text().set_color(textcolor)
    cell.set_edgecolor(edgecolor)
    cell.set_linewidth(0.5)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))
    cell.set_edgecolor(edgecolor)
    #cell.set_fontsize(24)
    titlestr = ' '+options['squadron']
    count = 0
    for col_idx in range(2,options['maxCols']+2):
        
        text = ''
        
        if count < len(titlestr):
            text = titlestr[count]
            count = count + 1
        cell = tb.add_cell(0, col_idx, width, height,
                        text=text.upper(),
                        loc='center',
                        facecolor=blankcell)
        cell.set_linewidth(0.5)                        
        cell.set_edgecolor(edgecolor)
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
        cell.set_edgecolor(edgecolor)    

    #cell.set_text_props(family='')


    #titlestr = 'JOW Greenie Board ' + minDate + ' to ' + maxDate

    minRows = len(pilots)

    if minRows < options['maxRows']: 
        minRows = options['maxRows']
        
    #for p_idx in range(0,len(pilots)):
    for p_idx in range(0,minRows):
        row_idx = p_idx+1
       
        rd = []
        name = ''
        scoreText = ''
        
        if p_idx < len(pilots):
            name = pilots[p_idx]            
            rd = pilotRowDictonary[name]
#            avg = statistics.mean(rd)
            avg = CalculateAverageScore(rd)
            scoreText = round(avg,1)
                
        cell = tb.add_cell(row_idx,0,10*width,height,text=name,loc='center',facecolor=blankcell,edgecolor='blue') #edgecolor='none'    
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size="7"))
        cell.set_edgecolor(edgecolor)
        cell.set_linewidth(0.5)
    #    name = pilots[p_idx];

        
        cell = tb.add_cell(row_idx,1,width,height,text=scoreText,loc='center',facecolor=blankcell)
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(size="6.0"))
        cell.set_edgecolor(edgecolor)
        cell.set_linewidth(0.5)
        col_idx = 2
            
        for ij in rd:
            
            color = ij['bg']
            
            if not color:
                color = blankcell
                
            text = ''      
            
            if '3' in ij['icon']:
                text = case3
            elif '2' in ij['icon']:
                text = case2
                        
            cell = tb.add_cell(row_idx,col_idx,width,height,text=text,loc='center',facecolor=color) #edgecolor='none'  
            cell.get_text().set_color('#333412')
            cell.set_linewidth(0.5)
           # cell.auto_set_font_size()
            cell.set_text_props(fontproperties=FontProperties(weight='bold',size="14"))
            cell.set_edgecolor(edgecolor)    
            col_idx = col_idx + 1
                    
            
        color = blankcell
        text=''
        
        # add the remaining cells to the end
        for f in range(col_idx,options['maxCols']+2):
            cell = tb.add_cell(row_idx,f,width,height,text=text,loc='center',facecolor=color) #edgecolor='none' 
            cell.set_linewidth(0.5)            
            cell.set_edgecolor(edgecolor)
     
    #
    #tb.set_fontsize(7)    
    ax.add_table(tb)
    ax.set_axis_off()
    ax.axis('off')
    plt.box(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    #plt.title(titlestr,color='w')

    plt.savefig('boardRange.png',transparent=False,bbox_inches='tight', pad_inches=0)
    
def plotDefaultBoard(pilotRowDictonary, options):
    print('***** Default Pilot Board *****') 
    maxLength = 0
    #name = pilotRowDictonary['name']
    for i in pilotRowDictonary:#['name']:
        if len(i) > maxLength:
            maxLength = 20
            print(' maxLength is : ', maxLength)

       
    if maxLength < 17:
        print(' maxLength is less than 17 so is : ', maxLength)
        maxLength = 17
        
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1,1,1)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])

    tb = Table(ax, bbox=[0, 0, 1, 1])

    tb.auto_set_font_size(False)

    n_cols = maxLength+2
    n_rows = len(pilots)+1
    width, height = 100 / n_cols, 100.0 / n_rows
    shack='⨂'
    goldstar = '⭐'
    #unicorn='✈️'
    #case3 = '●'
    case3 = '⨂' #added 2/14/21
    case2 = '⨀'
    night = '•' #added 2/14/21
    blankcell='#FFFFFF'
    callsigncell='#b6c700'
    

    #colors=['red','orange','orange','yellow','lightgreen']  #078a21
    #colors=['#a00000','#835C3B','#d17a00','#b6c700','#0bab35','#057718','#057718']
    colors=['#a00000','#d17a00','#d17a00','#b6c700','#0bab35','#057718','#057718']
            
    redcolor = '#a00000'
    browncolor = '#835C3B'
    orangecolor = '#d17a00'
    yellowcolor = '#b6c700'
    greencolor = '#0bab35'

   # try:
   #     minDate = data[-1]['ServerDate']
   #     maxDate = data[0]['ServerDate']
   # except:
   #     minDate =''
   #     maxDate = ''
        
    textcolor = '#708090'
    edgecolor = '#FFFFFF'
    if maxLength >50:
        print('maxLength >50: ') 
        cell = tb.add_cell(0,0,11,height,text='   Callsign   ',loc='center',facecolor=blankcell) #edgecolor='none'
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
        cell.set_edgecolor(edgecolor)
        #cell.set_fontsize(24)
        cell = tb.add_cell(0,1,2,height,text='',loc='center',facecolor=blankcell) #edgecolor='none' <- This line sets width of score column (changed to 5 from 'width')
    else:
        print('maxLength  LESS THAN 50: ') 
        cell = tb.add_cell(0,0,20,height,text='   Callsign   ',loc='center',facecolor=blankcell) #edgecolor='none'
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
        cell.set_edgecolor(edgecolor)
        #cell.set_fontsize(24)
        cell = tb.add_cell(0,1,width,height,text='',loc='center',facecolor=blankcell) #edgecolor='none' <- This line sets width of score column (changed to 5 from 'width')
    cell.get_text().set_color(textcolor)
    cell.set_edgecolor(edgecolor)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))
    cell.set_edgecolor(edgecolor)
    textcolor = '#FF7F50'
    gbDate = now.strftime("%b %Y")
    currentMonth = datetime.now().month
    #titlestr = ' RANGE BOMBING BOARD (last 20) ' #+ str(currentMonth) + '/' + str(datetime.now().year)
    finalstr = " ".join((titlestr,gbDate))

    print(titlestr)
    spacer = int(maxLength/2)        
    cell = tb.add_cell(0, spacer, width, height,text=finalstr,loc='center',facecolor=blankcell)    
    cell.set_edgecolor(edgecolor)
    cell.get_text().set_color(titleColor)
    cell.set_text_props(fontproperties=FontProperties(weight='bold',size=8))   
    cell.set_edgecolor(edgecolor)    

    #cell.set_text_props(family='')

    textcolor = '#000000'
    edgecolor = '#708090'
#    titlestr = 'JOW Greenie Board ' + minDate + ' to ' + maxDate

    minRows = len(pilots)

    if minRows < 19: 
        minRows = 19
        
    for p_idx in range(0,minRows):
        row_idx = p_idx+1
       
        rd = []
        name = ''
        scoreText = ''
        
        if p_idx < len(pilots):
            name = pilots[p_idx]
            rd = pilotRowDictonary[name]
            #avg = statistics.mean(rd)
            
            avg = CalculateAverageScore(rd)
            #print ('average score is: ',avg)
            scoreText = round(avg,1)
            if name.lower() == 'eese':
                name = "SippyCup"    

                
        cell = tb.add_cell(row_idx,0,5*width,height,text=name,loc='center',facecolor=blankcell,edgecolor='blue') #edgecolor='none'    
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size="7.0"))
        cell.set_edgecolor(edgecolor)

        
        cell = tb.add_cell(row_idx,1,width,height,text=scoreText,loc='center',facecolor=blankcell)
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight='bold',size="7.0"))
        cell.set_edgecolor(edgecolor)
        col_idx = 2
        
        rd2 = reversed(rd)

        for g in reversed(list(rd2)[0:20]):
            color = g['bg']            
            text = ''      
            
            if '1' in g['icon']:
                text = "1"
                #print('1 should be shown ')
            elif '2' in g['icon']:
                text = "2"
                #print('2 should be shown ')        
            elif '3' in g['icon']:
                text = "3"            
                #print('3 should be shown ')
            elif '4' in g['icon']:
                #print('4 should be shown ')
                text = "4"   
            elif '5' in g['icon']:
                text = "5"
                #print('5 should be shown ')
            elif '0' in g['icon']:
                text = "X"
                #print('5 should be shown ')

            cell = tb.add_cell(row_idx,col_idx,width,height,text=text,loc='center',facecolor=color) #edgecolor='none'  
            cell.get_text().set_color('#333412')
           # cell.auto_set_font_size()
            cell.set_text_props(fontproperties=FontProperties(weight='bold',size="10"))
            cell.set_edgecolor(edgecolor)    
            col_idx = col_idx + 1
                    
            
        color = blankcell
        text=''
        
        # add the remaining cells to the end
        for f in range(col_idx,maxLength+2):
            cell = tb.add_cell(row_idx,f,width,height,text=text,loc='center',facecolor=color) #edgecolor='none'            
            cell.set_edgecolor(edgecolor)
            
    #tb.set_fontsize(7)    
    ax.add_table(tb)
    ax.set_axis_off()
    ax.axis('off')
    plt.box(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    #plt.title(titlestr,color='w')

    plt.savefig('boardRange.png',transparent=False,bbox_inches='tight', pad_inches=0)

# set defaults
#airframe = ''
attackType = ''
squadron = ''
ruleset = 'all data'
titlestr = 'title not set'
#print('Length of argv: ' , len(sys.argv));
if len(sys.argv) >= 2:   
    if str(sys.argv[1]) == 'bomb':
        #airframe = 'F-14B', 'F-14A-135-GR'
        attackType = 'Bombing Run'
        titlestr = ' RANGE BOMBING BOARD (last 20) '
        titleColor = '#FF7F50'
    elif str(sys.argv[1]) == 'strafe':    
        #airframe = 'FA-18C_hornet'
        attackType = 'Strafing Run'
        titlestr = ' RANGE STRAFING BOARD (last 20) '
        titleColor = '#01A2EA'
    print('Attack Type: ', attackType)     
if len(sys.argv) >= 3:        
    ruleset = str(sys.argv[2])         
    
if len(sys.argv) >= 4:    
    squadron = str(sys.argv[3]);
    print('Squadron: ', squadron) 
  
print('Ruleset: ', ruleset)   
rangeData = 'data.txt'

updateDatabase(rangeData)

with open('data.txt') as json_file:
    data = json.load(json_file)
 


# go through and  keep only a specified airframe    
data2 = data
print('... size of data array: ' , str(len(data)))
count = 0

data2 = []

count = count + 1 #my edit     
for i in data:
    # if i['airframe']
    
    data2.append(i)
        # print('Deleting airframe: ', i['airframe'], ' was looking for: ' , airframe)
        # data.remove(i)
    count = count + 1

print('Number of rows kept: ', str(count))

data = data2
print('size of data array: ' , str(len(data)))
count = 0
if squadron != '':
    data2 = []
    print('Searching for squadron: ' , squadron)
    for i in data:    
        name = i['pilot']
        #print('Name: ' , name)
        name = name.replace('-', '')
        name = name.replace('_', '')
        name = name.replace('[', '')
        name = name.replace(']', '')
        name = name.replace('|', '')
        name = name.replace('\\', '')
        name = name.replace('/', '')
        name = name.replace('@', '')    
        name = name.lower()
        
        index = name.find(squadron)
        
        if index != -1:
            data2.append(i)
            count = count + 1;
            #print('Keeping in squadron: ' , name)
          #  name = name.replace(squadron,'')

# if the squadron was empty just keep the original data
data = data2

data2 = []
if attackType == 'Bombing Run':
    print('Skipping strafes')
    for i in data:
        if not'N/A' in i['impactQuality']:
            data2.append(i)
elif attackType == 'Strafing Run':
    print('Skipping bombing runs')
    for i in data:
        if not'N/A' in i['strafeQuality']:
            data2.append(i)

data = data2
print('Number remaining: ', str(len(data)))
pilots = [] #list      
pilotRowDictonary = {} #dictionary
pilotGradeDictionary = {} #added 5/25/21 to order the GPA's on board from HIGH to LOW scores
# get the rows as they will appear in our Greenie Board

# set the default grade
#grade0={}; grade0['color']='white'; grade0['score']=0.0; grade0['symbol']='x'; grade0['grade']='--'

# if squadron is empty then lets trim the landings not in the current month
data2 = []
if squadron == '':
    currentMonth = datetime.now().month
    print('skipping bombings/strafes not in current month')
    for i in data: 
        #print(i)
        idate = i['osDate'].split('/')
        imonth = int(idate[1])
        
        if imonth == currentMonth:
            data2.append(i)
            
    data = data2
        
    
for i in reversed(data):
    name = i['pilot']
    gpa = "gpa" #added 5/25/21 to order the GPA's on board from HIGH to LOW scores 
    
    if name not in pilots:
        pilots.append(name)  
        pilotRow = calculatePilotRow(data, name, ruleset)
        pilotRowDictonary[name] = (pilotRow)

        gpa = CalculateAverageScore(pilotRow) #added 5/25/21 to order the GPA's on board from HIGH to LOW scores 
        pilotGradeDictionary[name] = (gpa) #added 5/25/21 to order the GPA's on board from HIGH to LOW scores 
        
        




print ("pilots before sort:",pilots)

#print("pilotGradeDictionary :",pilotGradeDictionary) 
pilotGradeDictionary = dict(sorted(dict.items(pilotGradeDictionary), key=lambda kv: kv[1], reverse=True))#added 5/25/21 to order the GPA's on board from HIGH to LOW scores 
#print("pilotGradeDictionary after gpa sort :",pilotGradeDictionary) 
pilots = list(pilotGradeDictionary.keys()) #added 5/25/21 to order the GPA's on board from HIGH to LOW scores 


###print ('Print out of List - pilots:',pilotRowDictonary)
###pilotRowDictonary = dict(sorted(pilotRowDictonary.items(), key=lambda kv: pilotGradeDictionary[kv[0]],reverse=True))


print ("pilots after sort:",pilots)

# **** IDEA as I'm giving up for the day 5/25/21: Maybe make a dictionary of the names and grades, then order it based by grade, then extract out the list of names from dictionary, FIGURED IT OUT 2 MINUTES LATER!
      

options = {}

if squadron == '':
    plotDefaultBoard(pilotRowDictonary, options)
else:
    #options['airframe'] = airframe
    options['squadron'] = squadron
    options['ruleset'] = ruleset
    options['attackType'] = attackType
    options['maxRows']=10
    options['maxCols']=17
    plotSquadron(pilotRowDictonary, options)

print('done')    