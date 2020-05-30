import time, os, platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Arrays for Resulting Download and Upload Speeds
downloadResults = []
uploadResults = []

#Variables for convenience
numberOfTrials = None
rootDir = os.path.dirname(os.path.abspath(__file__))
chromeDriver = None
ublock = None
testIsInProgress = True
started = False
trialCount = None
waitTime = 2
testsSuccessful = 0
testsFailed = 0
startTime = None
endTime = None

#Setting Number of Trials to Run
def settingNumberofTrials():
    global numberOfTrials
    try:
        numberOfTrials = (input("How many speed tests do you wish to do? "))
        if numberOfTrials < 0:
            print("Incorrect Input......PLease Try Again or Type 0 to Quit Execution")
            time.sleep(2)
            settingNumberofTrials()
        elif numberOfTrials == 0:
            os._exit(1)
    except:
        print("Incorrect Input......PLease Try Again or Type 0 to Quit Execution")
        time.sleep(2)
        settingNumberofTrials()

#Setting up Chrome Driver using OS
def settingChromeDriver():
    global chromeDriver, ublock
    osType = platform.system()
    if osType == "Windows":
        chromeDriver = rootDir + r"\ChromeDrivers\chromedriver_win.exe"
        ublock = rootDir + r'\ublock-ver1.26.0_0'
    elif osType == "Linux":
        chromeDriver = rootDir + r"/ChromeDrivers/chromedriver_linux"
        ublock = rootDir + r'/ublock-ver1.26.0_0'
    elif osType == "macOS":
        chromeDriver = rootDir + r"/ChromeDrivers/chromedriver_mac"
        ublock = rootDir + r'/ublock-ver1.26.0_0'


#Setting up the broswer
try:
    settingNumberofTrials()
    settingChromeDriver()
    print("Opening Chrome....")
    startTime = time.time()
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + ublock)
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(executable_path = chromeDriver, options = chrome_options)
    driver.create_options()
    driver.get('http://www.speedtest.net')
    print("Chrome Opened!")
except:
    print("Chrome could not open.")

#Starts the speed test
def startTest():
    global started
    if not started:
        try:
            goButton = driver.find_element_by_xpath(
                '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
            goButton.click()
            started = True
            print(f"Test {trialCount} Started!")
        except:
            print("Could not start test!")
            testsFailed += 1
            started = False

#Waits for the individual test to be done before proceeding
def testInProgress():
    global started, testIsInProgress
    if started:
        try:
            goButton = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
            styles = goButton.get_property("style")
            while styles.index('display') >= 0:
                styles = goButton.get_property("style")
                testIsInProgress = True
            if testIsInProgress:
                print("Testing...")
        except:
            testIsInProgress = False
            print(f"Test {trialCount} Finished!")

#Adds resulting download speed to array
def addResult():
    global started, testIsInProgress, testsSuccessful, testsFailed
    if not testIsInProgress and started:
        try:
            downloadResult = float((driver.find_element_by_xpath(
                '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text))
            downloadResults.append(downloadResult)

            uploadResult = float((driver.find_element_by_xpath(
                '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text))
            uploadResults.append(uploadResult)
            testsSuccessful += 1
        except:
            print("Error!!")
            testsFailed += 1
        started = False

def average(array):
    sum = 0
    for i in array:
        sum += i
    try:
        return sum/len(array)
    except:
        print("Error!")

#Iterate through speed tests (n) times
def redoTest():
    global trialCount, numberOfTrials
    for i in range(numberOfTrials):
        trialCount = i + 1
        time.sleep(waitTime)
        startTest()
        time.sleep(waitTime)
        testInProgress()
        time.sleep(waitTime)
        addResult()


redoTest()
endTime = time.time()

print(f"\nTotal Time: {round(endTime - startTime, 2)} Seconds")
print(f"\nDownload Results: {downloadResults} ----- Average: {round(average(downloadResults), 2)} Mbps")
print(f"\nUpload Results: {uploadResults} ----- Average: {round(average(uploadResults), 2)} Mbps")
print(f"\nSuccess: {testsSuccessful} Trials")
print(f"Failed: {testsFailed} Trials")

#Close browser when all trials are done
print("\nClosing Chrome....")
driver.quit()
print("Chrome Closed!")
