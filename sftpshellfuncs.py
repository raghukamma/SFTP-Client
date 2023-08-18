''' sftpshellfuncs.py
Tazwell B. 7/14/2023
this file should contain functions that the shell executes through the command decoder. 
'''

import os
import warnings
import loggerclass
warnings.filterwarnings('ignore','.*Failed to load HostKeys.*')


commands = dict()

# uncomment for ide auto completion reasons
# from pysftp import Connection as t_sftp

# shell functions should take 2 args. The first is the initialized SFTP connection
# and the second is the list of args the user typed, like argv in C. Example:
#       sftp = pysftp.Connection()
# user input = "get foo bar.txt foobar.json"
#       args = ["get", "foo", "bar.txt", "foobar.json"]
def command_function_name(sftp, args):
    if sftp == None:
        return
    print("this is an example command")
    return
    
# functions go here:

# below function lists all directories and files in the pwd on the server
# it supports simple "ls" or "ls -l" to show file attributes
def list_content(sftp, args):
    log = loggerclass.getLogger('list_content')
    if sftp == None:
        print("\nWarning: SFTP client is not connected")
        log.warn("\nWarning: SFTP client is not connected ")
        return
    
    path = '.' # set the default path to pwd
    show_attributes = False

    if len(args) > 1 and args[1] == '-l':
        show_attributes = True

    if len(args) > 1 and args[1] != '-l':
        print("Error: Invalid argument. Currently ls command only supports -l argument. Please enter 'ls -l' to show file attributes")
        log.error("Error: Invalid argument. Currently ls command only supports -l argument. Please enter 'ls -l' to show file attributes")
        return

    try:
        directory = sftp.listdir_attr(path)
        for entry in directory:
            if show_attributes:
                attributes = entry.longname.split()
                print(' '.join(attributes))
                log.info(' '.join(attributes))
            else:
                print(entry.filename)
                log.info(entry.filename)
    except Exception as e:
        print(f"Error listing directory or files: {str(e)}")
        log.error(f"Error listing directory or files: {str(e)}")

#below function creates directory on remote server using mkdir command
def make_directory(sftp, args):
    log = loggerclass.getLogger('make_directory')
    if sftp == None:
        print("\nWarning: SFTP client is not connected")
        log.warn("\nWarning: SFTP client is not connected")
        return
    
    #show error message if no argument is passed
    if len(args) < 2:
        print("Error: Invalid argument. Please enter the directory name to be created. For example: mkdir new_directory")
        log.error("Error: Invalid argument. Please enter the directory name to be created. For example: mkdir new_directory")
        return
    
    #show error message if more than one argument is passed
    if len(args) > 2:
        print("Error: Invalid argument. Please enter only one argument. For example: mkdir new_directory")
        log.error("Error: Invalid argument. Please enter only one argument. For example: mkdir new_directory")
        return
    
    directory_name = args[1] #get the directory name from the argument
    try:
        #check if the directory already exists
        if sftp.isdir(directory_name):
            print(f"Error: There is an existing directory with the name '{directory_name}' Please use another name for creating a new directory")
            log.error(f"Error: There is an existing directory with the name '{directory_name}' Please use another name for creating a new directory")
            return
        else:
            sftp.mkdir(directory_name)
            print(f"Directory {directory_name} created successfully")
            log.info(f"Directory {directory_name} created successfully")
    except Exception as e:
        print(f"Error creating directory: {str(e)}")
        log.error(f"Error creating directory: {str(e)}")

# below function allows users to change permissions on a file or directory on remote server
def change_permission(sftp, args):
    log = loggerclass.getLogger('change_permission')
    if sftp == None:
        print("\nWarning: SFTP client is not connected")
        log.error("\nWarning: SFTP client is not connected")
        return
    
    if len(args) < 3:     #show error message if no argument is passed
        print("Error: Invalid argument. Please enter the file or directory name and the permission to be set. For example: chmod 777 filename, chmod 741 directoryname")
        log.error("Error: Invalid argument. Please enter the file or directory name and the permission to be set. For example: chmod 777 filename, chmod 741 directoryname")
        return
    
    if len(args) > 3:   #show error message if more than two arguments are passed
        print("Error: Invalid argument. Please enter only two arguments.  For example: chmod 777 filename, chmod 741 directoryname")
        log.error("Error: Invalid argument. Please enter only two arguments.  For example: chmod 777 filename, chmod 741 directoryname")
        return
    
    remotepath = args[2]    #get the file or directory name from the argument
    newmode = args[1]   #get the permission to be set from the argument
    try:
        if sftp.exists(remotepath): #check if the file or directory exists
            sftp.chmod(remotepath, mode=newmode)
            print(f"Permission changed successfully for '{remotepath}'")
            log.info(f"Permission changed successfully for '{remotepath}'")
        else:
            print(f"Error: There is no file or directory with the name '{remotepath}' Please use correct name")
            log.error(f"Error: There is no file or directory with the name '{remotepath}' Please use correct name")
            return
    except Exception as e:
        print(f"Error changing permission: {str(e)}")
        log.error(f"Error changing permission: {str(e)}")

# Saiteja G 7/19/2023
# Function to close SFTP connection
def logout(sftp):
    log = loggerclass.getLogger('logout')

    try:
        if sftp:
            sftp.close()
            sftp = None
            print("SFTP connection closed successfully.")
            log.info("SFTP connection closed successfully.")
    except Exception as e:
        print(f"Error closing SFTP connection: {e}")
        log.error(f"Error closing SFTP connection: {e}")
        

# Saiteja G 7/19/2023
# Function to handle logout command
# command to be used is "logout"
def tologOut(sftp, args):
    log = loggerclass.getLogger('tologOut')
    print("Are you sure to close the connection? (yes/no)")
    log.info("Are you sure to close the connection? (yes/no)")
    value = input().strip().lower()
    try:
        if value == "yes":
            log.info("User entered yes. Closing the connection..")
            logout(sftp) #connection closes using above logout function.
            exit()
        elif value == "no":
            print("closing the connection not successful as user selected 'No'.")
            log.info("closing the connection not successful as user selected 'No'.")

        else:
            print("Please give input as 'yes' or 'no'.")
            log.info("Please give input as 'yes' or 'no'.")
            tologOut(sftp, args)
    except Exception as e:
        print(f"Error closing SFTP connection: {e}")
        log.error(f"Error closing SFTP connection: {e}")

    
# prints all commands
def help(sftp, args=None):
    # this does not print the command names aligned, only as a list separated 
    # by two spaces
    log = loggerclass.getLogger('help')
    termw = os.get_terminal_size().columns
    currw = 0
    key_list = list(commands.keys())
    for key in key_list:
        if len(key) > termw:
            print(key, end=' ')
        else:
            if currw + len(key) + 2 > termw:
                print()
                currw = 0
            print(key, end='  ')
            currw = currw + len(key) + 2
    print('\n')
    log.info("Printed the options on console..")

# Tazwell
# puts file from local cwd to remote server
def put_file(sftp, args=None):
    log = loggerclass.getLogger('put_file')
    if sftp is None:
        print("\nWarning: SFTP client is not connected")
        log.warn("Warning: SFTP client is not connected")
        return
    if args is None or len(args) < 2:
        print("put requires at least one file to put")
        log.warn("put requires at least one file to put")
        return
    for i in range(1,len(args)):
        if os.path.isfile(os.getcwd()+'/'+args[i]):
            try:
                sftp.put(os.getcwd()+'/'+args[i])
                print(f"Uploaded file: {args[i]}")
                log.info(f"Uploaded file: {args[i]}")
            except IOError as e:
                print(f"File: {os.getcwd()+'/'+args[i]} failed to upload")
                log.error(f"File: {os.getcwd()+'/'+args[i]} failed to upload")
    return

#Varsha
#downloads file from remote server 
def get_file_remote_server(sftp, args=None):
    log = loggerclass.getLogger('get_file_remote_server')
    print("Enter the filname with the extension of the file from the current directory")
    filename = input()
    log.info("Enter the filname with the extension of the file from the current directory: "+filename)
    if sftp.isfile(filename):
        print(f"Downloading file:{filename} from current directory")
        log.info(f"Downloading file:{filename} from current directory")
        if getfile(sftp, filename):
            print(f"{filename} downloaded successfully")
            log.info(f"{filename} downloaded successfully")
        else:
            print("Downloading failed. \nRetrying to download the file again....")
            log.error("Downloading failed. \nRetrying to download the file again....")
            if getfile(filename):
                print("Downloaded successfully")
                log.info("Downloaded successfully")
            else:
                print("Download failed again.\n Please try again after some time")
                log.error("Download failed again.\n Please try again after some time")
    else:
        print(f"Filename you entered does not exist.\n Please try again")
        log.error(f"Filename you entered does not exist.\n Please try again")


def getfile(sftp, filename):  
    try:
        sftp.get(filename, preserve_mtime=True)
    except IOError as e:
        return False
    
    if os.path.exists('./'+filename):
        return True
    else:
        return False
    
    
# Saiteja G 7/24/2023
# Function to be used to download multiple files   
def getMultiple(sftp, args):
    log = loggerclass.getLogger('getMultiple')
    if sftp == None:
        print("\nWarning: SFTP client is not connected")
        log.warn("\nWarning: SFTP client is not connected")
        return
   
    print("Enter the file names from current directory with space inbetween. (Ex: test.txt test2.txt)")
    files = input()   # User Input
    multiple = files.split() # Multiple check
    log.info("Enter the file names from current directory with space inbetween. (Ex: test.txt test2.txt): "+files)
    for i in multiple:
        if sftp.isfile(i) and sftp.exists(i):
            print(f"Selected file:{i}")
            log.info(f"Selected file:{i}")
            if getfile(sftp,i):
                print("Downloading....\n Successfully Downloaded.")
                log.info("Downloading....\n Successfully Downloaded.")
            else:
                print("Download failed. Please try again!")
                log.info("Download failed. Please try again!")
        else:
            print(f"Filename you entered does not exist.\n Please try again!") 

            log.error(f"Filename you entered does not exist.\n Please try again!")
            
#Varsha
#Changing directory on the local machine
def change_directory_local(sftp, args):
    log = loggerclass.getLogger('change_directory_local')
    curDir = os.getcwd()
    print("Your current working directory is : "+os.getcwd())
    log.info("Your current working directory is : "+os.getcwd())
    print("Enter the name of directory or path to change the current working directory on local machine: ")
    userPath = input()
    log.info("Enter the name of directory or path to change the current working directory on local machine: " +userPath)
    try:
        os.chdir(userPath)
        if(os.getcwd() == curDir+"\\"+userPath or os.getcwd() == userPath or userPath == '..'):
            print("Your current working directory changed successfully")
            log.info("Your current working directory changed successfully")
            print("Your current working directory is : "+os.getcwd())
            log.info("Your current working directory is : "+os.getcwd())
        else:
            print("Error while changing the directory.\n Please try again!")
            log.error("Error while changing the directory.\n Please try again!")
    except Exception as e:
        print("Error while changing the directory.\n Please try again!")
        log.error("Error while changing the directory.\n Please try again!")
    


# Saiteja G 7/30/2023
# Function to copy directory on remote server
def copyDir(sftp, args):
    log = loggerclass.getLogger('copyDir')
    print('Enter the directory name that needs to be copied:')
    dirname = input() # Directory that needs to be copied
    log.info('Enter the directory name that needs to be copied: '+dirname)
    if sftp.isdir(dirname):
        print("Enter the destination(Directory name):")
        log.info("Enter the destination(Directory name):")
        dirdestination = input() # Destination of the directory that being copied to
        try:
            command = f'cp -r {dirname} {dirdestination}' # command for the copy
            result = sftp.execute(command) # Command execution
            if not result:
                print(f"Copying {dirname} to {dirdestination}.")
                log.info(f"Copying {dirname} to {dirdestination}.")
            else:
                print("Error copying the directory")
                log.error("Error copying the directory")
        except Exception as e: # Error handling
            print("Error performing this action.\n Please try again!")
            log.error("Error performing this action.\n Please try again!")

    else:
        print("This directory doesnot exist!")
        log.error("This directory doesnot exist!")
        

def list_files_folder_local(sftp, args=None):
    path = "."
    log = loggerclass.getLogger('list_files_folder_local')
    try:
        print("Displaying the files and folders from current directory present in the local machine: ")
        log.info("Displaying the files and folders from current directory present in the local machine: ")
        entries = os.listdir(path)
        entries.sort(key=os.path.getctime)
        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                print(entry)
                log.info(entry)
            else:
                print(entry)
                log.info(entry)

    except OSError as e:
        print(f"Error: {e}")
        log.error(f"Error: {e}")

def chDirRem(sftp, args):
    log = loggerclass.getLogger('chDirRem')
    if(len(args) > 2):
        print("Please only enter one directory at a time. ex: cd remoteDirectory")
        log.info("Please only enter one directory at a time. ex: cd remoteDirectory")
        return
    if(len(args) < 2):
        print("Please enter the directory to change into. ex: cd remoteDirectory")
        log.info("Please enter the directory to change into. ex: cd remoteDirectory")
        return
    if(sftp.exists(args[1])):
        sftp.chdir(args[1])
        print("-> " + sftp.pwd)
    else:
        print("That directory does not exist")
        log.info("That directory does not exist")
        
#Layla
def renameRemote(sftp, args):
    log = loggerclass.getLogger('renameRemote')
    if len(args) != 3:
        print("How to use the rename command: rename src.txt dest.txt")
        log.info("How to use the rename command: rename src.txt dest.txt")
        return
    src = args[1]
    if sftp.exists(src):
        dest = args[2]
        try:
            sftp.rename(src, dest)
        except IOError:
            print("Oops, you entered an invalid destination file name")
            log.error("Oops, you entered an invalid destination file name")
            return
        else:
            print(src + " successfully renamed " + dest)
            log.info(src + " successfully renamed " + dest)
            return
    else:
        print("The source file you entered does not exist.")
        log.warn("The source file you entered does not exist.")
        
#Varsha
def rename_file_on_local(sftp, args=None):
     log = loggerclass.getLogger('rename_file_on_local')
     print("Enter the name of the file along with it's extension to be renamed on the local machine")
     filerenamel= input()
     log.info("Enter the name of the file along with it's extension to be renamed on the local machine: "+filerenamel)
     if os.path.isfile(filerenamel) and os.path.exists(filerenamel):
        print("Enter the new name along with it's extension for the file")
        log.info("Enter the new name along with it's extension for the file")
        newnamel = input()
        if os.path.isfile(newnamel) and os.path.exists(newnamel):
            print("the name you entered already exists")
            log.error("the name you entered already exists")
        else:
            os.rename(filerenamel, newnamel)
            if os.path.isfile(newnamel) and os.path.exists(newnamel):
                print("The file has been renamed successfully")
                log.info("The file has been renamed successfully")
            else:
                print("The file could not be renamed. Please try again")
                log.error("The file could not be renamed. Please try again")
     else:
        print("The file you wish to rename does not exist. Please enter a valid filename")
        log.error("The file you wish to rename does not exist. Please enter a valid filename")

#Layla
def delFileRemote(sftp, args):

    log = loggerclass.getLogger('delFileRemote')
    #print("Please enter the name of the file you wish to delete")

    for x in args:
        if x != "rm":
            remotefile = x
            try:
                sftp.remove(remotefile)
            except IOError:
                print("Deletion unsuccessful: " + x + " does not exist")
                log.error("Deletion unsuccessful: " + x + " does not exist")
            except: 
                print("Deletion unsuccessful")
                log.error("Deletion unsuccessful")
            else:
                print( x + " deleted successfully!")
                log.info(x + " deleted successfully!")


# Saiteja G 8/8/2023
# Function to delete directory on remote server
def deleteDir(sftp, args):
    log = loggerclass.getLogger('deleteDir')
    for x in args:
        if x != "rmd":
            remotedir = x
            if sftp.exists(remotedir):
                try:
                    
                    sftp.execute(f"rm -r {remotedir}")
                    print(f"Performing Deletion of this directory: {remotedir}")
                    log.info(f"Performing Deletion of this directory: {remotedir}")
                except:
                    print("Error while performing this action. Deletion unsuccessful")
                    log.error("Error while performing this action. Deletion unsuccessful")
                else:
                    print("Deletion Successful")
                    log.info("Deletion Successful")
            else:
                print(f"Deletion unsuccessful: {x} does not exist!")
                log.error(f"Deletion unsuccessful: {x} does not exist!")
                
# to register a new command with the Command Decoder copy the form below:
commands["command_name"] = command_function_name
# copy to here:
commands["help"] = help
commands["ls"] = list_content
commands["get_file"] = get_file_remote_server
commands["chmod"] = change_permission
commands["closeconn"] = tologOut
commands["rm"] = delFileRemote
commands["mget"] = getMultiple
commands["mkdir"] = make_directory
commands["lsl"] = list_files_folder_local
commands["cd"] = chDirRem
commands["rename"] = renameRemote
commands["renamel"] = rename_file_on_local
commands["copydir"] = copyDir
commands["cdl"] = change_directory_local
commands["rmd"] = deleteDir
commands["put"] = put_file
del commands["command_name"] # deletes example from command list
