''' sftpshellfuncs.py
Tazwell B. 7/14/2023
this file should contain functions that the shell executes through the command decoder. 
'''

import os
import warnings
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
    print("this is an exmple command")
    return
    
# functions go here:

# below function lists all directories and files in the pwd on the server
# it supports simple "ls" or "ls -l" to show file attributes
def list_content(sftp, args):
    if sftp == None:
        print("\nWarning: SFTP client is not connected")
        return
    
    path = '.' # set the default path to pwd
    show_attributes = False

    if len(args) > 1 and args[1] == '-l':
        show_attributes = True

    if len(args) > 1 and args[1] != '-l':
        print("Error: Invalid argument. Currently ls command only supports -l argument. Please enter 'ls -l' to show file attributes")
        return

    try:
        directory = sftp.listdir_attr(path)
        for entry in directory:
            if show_attributes:
                attributes = entry.longname.split()
                print(' '.join(attributes))
            else:
                print(entry.filename)
    except Exception as e:
        print(f"Error listing directory or files: {str(e)}")


# prints all commands
def help(sftp, args=None):
    # this does not print the command names aligned, only as a list separated 
    # by two spaces
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

#Varsha
#downloads file from remote server 
def get_file_remote_server(sftp, args=None):
    print("Enter the filname with the extension of the file from the current directory")
    filename = input()
    if sftp.isfile(filename):
        print(f"Downloading file:{filename} from current directory")
        if getfile(sftp, filename):
            print(f"{filename} downloaded successfully")
        else:
            print("Downloading failed. \nRetrying to download the file again....")
            if getfile(filename):
                print("Downloaded successfully")
            else:
                print("Download failed again.\n Please try again after some time")
    else:
        print(f"Filename you entered does not exist.\n Please try again")


def getfile(sftp, filename):    
    try:
        sftp.get(filename, preserve_mtime=True)
    except IOError as e:
        return False
    
    if os.path.exists('./'+filename):
        return True
    else:
        return False

# to register a new command with the Command Decoder copy the form below:
commands["command_name"] = command_function_name
# copy to here:
commands["help"] = help
commands["ls"] = list_content
commands["getFile"] = get_file_remote_server


del commands["command_name"] # deletes example from command list
