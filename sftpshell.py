''' sftpshell.py
Tazwell B. 7/14/2023
This file contains the Main Shell Loop, Command Decoder, and the Login and Exit functions
'''

import pysftp
import sftpshellfuncs

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
            print("\nConnection Closed")

    # Can't be defined in sftpshellfuncs.py
    def exit(self, sftp, args):
        self.is_running = False
        if self.sftp != None:
            self.sftp.close()
            self.sftp = None
            print("\nConnection Closed")

    # MUST BE CALLED BEFORE start()
    def login(self, host, user, passw):
        self.sftp = pysftp.Connection(host, user, password=passw)

    # decodes the user command
    def decode_command(self, user_input):
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
            return
        self.command_dict[c](self.sftp, command)

    # gets user input and passes it to decoder
    def main_loop(self):
        while self.is_running:
            print(">", end='')
            user_input = input()
            self.decode_command(user_input)

    # starts the SFTP shell, call after loging in
    def start(self):
        if self.sftp == None:
            print("\nWarning: SFTP client is not connected")

        self.command_dict["exit"] = self.exit
        print("\nType 'help' to view a full list of commands\n")
        self.main_loop()
            

    

