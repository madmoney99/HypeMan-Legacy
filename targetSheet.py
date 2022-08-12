from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.patches import Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import matplotlib
import matplotlib.patches as patches
import cv2
import datetime
import math
import matplotlib.transforms as mtransforms #added by adam 5/21/21 for arrow rotation code
from private_api_keys import *
#%%
def ReadTargetsheet(filename):
    # read a target sheet into a dictionary as numpy arrays
    data={}
    try:
        with open(filename) as f:
            reader = csv.DictReader(f)
                    
            for headerNames in reader.fieldnames:
                data[headerNames]=np.array([])
                #print("ReadTargetsheet->  for headerNames in reader.fieldnames:  headerNames value: ", headerNames) #headerNames is the field name such as "callsign", "aircraft", etc
            for row in reader:
                for headerNames in reader.fieldnames:
                    svalue = row[headerNames]
                    try:
                        fvalue = float(svalue)
                        #print("ReadTargetsheet: float value: ", fvalue)
                        data[headerNames] = np.append(data[headerNames],fvalue)
                    except ValueError:
                        #print("Not a float", svalue)
                        data[headerNames]=svalue
        
    except:
        print('error reading targetsheet.')
        
    #data = data[-1]
    #print (data)  #prints out the entire csv file, column header and array associated with it
    return data
# %%        
def getRecentTargetsheet(sheetpath):
    try:
        p = Path(str(sheetpath))
        list_of_paths = p.glob('*RANGERESULTS*.csv')
        return max(list_of_paths, key=lambda p: p.stat().st_mtime) 
    except:
        return ''
    
# %%
        
def setSpine(ax,color):
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color(color)
    ax.spines['left'].set_color(color)
    ax.spines['right'].set_color(color)   

   
    
def plotTargetsheet(ts, pinfo):
    print('Plotting targetsheet...')

    facecolor = '#404040'
    referencecolor = '#C80000'  #A6A6A6 glide slope and flight path references
    #gridcolor = '#585858'
    gridcolor = '#d62d20'
    spinecolor = gridcolor
    #labelcolor = '#BFBFBF'
    labelcolor = '#BFBFBF'
    attackHeadingColor = '#c4ff0e'

    bombDistance = ts['Distance']
    bombRadial = ts['Radial']

    if bombDistance == 0 and bombRadial == 0:
        print('WE HAVE A STRAFE PASS!')
        fig, ax = plt.subplots(1, 1, sharex=True,facecolor=facecolor,dpi=150)
        fig.set_size_inches(6, 6)

        targetImage = plt.imread('Images/StrafeImageAlphaed.png')
        plt.imshow(targetImage,interpolation='none',origin='upper',extent=[-195, 195, -195, 195], clip_on=True) #this shows the image without being able to change paramters...
        #ax.figure.figimage(targetImage, 45,170, zorder=0, alpha=.7) #lower number results in more left for x, more down for y
        #matplotlib.use('Agg')
        plt.ioff() 
    
        ax.set_facecolor(facecolor)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        
        #plt.xlim(-270,270)
        #plt.ylim(-270,270)
        #plt.axis('scaled')
        
    
        #ax.xaxis.label.set_color(labelcolor)
        #plt.setp(ax.get_xticklabels(), color=labelcolor)
        #plt.setp(ax.get_yticklabels(), color=labelcolor)

        #ax.set_xlabel("Distance (Feet)")
        #ax.grid(linestyle='-', linewidth='0.5', color=gridcolor, alpha=1,zorder=5)  #Lineup Background Grid 
        #ax.tick_params(axis=u'both', which=u'both',length=0)
        #setSpine(ax,'none')
        #ax.spines['right'].set_color(spinecolor)
        #ax.spines['left'].set_color(spinecolor)
       

        #ax.set_xticks([-250,-200,-150,-100,-50,0,50,100,150,200,250])
        #ax.set_yticks([-250,-200,-150,-100,-50,0,50,100,150,200,250])

        bulletImage = plt.imread('Images/bulletHoleImage.png')
        #plt.imshow(targetImage) #this shows the image without being able to change paramters...
        #ax.figure.figimage(craterImage, x,y, alpha=1, zorder=9) #lower number results in more left for x, more down for y THIS WAS WORKING BUT NOT PLACING IN CORRECT LOCATION
    
        def main(n):
            '''
            bulletImage = plt.imread('bulletHoleImage.png')
            roundsHit = ts['Rounds Hit']
            #roundsHit=roundsHit.replace('.','')
            roundsHit = int(roundsHit)

            def scatterRandomPoints(n):
                plt.scatter(*np.random.randint(-100,100, size = (2, n)),color="black")


            scatterRandomPoints(roundsHit)
            '''
            
            #distance =  ts['Distance']*3.28084
            #degrees = ts['Radial']
            #radians = math.pi/180*degrees
            #n=10
            x=np.random.randint(-100,100)
            y=np.random.randint(-100,100)
            #image_path = bulletImage
            #fig, ax = plt.subplots()
            
            imscatter(x, y, bulletImage, zoom=0.2, ax=ax) # ***** USE THIHS LINE FOR AAZ SERVER AND TESTING ****, COMMENT OUT FOR CRANKY CA
            ax.plot(x, y,zorder=15, alpha=0.5) # ***** USE THIHS LINE FOR AAZ SERVER AND TESTING ****, COMMENT OUT FOR CRANKY CA
            #plt.scatter(x,y,color="red", marker="x", linewidths=8) # ***** USE THIHS LINE FOR CRANKY CA ****, COMMENT OUT FOR AAZ SERVER AND TESTING

        def imscatter(x, y, image, ax=None, zoom=1):
            if ax is None:
                ax = plt.gca()
            if not isinstance(image, np.ndarray):
                image = plt.imread(image)
            im = OffsetImage(image, zoom=zoom)
            x, y = np.atleast_1d(x, y)
            artists = []
            for x0, y0 in zip(x, y):
                ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
                artists.append(ax.add_artist(ab))
            ax.update_datalim(np.column_stack([x, y]))
            #ax.autoscale()
            return artists

        roundsHit = ts['Rounds Hit']
        #roundsHit=roundsHit.replace('.','')
        roundsHit = int(roundsHit)
        
        for x in range(roundsHit):
            main(roundsHit)

        roundsFired = ts['Rounds Fired']
        roundsHit = ts['Rounds Hit']
        roundsQuality = ts['Rounds Quality']
        accuracy = (roundsHit/roundsFired)*100
        accuracy = np.round(accuracy,2)
        #feetDistance = int(feetDistance)
        #feetDistance = np.round(feetDistance,2)
        titlestr = ts['Target']
        titlestr+=' '
        titlestr+=ts['Name']
        titlestr+='\n '
        #print("trying to find error causing no waveoff to print - 3.5")  
        titlestr+=''
        #titlestr+='\n'
        titlestr+=str(roundsFired)
        titlestr+=' Rounds Fired, '
        titlestr+=str(roundsHit)
        titlestr+=' Rounds Hit\n'
        titlestr=titlestr.replace('.','')
        titlestr+=str(accuracy)
        titlestr+='%'
        titlestr+=' accuracy,  '
        titlestr+=str(roundsQuality)
        titlestr+='\n '
        titlestr+=(ts['Airframe'])
        titlestr+=', '
        titlestr +=pinfo['time']
        titlestr=titlestr.replace('[','')
        titlestr=titlestr.replace(']','')
        
        print(titlestr)
    
        if accuracy >= 90: #changed to >90 on 5/23/21
            ax.text(0.5, 0.5, '*** DEAD EYE !! ***', 
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color='red', fontsize=26) 
            ax.text(0.505, 0.505, '*** DEAD EYE !! ***',
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color='yellow', fontsize=26) 

        if roundsQuality == '* INVALID - PASSED FOUL LINE *':
             ax.text(0.5, -0.2, 'X', 
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color='red', fontsize=400,zorder=16) 


        fig.suptitle(titlestr, fontsize=12,color=labelcolor)
    else:
        print('WE HAVE A BOMBING PASS!')
        fig, ax = plt.subplots(1, 1, sharex=True,facecolor=facecolor,dpi=150)
        fig.set_size_inches(6, 6)

        targetImage = plt.imread('Images/rangeTargetImageCropped.png')
        plt.imshow(targetImage,interpolation='none',origin='upper',extent=[-195, 195, -195, 195], clip_on=True) #this shows the image without being able to change paramters...
        #ax.figure.figimage(targetImage, 45,170, zorder=0, alpha=.7) #lower number results in more left for x, more down for y
        #matplotlib.use('Agg')
        plt.ioff() 
    

        targetImage = plt.imread('Images/NorthUp.png')
        plt.imshow(targetImage,interpolation='none',origin='upper',extent=[130, 250, 130, 250], clip_on=True,zorder=17)

        ax.set_facecolor(facecolor)
   
        #ax.set_ylim([-270,270])
        #ax.set_xlim([-270,270])
        plt.xlim(-270,270)
        plt.ylim(-270,270)
        plt.axis('scaled')
        #plt.gca().set_aspect('equal', adjustable='box')
        #ax.plot(xy[0],feet*xy[1], 'g', linewidth=16, alpha=0.01) #'g', linewidth=16, alpha=0.01
    
        ax.xaxis.label.set_color(labelcolor)
        # ax.set_title('Angle of Attack',color=labelcolor)
        plt.setp(ax.get_xticklabels(), color=labelcolor)
        plt.setp(ax.get_yticklabels(), color=labelcolor)

        ax.set_xlabel("Distance (Feet)")

        #fig.suptitle(titlestr, fontsize=14,color=labelcolor)
        #fig.title(ts['Details'], fontsize=10)

        ax.grid(linestyle='-', linewidth='0.5', color=gridcolor, alpha=1,zorder=5)  #Lineup Background Grid 
        ax.tick_params(axis=u'both', which=u'both',length=0)
        setSpine(ax,'none')
        ax.spines['right'].set_color(spinecolor)
        ax.spines['left'].set_color(spinecolor)
        #plt.legend()# giving an error when commenting out the plt.show
        #plt.show() #by commmenting this out, image is being saved but not opening up in python plot window. Not sure why windown doesn't open in trapsheet.py, but for whatever reason need this commented out.

        ax.set_xticks([-250,-200,-150,-100,-50,0,50,100,150,200,250])
        ax.set_yticks([-250,-200,-150,-100,-50,0,50,100,150,200,250])

        #plt.scatter(x,y,s=400,color='r',zorder=10, marker="x") #zorder is the layer order... made this 10 to be last layer, so not to have image or grids drawn over it. Make easier to see!
        #ax.scatter(x,y,s=400,color='r',zorder=10, marker="") #zorder is the layer order... made this 10 to be last layer, so not to have image or grids drawn over it. Make easier to see!
    
        #plt.plot([10,20,30,40,50], [10,20,30,40,50], 'x')
        #plt.show()
    
        craterImage = plt.imread('Images/crater2.png')
        #plt.imshow(targetImage) #this shows the image without being able to change paramters...
        #ax.figure.figimage(craterImage, x,y, alpha=1, zorder=9) #lower number results in more left for x, more down for y THIS WAS WORKING BUT NOT PLACING IN CORRECT LOCATION
    
        def main():
            craterImage = plt.imread('Images/crater2.png')
            #x = -100
            #y = -100

            #example Distance and Radius from data: 25.17, 298
            distance =  ts['Distance']*3.28084
            degrees = ts['Radial']
            radians = math.pi/180*degrees
            x=distance*math.sin(radians)
            y=distance*math.cos(radians)
            image_path = craterImage
            #fig, ax = plt.subplots()
            
            imscatter(x, y, craterImage, zoom=0.2, ax=ax) # ***** USE THIHS LINE FOR AAZ SERVER AND TESTING ****, COMMENT OUT FOR CRANKY CA
            ax.plot(x, y,zorder=15, alpha=0.5) # ***** USE THIHS LINE FOR AAZ SERVER AND TESTING ****, COMMENT OUT FOR CRANKY CA
            #plt.scatter(x,y,color="black", marker="X", linewidths=8) # ***** USE THIHS LINE FOR CRANKY CA ****, COMMENT OUT FOR AAZ SERVER AND TESTING
            

        def imscatter(x, y, image, ax=None, zoom=1):
            if ax is None:
                ax = plt.gca()
            if not isinstance(image, np.ndarray):
                image = plt.imread(image)
            im = OffsetImage(image, zoom=zoom)
            x, y = np.atleast_1d(x, y)
            artists = []
            for x0, y0 in zip(x, y):
                ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
                artists.append(ax.add_artist(ab))
            ax.update_datalim(np.column_stack([x, y]))
            #ax.autoscale()
            return artists

        distance =  ts['Distance']
        attackHeading = ts['Attack Heading']
        #plt.plot([10,20,30,40,50], [10,20,30,40,50], 'x',)
        #plt.plot((x, y),'#32CD32')

        ###x = [-225, -200, -175, -150]
        ###y = [225, 200, 175, 150]
        ###plt.plot(x, y,'#32CD32')



        targetImage = plt.imread('Images/greenArrow.png')
        #plt.imshow(targetImage,interpolation='none',origin='upper',extent=[-225, -150, 150, 225], clip_on=True,zorder=17)

        def do_plot(ax, Z, transform):
            im = plt.imshow(Z, interpolation='none',
                   origin='lower',
                   extent=[50, -50, 50, -50], clip_on=True,zorder=17)

            trans_data = transform + ax.transData
            im.set_transform(trans_data)
          
        #fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        do_plot(ax, targetImage, mtransforms.Affine2D().rotate_deg(-attackHeading).translate(-200, 175))

        if distance < 1.53:
            ax.text(0.5, 0.65, '*** SHACK !! ***', zorder=16,
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color='red', fontsize=22) 
            ax.text(0.505, 0.655, '*** SHACK !! ***',
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color='blue', fontsize=22) 
            #ax.text(0.505, 0.659, '*** SHACK !! ***',
            #    verticalalignment='bottom', horizontalalignment='center',
            #    transform=ax.transAxes,
            #    color='red', fontsize=22) 


        ax.text(0.15, .96, 'Attack Direction:',
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color=attackHeadingColor, fontsize=12,zorder=16)


        attackHeadingString = str(attackHeading)
        attackHeadingString=attackHeadingString.replace('[','')
        attackHeadingString=attackHeadingString.replace(']','')
        attackHeadingString=attackHeadingString.replace('.','°')

        ax.text(0.35, .96, attackHeadingString,
                verticalalignment='bottom', horizontalalignment='center',
                transform=ax.transAxes,
                color=attackHeadingColor, fontsize=12,zorder=16)

        main()

        feetDistance = ts['Distance']*3.28084
        #feetDistance = int(feetDistance)
        feetDistance = np.round(feetDistance,2)
        titlestr =  ts['Target']
        callsign = ts['Name']
        titlestr+='\n'
        titlestr+=ts['Name']
        titlestr+=': '
        #print("trying to find error causing no waveoff to print - 3.5")  
        titlestr+=''
        #titlestr+='\n'
        titlestr+=(ts['Quality'])
        titlestr+=' HIT ('
        titlestr+=str(feetDistance)
        titlestr+=' ft)\n'
        titlestr+=(ts['Airframe'])
        titlestr+=' '
        titlestr +=pinfo['time']
        titlestr=titlestr.replace('[','')
        titlestr=titlestr.replace(']','')

        print(titlestr)


        fig.suptitle(titlestr, fontsize=12,color=labelcolor)



    bombQuality = ts['Quality']  

    if bombQuality == "SHACK":
        scoreBadge = plt.imread('Images/pointsImage5.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 5 points badge')
    elif bombQuality == "EXCELLENT":
        scoreBadge = plt.imread('Images/pointsImage4.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 4 points badge')
    elif bombQuality == "GOOD":
        scoreBadge = plt.imread('Images/pointsImage3.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 3 points badge')
    elif bombQuality == "INEFFECTIVE":
        scoreBadge = plt.imread('Images/pointsImage2.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 2 points badge')
    elif bombQuality == "POOR":
        scoreBadge = plt.imread('Images/pointsImage1.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 1 points badge')

    strafeQuality = ts['Rounds Quality']

    if strafeQuality == "DEADEYE PASS":
        scoreBadge = plt.imread('Images/pointsImage5.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 5 points badge')
    elif strafeQuality == "EXCELLENT PASS":
        scoreBadge = plt.imread('Images/pointsImage4.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 4 points badge')
    elif strafeQuality == "GOOD PASS":
        scoreBadge = plt.imread('Images/pointsImage3.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 3 points badge')
    elif strafeQuality == "INEFFECTIVE PASS":
        scoreBadge = plt.imread('Images/pointsImage2.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 2 points badge')
    elif strafeQuality == "POOR PASS":
        scoreBadge = plt.imread('Images/pointsImage1.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 1 points badge')
    elif strafeQuality == "* INVALID - PASSED FOUL LINE *":
        scoreBadge = plt.imread('Images/pointsImage0.png')
        ax.figure.figimage(scoreBadge, 780, 800, alpha=1, zorder=1)
        print('adding 0 points badge')

    if pinfo['airframe']=='FA-18C_hornet':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/hornet_alpha.png')
        ax.figure.figimage(aircraftBadge, -90, 800, alpha=.75, zorder=1)
        print('adding F-18 badge')
    elif pinfo['airframe']=='F-14A-135-GR':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/tomcatA_alpha.png')
        ax.figure.figimage(aircraftBadge, -20, 830, alpha=.75, zorder=1)
        print('adding F-14A badge')
    elif pinfo['airframe']=='F-14B':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/tomcatB_alpha.png')
        ax.figure.figimage(aircraftBadge, -20, 740, alpha=.75, zorder=1)
        print('adding F-14B badge')
    elif pinfo['airframe']=='AV-8B':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/harrier_alpha.png')
        ax.figure.figimage(aircraftBadge, -40, 740, alpha=.75, zorder=1)
        print('adding AV-8B badge')
    elif pinfo['airframe']=='A-10C_2':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/a-10Alphaed.png')
        ax.figure.figimage(aircraftBadge, -30, 750, alpha=.75, zorder=1)
        print('adding A-10C badge')
    elif pinfo['airframe']=='A-10C':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/a-10Alphaed.png')
        ax.figure.figimage(aircraftBadge, -30, 750, alpha=.75, zorder=1)
        print('adding A-10C badge')
    elif pinfo['airframe']=='A-4E-C':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/skyhawk_alpha.png')
        ax.figure.figimage(aircraftBadge, -30, 770, alpha=.75, zorder=1)
        print('adding A-4E-C badge')
    elif pinfo['airframe']=='F-16C_50':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/f-16_alphaed.png')
        ax.figure.figimage(aircraftBadge, -30, 770, alpha=.75, zorder=1)
        print('adding F-16C_50 badge')    
    elif pinfo['airframe']=='UH-1H':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/uh-1_alphaed.png')
        ax.figure.figimage(aircraftBadge, -50, 780, alpha=.75, zorder=1)
        print('adding UH-1H badge')  
    elif pinfo['airframe']=='P-51D-30-NA':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/p51alphaed.png')
        ax.figure.figimage(aircraftBadge, -50, 770, alpha=.75, zorder=1)
        print('adding P-51D-30-NA badge')     
    elif pinfo['airframe']=='F-5E-3':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/F-5Ealphaed.png')
        ax.figure.figimage(aircraftBadge, -25, 780, alpha=.75, zorder=1)
        print('adding F-5E-3 badge')
    elif pinfo['airframe']=='VSN_F104G':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/starfighter_alpha.png')
        ax.figure.figimage(aircraftBadge, -0, 770, alpha=.75, zorder=1)
        print('adding F-104 badge') 
    elif pinfo['airframe']=='F-86F Sabre':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/sabre_Alpha.png')
        ax.figure.figimage(aircraftBadge, -0, 770, alpha=.75, zorder=1)
        print('adding F-86 badge')
    elif pinfo['airframe']=='Mi-24P':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Images/Hind_Alpha.png')
        ax.figure.figimage(aircraftBadge, -0, 810, alpha=.75, zorder=1)
        print('adding Hind badge') 
    elif pinfo['airframe']=='AH-64D_BLK_II':
        # Aircraft Badge top left corner
        aircraftBadge = plt.imread('Apache_Alpha.png')
        ax.figure.figimage(aircraftBadge, -10, 770, alpha=.75, zorder=1)
        print('adding Apache badge') 
    else:
    
        print('badge error, unknown aircraft')

    fig.savefig('targetSheet.png', facecolor=facecolor)  

    print('Plotting targetsheet END')


   
def parseFilename(vinput):
    
    pinfo ={}
    p = Path(vinput)
    last_modified = p.stat().st_mtime
    mod_timestamp = datetime.datetime.fromtimestamp(last_modified)
    
   
    #modificationTime = time.ctime ( fileStatsObj [ last_modified ] )
#    print("Last Modified Time : ", modificationTime )
    pinfo ={}
    p = Path(vinput)
    last_modified = p.stat().st_mtime
    mod_timestamp = datetime.datetime.fromtimestamp(last_modified)
    
   
    #modificationTime = time.ctime ( fileStatsObj [ last_modified ] )
#    print("Last Modified Time : ", modificationTime )
    timestampStr = mod_timestamp.strftime("%b %d %Y, %H:%M:%S")
    pinfo['time']=timestampStr
    

    print(timestampStr)
    ps = p.stem

    print(ps)
    ps=ps.replace('RANGERESULTS-','')
    ind = ps.find('-')
    print(ps)
    ps = ps[ind+1:-1]
    print(ps)
    ind = ps.rfind('-')
    ps = ps[0:ind]
    """
    hornet = 'FA-18C_hornet'
    tomcatB = 'F-14B'
    harrier = 'AV8BNA'#added 1/22/21
    skyhawk = 'A-4E-C'#added 2/1/21
    tomcatA = 'F-14A-135-GR'#added 2/19/21
    goshawk = 'T-45'#added 5/6/21

    if hornet in ps:
        print('contains hornet')
        ps = ps.replace(hornet,'')
        pinfo['aircraft']='F/A-18C'
    elif goshawk in ps:
        print('contains goshawk') #added 5/6/21
        ps = ps.replace(goshawk,'')
        pinfo['aircraft']='T-45C'    
    elif tomcatA in ps:
        print('contains tomcatA')
        ps = ps.replace(tomcatA,'')
        pinfo['aircraft']='F-14A-135-GR'
    elif tomcatB in ps:
        print('contains tomcatB')
        ps = ps.replace(tomcatB,'')
        pinfo['aircraft']='F-14B'
    elif harrier in ps:#added 1/22/21
        print('contains av8bna')
        ps = ps.replace(harrier, '')
        pinfo['aircraft']='AV-8B' 
    elif skyhawk in ps:#added 2/1/21
        print('contains A-4E-C')
        ps = ps.replace(skyhawk, '')
        pinfo['aircraft']='A-4E-C'     
    else:
        print('unknown aircraft.')
    """
    print(ps)
    
    
    pinfo['callsign']=ps[0:-1]
    return pinfo
def getCallsign(input):
    print('Getting callsign from: ', input)
    
# %%

# %%

#%%

# **** use line below for and insert your target folder - by default in MOOSE will be your Logs folder
targetfolder = targetSheetPath

#targetfolder = 'C:/temp'
p = Path(str(targetfolder))

#print('Latest path: ', latest_path)

targetfile = getRecentTargetsheet(targetfolder)

if targetfile == '':
    print('No target file found')
    quit()
    
print('Final file is:', targetfile)

#targetfile = '../targetsheets/AIRBOSS-CVN74_Targetsheet-PyCo00_F-14B-0008.csv'

pinfo = parseFilename(targetfile)

ts = ReadTargetsheet(targetfile)
pinfo['airframe']=ts['Airframe']
plotTargetsheet(ts, pinfo)
#print('Name: ', ts['Name'], 'Target: ', ts['Target'], 'Distance: ', ts['Distance'], ' Radial: ', ts['Radial'], ' Quality: ', ts['Quality'], 'Rounds Fired', ts['Rounds Fired'], 'Rounds Hit', ts['Rounds Hit'] ,'Rounds Quality', ts['Rounds Quality'],'Attack Heading', ts['Attack Heading'], 'Airframe', ts['Airframe'] )

# %% this is a cell here
print('Name: ', ts['Name'], 'Target: ', ts['Target'], 'Distance: ', ts['Distance'], ' Radial: ', ts['Radial'], ' Quality: ', ts['Quality'], 'Rounds Fired', ts['Rounds Fired'], 'Rounds Hit', ts['Rounds Hit'] ,'Rounds Quality', ts['Rounds Quality'],'Attack Heading', ts['Attack Heading'], 'Airframe', ts['Airframe'] )
#Name,Target,Distance,Radial,Quality,Rounds Fired,Rounds Hit,Rounds Quality,Weapon,Airframe,Mission Time,OS Time                                          
#if ts['Details'] == '':
#    print('no comments in grade')
#else:
#    print('there ARE comments in grade')
