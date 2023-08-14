''' sftpclient.py
Tazwell B. 7/14/2023
This file contains the client menus before connected to a server
'''

import sftpshell
import getpass
from termcolor import colored

class SFTPClient:
    # Enumerated Menu States
    s_exit    = -1
    s_welcome = 0
    s_main    = 1
    s_connect = 2
    s_saved   = 3

    def __init__(self):
        self.state = 0
        self.is_running = True
        self.shell = sftpshell.SFTPShell()

    def welcome(self):
        print(colored("\nWelcome to Group 2's SFTP Client!", 'green', attrs=['bold', 'blink']))
        print("---------------------------------")
        self.state = self.s_main

    def main(self):
        print("\nWhat would you like to do?:")
        print("(c)onnect to a new server")
        print("(s)ave a new connection")
        print("(e)xit")
        print("\n ", end='')
        user_input = input().lower()
        if user_input == 'c':
            self.state = self.s_connect
        elif user_input == 's':
            self.state = self.s_saved
        elif user_input == 'e':
            self.state = self.s_exit
            print(colored("\nConnection Closed", 'red', attrs=['bold']))

    def connect(self):
        host = input("Enter the name of the host to connect to: ")
        user = input("Enter your username: ")
        passw = getpass.getpass(stream=None)

        # ISSUE #17: check if saved, ask if want to save etc...

        self.shell.login(host, user, passw)
        self.shell.start()
        self.state = self.s_main

    def saved(self):
        # ISSUE #18: use saved connection information to connect

        # self.shell.login(host, user, passw)
        self.shell.start()
        self.state = self.s_main

    def exit(self):
        self.is_running = False

    def menu_loop(self):
        while self.is_running:
            if self.state == self.s_welcome:
                self.welcome()
            if self.state == self.s_main:
                self.main()
            if self.state == self.s_connect:
                self.connect()
            if self.state == self.s_saved:
                self.saved()
            if self.state == self.s_exit:
                self.exit()

    def start(self):
        # if anything needs to happen before menu_loop
        self.menu_loop()
