# Destop top resoultion or windows size should be 1344x756
import datetime
import shutil

# Settings 
scrollFlag = "PD" # PD - pageDown; PU - pageUp;
lang = "JP" # JP - Japan version; US - English version;
maxDrag = 60 # The number of scroll before claim coins
existDelay = 0.1 # The check if image exist delay in second
waitDelay = 10 # The image wait in second
waitRetryCount = 3 # No of retury before giving up
clickRetryCount = 5 # No of click before giving up
imagePath = getBundlePath()

# Advance settings for better program peformance
Settings.ClickDelay = 0.1
Settings.MoveMouseDelay = 0.1
Settings.WaitScanRate = 20              
#Settings.ObserveScanRate = 10
Settings.SlowMotionDelay = 0

# For Logging only
Settings.UserLogs = True #False: user log calls are ignored
Settings.UserLogPrefix = "user" #message prefix
Settings.UserLogTime = True
#Debug.setUserLogFile(imagePath+"/SikTsum"+lang+".log")
Debug.on(1)

# Declare some search region to speed up 
titleRegion = Region(449,124,442,155) 
redHeartRegion = Region(763,209,104,378)
claimCoinRegion = Region(730,207,128,355)
mailBoxRegion = Region(460,105,433,623)
middleDialogRegion = Region(453,224,444,294)
bottomRegion = Region(453,587,440,180)

# Register hot key to capture images
def captureImages(event):
    popup("Please move to leader board!")
    shutil.move(capture(Region(512,212,166,32)), imagePath+"/capture/RankingTitle.png")
    shutil.move(capture(Region(787,155,29,52)), imagePath+"/capture/mailBoxIcon.png") 
    popup("Please scroll for red heart!")
    tmpImagePath = capture("Please select a red heart!")
    if tmpImagePath is not None:
        shutil.move(tmpImagePath, imagePath+"/capture/redHeart.png")

    popup("Please scroll to top of list!")
    tmpImagePath = capture("Please select the top of list image!")
    if tmpImagePath is not None:
        shutil.move(tmpImagePath, imagePath+"/capture/topOfList.png")

    popup("Please scroll to end of list!")
    tmpImagePath = capture("Please select the end of list image!")
    if tmpImagePath is not None:
        shutil.move(tmpImagePath, imagePath+"/capture/endOfList.png")

# Register listener for captureImages
Env.addHotkey(Key.F1, KeyModifier.ALT+KeyModifier.CTRL, captureImages)

# Subroutine for wait and click
def myWait(region, object, delay=waitDelay):
    failCount = 0
    while True:
        try:
            region.wait(object, delay)
            return True
        except FindFailed:
            generalErrorFix()
            failCount += 1 
            if failCount > waitRetryCount:
                Debug.log("myWait failed after %d attempts!" % failCount)
                return False
                
# Subroutine for click
def myClick(region, searchObject, clickObject=None, delay=existDelay):
    clickCount = 0
    success = True
    while region.exists(searchObject, delay):
        if clickObject == None:
            clickObject = region.getLastMatch()
        region.click(clickObject)
        clickCount += 1
        if clickCount > clickRetryCount:
            Debug.log("myClick failed after %d attempts!" % clickCount)
            success = False
            break
    wait(0.1)
    return success

# Subroutine for claim coins
def claimCoins():  
    Debug.log("*** claimCoins START ***")
    
    myWait(titleRegion, lang+"/RankingTitle.png") 
    while True:        
        failCount = 0
        claimCount = 0

        myClick(titleRegion, lang+"/mailBoxIcon.png")

        while True:
            myWait(titleRegion, lang+"/mailboxTitle.png")
            
            if claimCoinRegion.exists(lang+"/claimCoin.png", existDelay):
                myClick(claimCoinRegion, lang+"/claimCoin.png")
                claimCount += 1
                failCount = 0
                
                # Confirm dialog
                if myWait(Region(575,257,187,63), lang+"/coinConfirmDialog.png"):
                    myClick(middleDialogRegion, lang+"/coinConfirmOk.png")
                
                # Notify dialog
                if myWait(middleDialogRegion, lang+"/coinNotifyDialog.png"):
                    myClick(middleDialogRegion, lang+"/coinNotifyDialog.png")
                    
            else:
                failCount += 1
            
            # Empty mailbox
            if mailBoxRegion.exists(lang+"/mailboxEmpty.png", existDelay):
                Debug.log("Empty mailbox, collected %d times!" % claimCount)
                break

            # No more coins
            if failCount > 5:
                Debug.log("No more coins, collected %d times!" % claimCount)
                break  

        wait(0.2)
        if mailBoxRegion.exists(lang+"/mailboxTitle.png", existDelay):
            mailBoxRegion.click(lang+"/mailBoxClose.png")
        
        if claimCount < 99:
            break
    
    Debug.log("*** claimCoins END ***")

# Subroutine for send hearts
def sendHearts(maxDrag):
    global scrollFlag
    
    Debug.log("*** sendHearts START ***")
    
    myWait(titleRegion, lang+"/RankingTitle.png")
    dragCount = 0 
    while True:        
        breakFlag = False    
        while True:
            if redHeartRegion.exists(lang+"/redHeart.png", existDelay): 
                myClick(redHeartRegion, lang+"/redHeart.png")
            else:
                if titleRegion.exists(lang+"/RankingTitle.png", existDelay) and not redHeartRegion.exists(lang+"/redHeart.png", existDelay):
                    break

            # Close player info
            myClick(Region(543,499,214,156), lang+"/playerInfoClose.png")
            if myWait(Region(502,257,336,62), Pattern(lang+"/heartConfirmDialog.png").similar(0.50)):
                myClick(middleDialogRegion, lang+"/heartConfirmOk.png")
            if myWait(middleDialogRegion, lang+"/heartNotifyDialog.png"):     
                myClick(middleDialogRegion, lang+"/heartNotifyDialog.png", Location(674, 572))

            # Clear connection problem
            if middleDialogRegion.exists(lang+"/errorDialogTitleScreen.png", existDelay):
                myClick(middleDialogRegion, lang+"/errorDialogRetry.png")
                Debug.log("Tried to fix Error Dialog!")

        if dragCount >= maxDrag: 
            break        
        if Region(506,237,54,325).exists(Pattern(lang+"/topOfList.png").similar(0.97), existDelay): #Top of list reached 
            scrollFlag = "PD"
            Debug.log("Top reached; scrollFlag: %s" % scrollFlag)
            breakFlag = True
        if Region(530,223,53,339).exists(lang+"/endOfList.png", existDelay) : # End of list reached
            scrollFlag = "PU"
            Debug.log("Bottom reached; scrollFlag: %s" % scrollFlag)
            breakFlag = True
        if scrollFlag == "PD":            
            dragDrop(Location(508,209+330),Location(508,209+100))
            dragCount+=1
        if scrollFlag == "PU":            
            dragDrop(Location(508,209+50),Location(508,209+270))
            dragCount+=1
        if breakFlag:
            break
    Debug.log("*** sendHearts END ***")

def generalErrorFix():
    Debug.log("*** generalErrorFix Start ***")       

    # Clear error code dialog
    if middleDialogRegion.exists(lang+"/errorDialogTitleScreen.png", existDelay):
        myClick(middleDialogRegion, lang+"/errorDialogRetry.png")
        Debug.log("Tried to fix Error Dialog!")

    # Return back to Ranking
    if bottomRegion.exists(lang+"/playStart.png"):
        myClick(bottomRegion, lang+"/playBack.png")
        Debug.log("Tried to back to Ranking!")

    # Close mail box 
    #if mailBoxRegion.exists(lang+"/mailboxTitle.png", existDelay):
    #    mailBoxRegion.click(lang+"/mailBoxClose.png")
    #    Debug.log("Tried to close mailbox!")

    Debug.log("*** generalErrorFix END ***")           

# Start Main Program
while True:
    generalErrorFix()
    claimCoins()
    sendHearts(maxDrag)
# End Main Program    