import os
from turtle import clearscreen

# Simple function that cleans screen. Returns nothing
def cleanScreen():
    os.system("cls")

# Function that finds icon file. Returns string array
def findIconFiles():

    # variable
    iconFiles = []
    
    # start file search
    for path in os.scandir(os.getcwd()):
        if (path.is_file()):
            str = path.name.upper()
            if (str[len(str)-4:len(str)] == ".ICO"):
                iconFiles.append(path.name)
    
    if (len(iconFiles) > 1):
        iconFiles = sorted(iconFiles)

    return iconFiles

# General function that finds any file. Returns Boolean True or False
def fileExists(filename):

    # start file search
    for path in os.scandir(os.getcwd()):
        if (path.is_file() and path.name == filename):
            return True
    
    return False

# Simple function that makes the 'autorun.inf' file. Returns Boolean True or False
def makeAutorunFile(iconFile):
    
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

    # if 'autorun.inf' does not exist, or user decided to overwrite
    with open('autorun.inf', 'w') as f:
        f.write('[AutoRun.Amd64]\nicon="' + iconFile + '"\n\n[AutoRun]\nicon="' + iconFile + '"')
            
    print("Successfully generated new autorun.inf file.\n")
    return True

# Start of all processes
def start():
    
    # clean screen, get icons list
    cleanScreen()
    iconFiles = findIconFiles()

    if (len(iconFiles) == 0):

        print("We found out that there is still no icon files in your USB.")
        return False

    elif (len(iconFiles) > 0):     
        
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
                for icon in iconFiles:
                    print("[" + str(index+1) +"] " + icon)
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
                if (choice.upper == "EXIT"):
                    print("User decided to exit. Program halted.")
                    return False

                # int validity check
                if (choice.isnumeric()):
                    intFailed = False
                else:
                    intFailed = True

            # At this point, the user has a valid integer choice input      
            if ((int(choice) > 0) and (int(choice) <= len(iconFiles))):
                cleanScreen()
                print("User selected file '" + iconFiles[int(choice)-1] + "'.\n")

                # make autorun.inf file using icon file of choice            
                return makeAutorunFile(iconFiles[int(choice)-1])

            else:

                # index bound error
                indexBoundError = True


    else:
        print("Unexpected error occurred while finding icon files.")
        return False

start()