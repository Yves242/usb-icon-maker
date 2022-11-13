import os, string, subprocess, shutil, time
from locale import atoi
from PIL import Image
from termcolor import colored
from tkinter import filedialog, Tk
from pathlib import Path

# DEFINES
usedIconIdentifierString = "-used-icon-label.ico"   # used for label identifier string
appVersion = "v 4.3.0"

# Simple cmd-based function that gets available drives and their names. Returns array
def getDrivesAndNames():

    # 1-line code below adapted from https://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-windows-drives 
    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

    # stores final return array
    drivesAndLetters = []

    for driveletter in available_drives:
        
        # 1-line code below adopted from https://stackoverflow.com/questions/8319264/how-can-i-get-the-name-of-a-drive-in-python
        drivename = subprocess.check_output(["cmd","/c vol "+driveletter]).decode().split("\r\n")[0]

        if (driveletter[0] != "C"):   # Do not add to list if "C"  
            drivesAndLetters.append(driveletter + drivename[21:-1] + drivename[-1])

    return drivesAndLetters

# Simple function that counts down until a given second, and will prompt message.
def countdown(seconds, message):
    while (seconds >= 0):
        cleanScreen()
        if (seconds == 0):
            print(message + " " + str(seconds) + ".")
        else:
            print(message + " " + str(seconds))
            time.sleep(1)
        seconds = seconds-1

# Simple function that prompts open file. Returns array of image path/s
def openImageFiles():
    
    # prompt window
    root = Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    imagePathsTuple = filedialog.askopenfilenames(title="Open image files", filetypes=[("image files","*.png"), ("image files","*.jpg"), ("image files","*.jpeg")])
    root.destroy()

    # convert to array
    imagePaths = []
    for image in imagePathsTuple:
        imagePaths.append(image)
        
    return imagePaths

# Simple function that prompts open file. Returns string of single image path 
def openImageFile():
    
    # prompt window
    root = Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    imagePathTuple = filedialog.askopenfilename(title="Open image file", filetypes=[("image file","*.png"), ("image file","*.jpg"), ("image file","*.jpeg")])
    root.destroy()

    return imagePathTuple

# Simple function that cleans screen. Returns nothing
def cleanScreen():
    os.system("cls")

# Simple function that hides that unhides a given file
def hideFile(filename):
    os.system('cmd /c "IF EXIST ' + filename + ' (attrib +h +s +r +a ' + filename + ') & exit"')

# Simple function that unhides a given file
def unhideFile(filename):
    os.system('cmd /c "IF EXIST ' + filename + ' (attrib -h -r -s -a ' + filename + ') & exit"')

# Simple function that dletes a given filename
def deleteFile(filename):
    os.system('cmd /c "IF EXIST ' + filename + ' (attrib -h -r -s -a ' + filename + ' & del ' + filename + ') & exit"')

# Simple function that replaces cmd-sensitive special characters with "-"
def removeSpecialCharacters(filename):
    i=0
    newFilename = ""
    while (i<len(filename)):
        if (filename[i] in (" ", "!", "%", "^", "&", "$", "*", "(", ")", "'", "\"", "\\")):
            newFilename = newFilename+"-"
        else:
            newFilename = newFilename+filename[i]
        i = i+1
    return newFilename

# General function that finds files with specific extension. Returns string array
def findExtensionFiles(dir, extension):

    # variable
    extensionFiles = []

    # start file search
    for path in os.scandir(dir):
        if (path.is_file()):
            str = path.name.lower()
            if (str[len(str)-len(extension):len(str)] == extension):
                extensionFiles.append(path.name)
    
    # sort for organization
    if (len(extensionFiles) > 1):
        extensionFiles = sorted(extensionFiles)

    return extensionFiles

# General function that finds any file. Returns Boolean
def fileExists(filename):

    # start file search
    for path in os.scandir(os.getcwd()):
        if (path.is_file() and path.name == filename):
            return True
    
    return False

# function that converts an image to icon. Returns image file name.
def convertImageToIcon(imgFile):

    # Get image file name
    imgSplitted = imgFile.split("/")
    icoFilename = imgSplitted[-1]
    returnval = icoFilename

    file = Image.open(Path(imgFile))

    # save image as proper filename
    if (imgFile[-4] == "."): # if of format .jpg, .png, or .gif
        icoFilename = imgFile[0:len(imgFile)-4] + ".ico"        
    else: # else if of format .jpeg
        icoFilename = imgFile[0:len(imgFile)-5] + ".ico"

    # save using proper image filename
    file.save(icoFilename)

    return returnval

# function that makes the 'autorun.inf' based on a given image. Returns Boolean, String as notification
def makeAutorunFile(drive, imgFile):

    # unhide autorun.inf
    unhideFile(drive + "autorun.inf")

    # Boolean error switch
    isError = False

    # if 'autorun.inf' already exists, ask user what to do.
    if fileExists(drive + "autorun.inf"):
        decision = ""
        while (decision not in ("y", "Y")):
            
            print("User selected image file '" + colored((drive + imgFile), "green") + "'.\n")
            print("Configuration file 'autorun.inf' already exists. \nYou may have already placed an icon on this device before.\n\n")
            
            if (isError):
                print(colored("Error: Please type either 'y' or 'n' only.", "red"))
                isError = False # reset Boolean error switch
            
            decision = input("Overwrite to add new icon to this device? [y/n]\n")        
            cleanScreen()
            if (decision in ("n", "N")):
                return False, "Aborting process. User decided not to overwrite 'autorun.inf' file.\n"
            elif (decision not in ("y", "Y")):
                isError = True

    # if 'autorun.inf' does not exist, or user decided to overwrite, convert and save image as icon file.
    file = Image.open(drive + imgFile)

    # find if it is using a 3-char or a 4-char extension 
    if (imgFile[len(imgFile)-3:1] == "."):
        usedIconName = removeSpecialCharacters(imgFile)[0:len(imgFile)-3] + usedIconIdentifierString 
    else:
        usedIconName = removeSpecialCharacters(imgFile)[0:len(imgFile)-4] + usedIconIdentifierString
    
    # remove old files with format *-used-icon-label.ico.
    oldFiles = findExtensionFiles(drive, usedIconIdentifierString)
    if (len(oldFiles) > 0):
        i=0
        while (i< len(oldFiles)):
            deleteFile(oldFiles[i])
            i = i+1

    # save file as such name without space
    unhideFile(drive + usedIconName)
    file.save(drive + usedIconName) 
    
    # create new file 
    with open(drive + 'autorun.inf', 'w') as f:
        f.write('[AutoRun.Amd64]\nicon="' + usedIconName + '"\n\n[AutoRun]\nicon="' + usedIconName + '"')
    
    # hide 'autorun.inf' and the used icon file and exit function
    hideFile(drive + "autorun.inf")
    hideFile(drive + usedIconName)
    return True, "Successfully added image as label."


# Main functions below

# Function that lets user choose image as icon for a specific drive. Returns Boolean, String as notification text
def chooseImageAsDriveIcon():
    
    # clean screen
    cleanScreen()

    # Get usable image file list from given drive
    driveArray = getDrivesAndNames()

    # if driveArray has no element
    if (len(driveArray) == 0):
        return False, "There are no USB devices or other storage devices!"

    elif (len(driveArray) > 0):

        errorCount = 0
        driveChoice = ""

        # Do this until user selects drive to place icon
        while(True):
            cleanScreen()

            print("The program found these drives on your device:\n")
            buffer = 1

            for element in driveArray:
                print("[" + str(buffer) + "] " + element)
                buffer = buffer + 1
            print()

            if (errorCount > 0):
                print(colored("Error #" + str(errorCount) + ": Wrong choice number.", "red"))

            driveChoice = input("Which drive would you like to add a USB icon on? (To exit, type 'exit')\nChoice number: ")

            # check for exit prompt
            if (driveChoice.lower() in ["exit"]):
                return(False, "User decided to exit option 1.")

            # else, check if numeric
            elif (driveChoice.isnumeric()):
                if (atoi(driveChoice) <= len(driveArray)):
                    if (atoi(driveChoice) > 0):
                        break

            errorCount = errorCount + 1

        # main drive letter of format "X:/"
        drive = driveArray[atoi(driveChoice)-1][0] + ":/"

        # Start of modified function 
        cleanScreen()
        
        # Show notification
        print("Selecting image...")
        time.sleep(0.25)

        # Get image files
        imgFile = openImageFile()

        if (len(imgFile) == 0):      
            return False, "User cancelled selecting image."

        else:
            convertedIcon = convertImageToIcon(imgFile)

            # Get proper icon location
            convertedIconLocation = imgFile
            if (imgFile[-4] == "."): # if of format .jpg, .png, or .gif
                convertedIconLocation = convertedIconLocation[0:len(convertedIconLocation)-4] + ".ico"        
            else: # else if of format .jpeg
                convertedIconLocation = convertedIconLocation[0:len(convertedIconLocation)-5] + ".ico"

            shutil.copyfile(convertedIconLocation, drive+convertedIcon)
            makeAutorunFile(drive, convertedIcon)
            return True, "Successfully assigned '" + convertedIcon + "' to drive '" + drive[0] + ":'."            


    else:
        return False, "Unexpected program error occurred while searching for files."

# Function that lets user choose icon/s based on image files. Returns Boolean, String as notification text
def chooseImageToConvert():
    
    # clean screen
    cleanScreen()
    
    # Show notification
    print("Selecting image...")
    time.sleep(0.25)

    # Get image files
    imgFiles = openImageFiles()

    if (len(imgFiles) == 0):      

        return False, "User cancelled file conversion operation."

    elif (len(imgFiles) > 0):     
        
        for eachImage in imgFiles:
            convertImageToIcon(eachImage)
        
        if (len(imgFiles) == 1):
            return True, "Successfully converted " + str(len(imgFiles)) + " image file to .ico file."
        else:
            return True, "Successfully converted " + str(len(imgFiles)) + " image files to .ico files."            

    else:
        return False, "Unexpected program error occurred while searching for files."

# This occurs if it was detected that application is running on topmost directory.
def menu():
        
    wrongChoice = False
    errorCounter = 0
    notification = (True, "")

    # Do always until user exits.
    while (True):

        cleanScreen()

        if (notification[1] != ""):

            # print out notification based on success/failure
            if (notification[0] == True):                
                print("Status: " + colored(notification[1] + "\n", 'green'))
            else:
                print("Status: " + colored(notification[1] + "\n", 'yellow'))

            # reset boolean switch
            notification = (True, "") 

        print(colored("USB Icon Maker ", "cyan") + colored("(", "magenta") + colored(appVersion, "yellow") + colored(")\n", "magenta"))
        print("What would you like to do?\n")
        print("[1] Use images as icon for your USB Drive")
        print("[2] Convert an image to .ico file (optional)")
        print("[0] Exit\n")

        # notification text upon wrong choice
        if (wrongChoice):
            print(colored("Error #" + str(errorCounter) + ": Wrong choice number.", "red"))
            wrongChoice = False # reset failure switch

        choice = input("Choice number: ")

        if (choice.lower() in ("0", "exit")):
            exit()
        elif (choice.isnumeric()):
            if (choice == "1"):
                notification = chooseImageAsDriveIcon()
            elif (choice == "2"):
                notification = chooseImageToConvert()
            else:
                errorCounter = errorCounter + 1
                wrongChoice = True
        else:
            errorCounter = errorCounter + 1
            wrongChoice = True

menu()