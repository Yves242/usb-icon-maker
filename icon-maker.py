from lib2to3.pytree import convert
import os
from PIL import Image
from colorama import init
from termcolor import colored

# Simple function that cleans screen. Returns nothing
def cleanScreen():
    os.system("cls")

# Simple function that hides autorun.inf and autorun.ico
def hideFiles():
    os.system('cmd /c "IF EXIST autorun.inf (attrib +h +r +a +s autorun.inf) & IF EXIST autorun.ico (attrib +h +r +a +s autorun.ico) & exit"')

# Simple function that unhides autorun.inf and autorun.ico
def unhideFiles():
    os.system('cmd /c "IF EXIST autorun.ico (attrib -h -r -a -s autorun.inf) & IF EXIST autorun.ico (attrib -h -r -a -s autorun.ico) & exit"')

# General function that finds files with specific extension. Returns string array
def findExtensionFiles(extension):

    # variable
    extensionFiles = []

    # start file search
    for path in os.scandir(os.getcwd()):
        if (path.is_file()):
            str = path.name.lower()
            if (str[len(str)-4:len(str)] == extension):
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

# Simple function that makes the 'autorun.inf' file. Returns Boolean, String as notification
def convertImageToIcon(imgFile):

    # this will be the new icon name
    icoFilename = imgFile

    # if not .ico file, convert to ico file.    
    if (imgFile[len(imgFile)-4:len(imgFile)].lower() != ".ico"):
        file = Image.open(imgFile)

        # save image as proper filename
        if (imgFile[-4] == "."): # if of format .jpg, .png, or .gif
            icoFilename = imgFile[0:len(imgFile)-4] + ".ico"        
        else: # else if of format .jpeg
            icoFilename = imgFile[0:len(imgFile)-5] + ".ico"

        # save using proper image filename
        file.save(icoFilename)

        return True, "Successfully converted '" + imgFile + "' to '" + icoFilename + "'."

# Simple function that makes the 'autorun.inf' based on a given image (converted to 'autorun.ico' file 
# from within this function). Returns Boolean, String as notification
def makeAutorunFile(imgFile):

    # unhide autorun.inf and autorun.ico
    unhideFiles()
    
    # Boolean error switch
    isError = False

    # if 'autorun.inf' already exists, ask user what to do.
    if fileExists("autorun.inf"):
        decision = ""
        while (decision not in ("y", "Y")):
            
            print("User selected image file '" + colored((imgFile), "green") + "'.\n")
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

    # if 'autorun.inf' does not exist, or user decided to overwrite, convert and save image as autorun.ico
    file = Image.open(imgFile)
    file.save("autorun.ico")
    
    # create new file 
    with open('autorun.inf', 'w') as f:
        f.write('[AutoRun.Amd64]\nicon="autorun.ico"\n\n[AutoRun]\nicon="autorun.ico"')
    
    # hide 'autorun.inf' and 'autorun.ico' and exit function
    hideFiles()
    return True, "Successfully added image as label."

# Function that lets user choose icons based on image files. Returns Boolean, String as notification text
def chooseImagesAsIcons():
    
    # clean screen
    cleanScreen()

    # get usable image files list
    pngFiles = findExtensionFiles(".png")
    jpgFiles = findExtensionFiles(".jpg")
    jpegFiles = findExtensionFiles(".jpeg")
    gifFiles = findExtensionFiles(".gif")
    icoFiles = findExtensionFiles(".ico")
    imgFiles = pngFiles + jpgFiles + jpegFiles + gifFiles + icoFiles

    # sort for organization
    if (len(imgFiles) > 1):
        imgFiles = sorted(imgFiles)    

    if (len(imgFiles) == 0):      

        return False, "(see below)\nWe found out that there are no image files in the current folder.\nImage files have extensions .png, .jpg, .jpeg, .gif, and .ico\n\nPlace images inside the folder where this program is located. \n('" + os.getcwd() + "')."

    elif (len(imgFiles) > 0):     
        
        # initialize for main while loop
        success = False
        indexBoundError = False
        errorCount = 0

        # Do until successful or user chose exit
        while (not success):
            
            # initialize for inner while loop
            intFailed = False
            choice = "" 

            # do while choice is not an integer
            while (not choice.isnumeric()):
                cleanScreen()
                
                print("The program found these icon files in the current folder/directory:\n")
                
                # index for each element in icon array
                index = 0

                # pass through each icon file found in array
                for img in imgFiles:
                    print("[" + str(index+1) +"] " + img)
                    index = index + 1
                print("")

                if (intFailed):
                    errorCount = errorCount + 1
                    print(colored("Input error #" + str(errorCount) + ": Please only use numbers.", "red"))
                    # reset failure boolean switches
                    intFailed = False   
                    indexBoundError = False

                if (indexBoundError): 
                    errorCount = errorCount + 1                   
                    print(colored("Input error #" + str(errorCount) + ": Please only use numbers shown above, ranging from 1 to " + str(len(imgFiles)) + ".", "red"))
                    # reset failure boolean switches
                    intFailed = False   
                    indexBoundError = False                

                # ask user what file to use
                choice = input("What file would you like to use? (To exit, type 'exit') \nChoice number: ")
                
                # if user placed exit, stop function and program.
                if (choice.upper() == "EXIT"):
                    return False, "User decided to exit option 1."

                # int validity check
                if (choice.isnumeric()):
                    intFailed = False
                else:
                    intFailed = True

            # At this point, the user has a valid integer choice input      
            if ((int(choice) > 0) and (int(choice) <= len(imgFiles))):
                cleanScreen()

                # make autorun.inf file using icon file of choice            
                return makeAutorunFile(imgFiles[int(choice)-1])

            else:

                # index bound error
                indexBoundError = True

    else:
        return False, "Unexpected program error occurred while searching for files."

# Function that lets user choose icons based on image files. Returns Boolean, String as notification text
def chooseImageToConvert():
    
    # clean screen
    cleanScreen()

    # get usable image files list
    pngFiles = findExtensionFiles(".png")
    jpgFiles = findExtensionFiles(".jpg")
    jpegFiles = findExtensionFiles(".jpeg")
    gifFiles = findExtensionFiles(".gif")
    imgFiles = pngFiles + jpgFiles + jpegFiles + gifFiles

    # sort for organization
    if (len(imgFiles) > 1):
        imgFiles = sorted(imgFiles)    

    if (len(imgFiles) == 0):      

        return False, "(see below)\nThere are no image files in the main directory where this program is located.\nImage files have extensions .png, .jpg, .jpeg, .gif, and .ico\n\nPlace images inside the folder where this program is located. \n('" + os.getcwd() + "')."

    elif (len(imgFiles) > 0):     
        
        # initialize for main while loop
        success = False
        indexBoundError = False
        errorCount = 0

        # Do until successful or user chose exit
        while (not success):
            
            # initialize for inner while loop
            intFailed = False
            choice = "" 

            # do while choice is not an integer
            while (not choice.isnumeric()):
                cleanScreen()
                
                print("The program found these image files in the current folder/directory:\n")
                
                # index for each element in icon array
                index = 0

                # pass through each icon file found in array
                for img in imgFiles:
                    print("[" + str(index+1) +"] " + img)
                    index = index + 1
                print("")

                if (intFailed):
                    errorCount = errorCount + 1
                    print(colored("Input error #" + str(errorCount) + ": Please only use numbers.", "red"))
                    # reset failure boolean switches
                    intFailed = False   
                    indexBoundError = False

                if (indexBoundError): 
                    errorCount = errorCount + 1                   
                    print(colored("Input error #" + str(errorCount) + ": Please only use numbers shown above, ranging from 1 to " + str(len(imgFiles)) + ".", "red"))
                    # reset failure boolean switches
                    intFailed = False   
                    indexBoundError = False                

                # ask user what file to use
                choice = input("What file would you like to use? (To exit, type 'exit') \nChoice number: ")
                
                # if user placed exit, stop function and program.
                if (choice.upper() == "EXIT"):
                    return False, "User decided to exit option 1."

                # int validity check
                if (choice.isnumeric()):
                    intFailed = False
                else:
                    intFailed = True

            # At this point, the user has a valid integer choice input      
            if ((int(choice) > 0) and (int(choice) <= len(imgFiles))):
                cleanScreen()
                print("User selected image file '" + colored(imgFiles[int(choice)-1], "green") + "'.\n")

                # convert image to .ico file           
                return convertImageToIcon(imgFiles[int(choice)-1])

            else:

                # index bound error
                indexBoundError = True

    else:
        return False, "Unexpected program error occurred while searching for files."

# This is where everything starts. Returns nothing
def menu():
    
    # initialize for colors
    init()
    
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

        print(colored("USB Icon Maker ", "cyan") + colored("(", "magenta") + colored("v 3.0.0", "yellow") + colored(")\n", "magenta"))
        print("What would you like to do?\n")
        print("[1] Use images as icon for your USB Drive")
        print("[2] Convert images to .ico file (optional)")
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
                notification = chooseImagesAsIcons()
            elif (choice == "2"):
                notification = chooseImageToConvert()
            else:
                errorCounter = errorCounter + 1
                wrongChoice = True
        else:
            errorCounter = errorCounter + 1
            wrongChoice = True

menu()
