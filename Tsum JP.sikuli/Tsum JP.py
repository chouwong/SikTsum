# Destop top resoultion or windows size should be 1344x756
import datetime

# Settings 
scrollFlag = "PD" # PD - pageDown; PU - pageUp;
lang = "JP" # JP - Japan version; US - English version;
maxDrag = 60 # The number of scroll before claim coins
existDelay = 0.1 # The check if image exist delay in second
waitDelay = 30 # The image wait in second

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
Debug.setUserLogFile(getBundlePath()+"/SikTsum"+lang+".log")
Debug.on(4)

# Declare some search region to speed up 
titleRegion = Region(449,124,442,155) 
redHeartRegion = Region(763,209,104,378)
claimCoinRegion = Region(730,207,128,355)
mailBoxRegion = Region(460,105,433,623)
middleDialogRegion = Region(453,224,444,294)

def claimCoins():  
    Debug.user("*** claimCoins START ***")
    
    titleRegion.wait(lang+"/RankingTitle.png", waitDelay)
    if titleRegion.exists(lang+"/mailBoxIcon.png", existDelay): # 若螢幕有郵件
        click(titleRegion.getLastMatch())  # 點取郵件   
    while True:
        failCount = 0
        claimCount = 0
        while True:
            titleRegion.wait(lang+"/mailboxTitle.png", waitDelay)
            
            if claimCoinRegion.exists(lang+"/claimCoin.png", existDelay):
                click(claimCoinRegion.getLastMatch())
                claimCount += 1
                failCount = 0
                Region(575,257,187,63).wait(lang+"/coinConfirmDialog.png", waitDelay)
                while middleDialogRegion.exists(lang+"/coinConfirmOk.png", existDelay): 
                    click(middleDialogRegion.getLastMatch())
                click(middleDialogRegion.getLastMatch())
                middleDialogRegion.wait(lang+"/coinNotifyDialog.png", waitDelay)
                while middleDialogRegion.exists(lang+"/coinNotifyDialog.png",existDelay):
                    click(middleDialogRegion.getLastMatch())
            else:
                failCount += 1
            if mailBoxRegion.exists(lang+"/mailboxEmpty.png", existDelay):
                Debug.user("End of claim, collected %d times!" % claimCount)
                mailBoxRegion.click(lang+"/mailBoxClose.png")
                break
            if failCount > 5 and not claimCoinRegion.exists(lang+"/claimCoin.png", existDelay):
                Debug.user("No more coins, collected %d times!" % claimCount)
                mailBoxRegion.click(lang+"/mailBoxClose.png")
                break  
       
        if claimCount < 99:
            break
    
    Debug.user("*** claimCoins END ***")
# End claim coins

def sendHearts(maxDrag):
    global scrollFlag
    
    Debug.user("*** sendHearts START ***")
    
    titleRegion.wait(lang+"/RankingTitle.png", waitDelay)
    dragCount = 0 
    while True:        
        breakFlag = False    
        while True:
            try:
                if redHeartRegion.exists(lang+"/redHeart.png"): 
                    click(redHeartRegion.getLastMatch()) # 送心
                    Region(502,257,336,62).wait(Pattern(lang+"/heartConfirmDialog.png").similar(0.50), waitDelay)
                    while middleDialogRegion.exists(lang+"/heartConfirmOk.png", existDelay):
                        click(middleDialogRegion.getLastMatch())
                    middleDialogRegion.wait(lang+"/heartNotifyDialog.png", waitDelay) 
                    while middleDialogRegion.exists(lang+"/heartNotifyDialog.png", existDelay): click(Location(674, 572))
                else:
                    if titleRegion.exists(lang+"/RankingTitle.png", existDelay) and not redHeartRegion.exists(lang+"/redHeart.png", existDelay):
                        break
            except FindFailed:
                sentHeartErrorFix()
        if dragCount >= maxDrag: 
            break        
        if Region(506,237,54,325).exists(Pattern(lang+"/topOfList.png").similar(0.97), existDelay): #Top of list reached 
            scrollFlag = "PD"
            Debug.user("Top reached; scrollFlag: %s" % scrollFlag)
            breakFlag = True
        if Region(472,477,101,79).exists(lang+"/endOfList.png", existDelay) : # End of list reached
            scrollFlag = "PU"
            Debug.user("Bottom reached; scrollFlag: %s" % scrollFlag)
            breakFlag = True
        titleRegion.wait(lang+"/RankingTitle.png", waitDelay)
        ranking = titleRegion.getLastMatch()
        if scrollFlag == "PD":            
            dragDrop(Location(ranking.x,ranking.y+270),Location(ranking.x,ranking.y+50))
            dragCount+=1
        if scrollFlag == "PU":            
            dragDrop(Location(ranking.x,ranking.y+50),Location(ranking.x,ranking.y+270))
            dragCount+=1
        if breakFlag:
            break
    Debug.user("*** sendHearts END ***")
# End send hearts

# Abnormal handling
def sentHeartErrorFix():
    Debug.user("*** sentHeartErrorFix START ***")

    # Clear Player Info Dialog
    searchRegion = Region(543,499,214,156)
    if searchRegion.exists(lang+"/playerInfoClose.png", existDelay):
        click(searchRegion.getLastMatch())
        print "Fixed player info dialog!"
    
    Debug.user("*** sentHeartErrorFix END ***")       
# End Abnormal handling

# Start Main Program
while True:
    claimCoins()
    sendHearts(maxDrag)

# End Main Program    