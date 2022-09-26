from lib2to3.pytree import convert
import os
from PIL import Image

# Simple function that cleans screen. Returns nothing
def cleanScreen():
    os.system("cls")

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

# Simple function that makes the 'autorun.inf' file. Returns Boolean
def makeAutorunFile(imgFile):
    
    # if 'autorun.inf' already exists, ask user what to do.
    if fileExists("autorun.inf"):
        decision = ""
        while (decision not in ("y", "Y")):    
            decision = input("'autorun.inf' file already exists. \nYou may have already placed an icon on this device before.\n\nOverwrite to add new icon to this device? [y/n]\n")        
            cleanScreen()
            if (decision in ("n", "N")):
                print("Aborting process. User decided not to overwrite 'autorun.inf'.\n")
                return False
            elif (decision not in ("y", "Y")):
                print("Please type either 'y' or 'n' only.\n")

    # if 'autorun.inf' does not exist, or user decided to overwrite, start here.
    icoFilename = imgFile

    # if not ico file, convert to ico file.    
    if (imgFile[len(imgFile)-4:len(imgFile)].lower() != ".ico"):
        file = Image.open(imgFile)

        # save image as proper filename
        if (imgFile[-4] == "."): # if of format .jpg, .png, or .gif
            icoFilename = imgFile[0:len(imgFile)-4] + ".ico"        
        else: # else if of format .jpeg
            icoFilename = imgFile[0:len(imgFile)-5] + ".ico"

        # save using proper image filename
        file.save(icoFilename)

    # create new file 
    with open('autorun.inf', 'w') as f:
        f.write('[AutoRun.Amd64]\nicon="' + icoFilename + '"\n\n[AutoRun]\nicon="' + icoFilename + '"')
            
    print("Successfully generated new autorun.inf file.\n")
    return True

# Function that lets user choose icons based on image files. Returns Boolean
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

    if (len(imgFiles) == 0):

        print("We found out that there are no image files in the current folder.")
        print("Image files have extensions .png, .jpg, .jpeg, .gif, and .ico\n")
        print("Place images inside the folder where this program is located. ('" + os.getcwd() + "').")

        return False

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

                if (intFailed):
                    errorCount = errorCount + 1
                    print("\nInput error #" + str(errorCount) + ": Please only use numbers.")
                    # reset failure boolean switches
                    intFailed = False   
                    indexBoundError = False

                if (indexBoundError): 
                    errorCount = errorCount + 1                   
                    print("\nInput error #" + str(errorCount) + ": Please only use numbers shown above, ranging from 1 to " + str(len(iconFiles)) + ".")
                    # reset failure boolean switches
                    intFailed = False   
                    indexBoundError = False                

                # ask user what file to use
                choice = input("\nWhat file would you like to use? (To exit, type 'exit') \nChoice number: ")
                
                # if user placed exit, stop function and program.
                if (choice.upper() == "EXIT"):
                    print("User decided to exit. Program halted.")
                    return False

                # int validity check
                if (choice.isnumeric()):
                    intFailed = False
                else:
                    intFailed = True

            # At this point, the user has a valid integer choice input      
            if ((int(choice) > 0) and (int(choice) <= len(imgFiles))):
                cleanScreen()
                print("User selected file '" + imgFiles[int(choice)-1] + "'.\n")

                # make autorun.inf file using icon file of choice            
                return makeAutorunFile(imgFiles[int(choice)-1])

            else:

                # index bound error
                indexBoundError = True


    else:
        print("Unexpected error occurred while finding icon files.")
        return False

# This is where everything starts. Returns nothing
def menu():

    wrongChoice = False
    errorCounter = 0

    # Do always until user exits.
    while (True):

        cleanScreen()
        print("What would you like to do?\n")
        print("[1] Use images as icon for your USB Drive")
        print("[0] Exit\n")

        # notification text upon wrong choice
        if (wrongChoice):
            print("Error #" + str(errorCounter) + ": Wrong choice number.\n")
            wrongChoice = False # reset failure switch

        choice = input("Choice number: ")

        if (choice.lower() in ("0", "exit")):
            exit()
        elif (choice.isnumeric()):
            if (choice == "1"):
                chooseImagesAsIcons()
            else:
                errorCounter = errorCounter + 1
                wrongChoice = True
        else:
            errorCounter = errorCounter + 1
            wrongChoice = True

menu()
