''' sftpshell.py
Tazwell B. 7/14/2023
This file contains the Main Shell Loop, Command Decoder, and the Login and Exit functions
'''

import pysftp
import loggerclass
import sftpshellfuncs
from tabulate import tabulate
from termcolor import colored

class SFTPShell:
    # SFTPShell Constructor
    def __init__(self, command_dict=sftpshellfuncs.commands):
        if type(command_dict) is not dict:
            raise ValueError("SFTPShell must be initialized with a dictionary of commands")
        
        self.command_dict = command_dict
        self.is_running = True
        self.sftp = None # variable for the sftp connection

    # SFTPShell Destructor
    def __del__(self):
        if self.sftp != None:
            self.sftp.close()
            print(colored("\nConnection Closed", 'red', attrs=['bold']))

    # Can't be defined in sftpshellfuncs.py
    def exit(self, sftp, args):
        log = loggerclass.getLogger('exit')
        self.is_running = False
        if self.sftp != None:
            self.sftp.close()
            self.sftp = None
            print(colored("\nSuccessfully Logged out!", 'green', attrs=['bold']))
            log.info("Successfully Logged out!")

    # MUST BE CALLED BEFORE start()
    def login(self, host, user, passw):
        log = loggerclass.getLogger('login')
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        try:
            self.sftp = pysftp.Connection(host, user, password=passw, cnopts=cnopts)
        except Exception as e:
            print("Error: could not connect to server")
            log.error("Error: could not connect to server")
        else:
            self.sftp.timeout = 10
        

    # decodes the user command
    def decode_command(self, user_input):
        log = loggerclass.getLogger('decode_command')
        command = str.split(user_input, ' ')

        if type(command) != list:
            return
        if len(command) < 1:
            return
        for arg in command:
            if type(arg) != str:
                return
        
        c = command[0].lower()
        if c not in self.command_dict.keys():
            print("Command not recognized")
            log.warn("Command not recognized. Command entered is: "+c)
            return
        self.command_dict[c](self.sftp, command)

    # gets user input and passes it to decoder
    def main_loop(self):
        while self.is_running:
            print("> ", end='')
            user_input = input()
            self.decode_command(user_input)

    # starts the SFTP shell, call after loging in
    def start(self):
        log = loggerclass.getLogger('start')
        self.is_running = True
        if self.sftp == None:
            print("\nWarning: SFTP client is not connected")

        self.command_dict["logoff"] = self.exit
        print("---------------------------------")
        print(colored("\nLogin Successful!\n", 'green', attrs=['bold', 'blink']))
        log.info("Login Successful!")
        print("---------------------------------")
        print("\nType 'help' to view a full list of commands\n")
        # List of commands in a tabular format
        print(tabulate([['ls', 'list directories and files on remote server'], ['get_file', 'get file from remote server'],
                        ['chmod', 'change permissions on remote server'], ['closeconn','close connection'],
                        ['logoff','logout from remote server'],['rm','delete file from remote server'],
                        ['mget','get multiple'],['mkdir','create directory on remote server'],
                        ['lsl','list of directories and files on local machine'],['cd','change directory on remote server'],
                        ['rename','rename file on remote server'],['renamel','rename file on local machine'],
                        ['copydir','copy directories on remote server'],['cdl','change directory on local machine'],
                        ['rmd','delete directory on remote server'], ['put','put file/files onto remote server']], 
                       headers=['Command', 'Description']))
        self.main_loop()
            

    

