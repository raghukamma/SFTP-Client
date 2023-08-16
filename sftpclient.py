''' sftpclient.py
Tazwell B. 7/14/2023
This file contains the client menus before connected to a server
'''

import sftpshell
import getpass
import json
from termcolor import colored

class SFTPClient:
    # Enumerated Menu States
    s_exit     = -1
    s_welcome  = 0
    s_main     = 1
    s_connect  = 2
    s_saved    = 3
    s_sel_user = 4
    s_sel_host = 5

    def __init__(self):
        self.state = 0
        self.is_running = True
        self.shell = sftpshell.SFTPShell()
        self.saved_logins = dict()
        self.selected_host = None
        self.selected_user = None
        with open("saved_cons.json", "a"): # create file if it doesn't exist
            pass
        with open("saved_cons.json") as cons:
            read = cons.read()
            try:
                self.saved_logins = json.loads(read)
            except json.JSONDecodeError as e:
                if len(read) > 1:
                    print("saved connections file may be improperly formatted")
                # log decode error here
                pass

    def save_login(self, host, user, passw):
        if host not in self.saved_logins.keys():
            self.saved_logins[host] = {user: passw}
        else:
            self.saved_logins[host][user] = passw
        with open("saved_cons.json", "w") as cons:
            try:
                cons.write(json.dumps(self.saved_logins))
            except Exception as e:
                print("Something went wrong saving connection")


    def welcome(self):
        print(colored("\nWelcome to Group 2's SFTP Client!", 'green', attrs=['bold', 'blink']))
        print("---------------------------------")
        self.state = self.s_main

    def main(self):
        print("\nWhat would you like to do?:")
        print("(c)onnect to a new server")
        print("(s)aved connections")
        print("(e)xit")
        print("\n ", end='')
        user_input = input().lower()
        if user_input == 'c':
            self.state = self.s_connect
        elif user_input == 's':
            self.state = self.s_sel_host
        elif user_input == 'e':
            self.state = self.s_exit
            print(colored("\nConnection Closed", 'red', attrs=['bold']))

    def connect(self):
        host = input("Enter the name of the host to connect to: ")
        user = input("Enter your username: ")
        passw = getpass.getpass(stream=None)

        user_input = str()
        if host not in self.saved_logins.keys() or user not in self.saved_logins[host].keys():
            while user_input.lower() != 'y' and user_input.lower() != 'n':
                print("Would you like to save this login? y/n: ", end='')
                user_input = input()
            if user_input.lower() == 'y':
                self.save_login(host, user, passw)
            
        self.shell.login(host, user, passw)
        self.shell.start()
        self.state = self.s_main

    def select_host(self):
        selected = False # redundant, I could just use while True, but I don't like that
        while not selected:
            print("Please select a Host:")
            hosts = list(self.saved_logins.keys())
            for k in range(len(hosts)):
                print(k,": ",hosts[k])
            print("\nelect host number or (b)ack: ", end='')
            uin = input()
            print()
            if uin.lower() == 'b':
                self.state = self.s_main
                return
            try:
                uin = int(uin)
            except ValueError as e:
                print(colored(f"Please input a number from 0 to {len(hosts) - 1}\n", "red"))
            else:
                if uin >= 0 and uin < len(hosts):
                    self.selected_host = hosts[uin]
                    self.state = self.s_sel_user
                    selected = True
                    print(colored(f"Host selected: {self.selected_host}\n", "green"))
                    return
                else:
                    print(colored(f"Please input a number from 0 to {len(hosts) - 1}\n", "red"))
    
    def select_user(self):
        selected = False # redundant, I could just use while True, but I don't like that
        while not selected:
            print(f"Please select a User from {self.selected_host}:")
            users = list(self.saved_logins[self.selected_host].keys())
            for k in range(len(users)):
                print(k,": ",users[k])
            print("\nSelect user number or (b)ack: ", end='')
            uin = input()
            print()
            if uin.lower() == 'b':
                self.state = self.s_sel_host
                return
            try:
                uin = int(uin)
            except ValueError as e:
                print(colored(f"Please input a number from 0 to {len(users) - 1}\n", "red"))
            else:
                if uin >= 0 and uin < len(users):
                    self.selected_user = users[uin]
                    self.state = self.s_saved
                    selected = True
                    return
                else:
                    print(colored(f"Please input a number from 0 to {len(users) - 1}\n", "red"))

    def saved(self):
        # ISSUE #18: use saved connection information to connect
        host = self.selected_host
        user = self.selected_user
        passw = self.saved_logins[host][user]
        self.shell.login(host, user, passw)
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
            if self.state == self.s_sel_host:
                self.select_host()
            if self.state == self.s_sel_user:
                self.select_user()
            if self.state == self.s_exit:
                self.exit()

    def start(self):
        # if anything needs to happen before menu_loop
        self.menu_loop()
