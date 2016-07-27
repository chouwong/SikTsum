# Destop top resoultion or windows size should be 1344x756
import datetime

# Some tunable settings 
scrollFlag = "PD" # PD - pageDown; PU - pageUp
maxDrag = 60 # The number of scroll before claim coins
existDelay = 0.1 # The check if image exist delay in second
waitDelay = 30 # The image wait in second

# Some advance settings for better program peformance
Settings.MoveMouseDelay = 0.1                
Settings.ObserveScanRate = 10
Settings.SlowMotionDelay = 0

# Declare some search region to speed up 
rankingHeaderRegion = Region(475,191,236,79)
redHeartRegion = Region(763,209,104,378)
claimCoinRegion = Region(730,207,128,355)
mailBoxRegion = Region(471,145,407,585)
middleDialogRegion = Region(453,224,444,294)


def logMsg(msg):
    print datetime.datetime.now().isoformat() + " " + msg

def myClick(button):
    while True:
        if click(button) == 1: 
            break
        else:
            wait(0.1)
        
def claimCoins():    
    logMsg("*** claimCoins START ***")
    
    rankingHeaderRegion.wait("RankingHeader.png", waitDelay)
    if exists("mailBoxIcon.png", existDelay): # 若螢幕有郵件
        myClick(getLastMatch())  # 點取郵件   
    while True:
        failCount = 0
        claimCount = 0
        while True:    
            if claimCoinRegion.exists("claimCoin.png", existDelay):
                click(claimCoinRegion.getLastMatch())
                claimCount += 1
                failCount = 0
                Region(575,257,187,63).wait("1469547378925.png", waitDelay)
                wait(0.2)
                middleDialogRegion.click("1469546227253.png")         
                middleDialogRegion.wait("claimNotifyDialog.png", waitDelay)
                click(middleDialogRegion.getLastMatch())
            else:
                failCount += 1
            if mailBoxRegion.exists("mailboxEmpty.png", existDelay):
                logMsg("End of claim: {0}".format(claimCount))
                mailBoxRegion.click("mailBoxDialogClose.png")
                break
            if failCount > 10 and not claimCoinRegion.exists("claimCoin.png", existDelay):
                logMsg("No more coins: {0}".format(claimCount))
                mailBoxRegion.click("mailBoxDialogClose.png")
                break  
       
        if claimCount < 99:
            break
    
    logMsg("*** claimCoins END ***")
# End claim coins

def sendHearts(maxDrag):
    global scrollFlag, rankingHeaderRegion, redHeartRegion
    
    logMsg("*** sendHearts START ***")
    
    rankingHeaderRegion.wait("RankingHeader.png", waitDelay)
    dragCount = 0 
    while True:        
        breakFlag = False    
        while True:
            try:
                if redHeartRegion.exists("redHeart.png"): 
                    click(redHeartRegion.getLastMatch()) # 送心
                    Region(502,257,336,62).wait(Pattern("sentHeart.png").similar(0.50), waitDelay)
                    wait(0.2)
                    middleDialogRegion.click("1469293322575.png")
                    middleDialogRegion.wait("1469293482923.png", waitDelay) 
                    click(Location(674, 572))  #按"愛心已寄送"
                    wait(0.3)
                else:
                    if rankingHeaderRegion.exists("RankingHeader.png", existDelay) and not redHeartRegion.exists("redHeart.png", existDelay):
                        break
            except FindFailed:
                sentHeartErrorFix()
        if dragCount >= maxDrag: 
            break        
        if Region(506,237,54,325).exists(Pattern("1469295945522.png").similar(0.97), existDelay): #Top of list reached 
            scrollFlag = "PD"
            logMsg("Top reached; scrollFlag: {0}".format(scrollFlag))
            breakFlag = True
        if Region(472,477,101,79).exists("1469296699039.png", existDelay) : # End of list reached
            scrollFlag = "PU"
            logMsg("Bottom reached; scrollFlag: {0}".format(scrollFlag))
            breakFlag = True
        rankingHeaderRegion.wait("RankingHeader.png", waitDelay)
        ranking = rankingHeaderRegion.getLastMatch()
        if scrollFlag == "PD":            
            dragDrop(Location(ranking.x,ranking.y+270),Location(ranking.x,ranking.y+50))
            dragCount+=1
        if scrollFlag == "PU":            
            dragDrop(Location(ranking.x,ranking.y+50),Location(ranking.x,ranking.y+270))
            dragCount+=1
        if breakFlag:
            break
    logMsg("*** sendHearts END ***")
# End send hearts

# Abnormal handling
def sentHeartErrorFix():
    logMsg("*** sentHeartErrorFix START ***")

    # Clear Player Info Dialog
    searchRegion = Region(543,499,214,156)
    if searchRegion.exists("1469333898742.png",existDelay):
        click(searchRegion.getLastMatch())
        print "Fixed player info dialog!"
    
    logMsg("*** sentHeartErrorFix END ***")       
# End Abnormal handling

# Start Main Program
while True:
    claimCoins()
    sendHearts(maxDrag)

# End Main Program    