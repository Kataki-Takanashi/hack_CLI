# import os
# os.system('clear')
# print('Last login: Tue Sep 12 23:42:44 on ttys000')
# USER = 'ali@Mohammeds-iMac'
#
# COMMANDS = ['ls', 'cd', '', '', '',
#             '', '', '', '', '',
#             '', '', '', '', '',
#             '', '', '', '', '',
#             '', '', '', '', '']
#
# current_directory = '~'
# directories = {'/':
#                    {'usr': {'~': {'Desktop': {'note.txt': 'INSERT NOTE HERE!!!'},
#                                   "Documents": None,
#                                   "Mail": None
#                                   }
#                             }
#                     },
#                }
#
# class InputHandler():
#     def __init__(self, imput: str):
#         self.input = imput.split()
#         if self.input[0] == 'ls':
#             self.ls()
#
#         def ls(self):
#             dir = self.find_dir(current_directory)
#             return dir.keys()
#
#         def find_dir(self, directory): #TODO make this non dependent on directories so it changes between computers
#             try:
#                 cd = directories['/']
#                 while True:
#                     if cd.__str__() == directory:
#
# # Main Loop --------------------------------
# while True:
#     cmd = input(f"{USER} {current_directory} % ") #TESTING

import os
import random
import string
import time
import re
# import readline

from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.filters import IsDone
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

from dataclasses import dataclass, fields, field



os.system('clear')
print('Last login: Tue Sep 12 23:42:44 on ttys000')


# Variables
allow_ping = True
allow_hydra = False

show_popup = True

command_list = [i for i in ['ls', 'cd', 'cat', 'ssh', 'ping' if allow_ping else '', 'hydra' if allow_hydra else '', 'popup', 'help', 'exit'] if i != '']


# Constants
USER = f"{os.getlogin()}@{os.uname().nodename.split('.')[0]}"

@dataclass
class Computer:
    name: str = field(compare=False)
    directories: dict = field(compare=False)
    ip: str = field(compare=True)
    password: str = field(default=None, compare=False)

@dataclass
class File:
    name: str
    content: str


class InputHandler:
    def __init__(self, input_str):
        global current_computer  # Declare current_computer as global
        self.input = input_str.split()
        self.command = self.input[0]
        self.current_directory = current_directory

        if self.command == 'ls' or self.command == 'l':
            self.ls()
        elif self.command == 'cd' or self.command == 'c':
            self.cd()
        elif self.command == 'cat' or self.command == 'ca':
            self.cat()
        elif self.command == 'help' or self.command == 'h':
            self.help()
        elif self.command == 'ssh' or self.command == 's':
            self.ssh()
        elif self.command == 'ping' or self.command == 'p':
            self.ping()
        elif self.command == 'hydra' or self.command == 'hy':
            self.hydra()
        elif self.command == 'popup':
            self.popup()
        elif self.command == 'exit':
            print("""
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.
Deleting expired sessions...none found.

[Process completed]"""); exit()
        else:
            print(f"Command not found: {self.command}")

    def ls(self):
        current_dir = find_dir(current_computer, self.current_directory)
        if current_dir is not None and isinstance(current_dir, dict):
            show_hidden = len(self.input) > 1 and self.input[-1] == '-a'
            if self.input[-1] != '-a' and self.input[-1] != 'ls' and self.input[-1] != 'l':
                print("\nls    (l)  - List files and directories")
                print("Usage: ls <options>")
                print("\nOptions:")
                print("-a         - List hidden files and directories")
                return
            for item in current_dir.keys():
                if not item.startswith('.') or show_hidden:
                    print(item)
        else:
            print("Directory not found.")

    def cd(self):
        if len(self.input) > 1:
            new_dir = self.input[-1]
            temp_dir = self.current_directory.copy()
            temp_dir.append(new_dir)
            current_computer_dirs = find_dir(current_computer, temp_dir)
            # print(f"Current Directory: {self.current_directory}")  # Add this line
            if new_dir == ".":
                return
            elif new_dir == "..":
                if len(self.current_directory) > 1:
                    self.current_directory.pop()  # Go up one directory
            elif new_dir == "...":
                for _ in range(len(self.current_directory) - 1):
                    self.current_directory.pop()
                # self.current_directory = [self.current_directory[0]]
            elif current_computer_dirs and len([s for s in new_dir.split('.') if s != '']) == 1:
                self.current_directory.append(new_dir)  # Updat the current_directory
            elif current_computer_dirs == {}:
                self.current_directory.append(new_dir)
            else:
                print("Directory not found.")
        else:
            print("Usage: cd <directory>")

    def cat(self):
        if len(self.input) > 1:
            file_name = self.input[-1]
            current_dir = find_dir(current_computer, self.current_directory)
            if file_name in current_dir or (self.input[
                                                1] == '-a' and f".{file_name}" in current_dir):  # the second statement dose nothing, fix it
                try:
                    print(current_dir.get(file_name, current_dir.get(f".{file_name}", None)).content)
                except AttributeError:
                    print("Not a File.")
            else:
                print("File not found.")
        else:
            print("Usage: cat <file>")

    def popup(self):
        if len(self.input) > 1:
            global update, show_popup
            if self.input[-1] == 'Enable':
                show_popup = True
                update = True

            elif self.input[-1] == 'Disable':
                show_popup = False
                update = True

            else:
                print(f"Error: {self.input[-1]} is not an option, try: Enable | Disable")

        else:
            print("Usage: popup Enable | Disable")

    def help(self):
        if self.input[-1].startswith('h') and len(self.input) == 1:
            print("\nAvailable commands:")
            print("ls    (l)  - List files and directories")
            print("cd    (c)  - Change directory")
            print("cat   (ca) - View file contents")
            print("ssh   (s)  - Secure Shell into a Computer")
            print("ping  (p)  - Checks an ip or range") if allow_ping else None
            print("hydra (hy) - Cracks the password of a computer") if allow_hydra else None
            print("help  (h)  - Display this help message")
            print("help  cmd  - For help with a cmd")
            print("popup      - Enable/Disable autocomplete popup")
            print("exit - Exit the terminal")

        elif self.input[-1] in ('ls', 'l'):
            print("\nls    (l)  - List files and directories")
            print("Usage: ls <options>")
            print("\nOptions:")
            print("-a         - List hidden files and directories")

        elif self.input[-1] in ('cd', 'c'):
            print("\ncd    (c)  - Change directory")
            print("Usage: cd <directory>")
            print("\nOptions:")
            print("..         - Go back to the previous directory")
            print("...        - Go back to the root directory")

        elif self.input[-1] in ('cat', 'ca'):
            print("\ncat   (ca) - View file contents")
            print("Usage: cat <file>")

        elif self.input[-1] in ('ssh', 's'):
            print("\nssh   (s)  - Secure Shell into a Computer")
            print("Usage: ssh <computer>")

        elif self.input[-1] in ('ping', 'p'):
            if allow_ping:
                print("\nping   (p)  - Checks an ip or range")
                print("Usage: ping x.x.x.x")
                print("Usage: ping -r x.x.x (0-255) (0-255)")
                print("Tip: in ping range use only the first part of an ip like 192.198.4 not 192.168.4.24")
            else:
                print("This command is not available.")

        elif self.input[-1] in ('hydra', 'hy'):
            if allow_hydra:
                print("\nhydra (hy) - Cracks the password of a computer")
                print("Usage: hydra <computer>")
            else:
                print("This command is not available.")

        elif self.input[-1] in ('help', 'h'):
            print("\nhelp  (h)  - Display a help message")
            print("Usage: help")

        elif self.input[-1] in ('cmd'):
            print("\nhelp cmd   - For help with a cmd")
            print("Usage: help <cmd>")

        elif self.input[-1] in ('popup'):
            print("\npopup      - Enable/Disable autocomplete popup")
            print("Usage: popup Enable | Disable")

        elif self.input[-1] in ('exit'):
            print("\nexit - Exit the terminal")
            print("Usage: exit")

        else:
            print(f"Help: Command not found: {self.command}")
            print("Usage: help <cmd>")

    def ssh(self):
        if len(self.input) > 1:

            target_computer_ip = self.input[-1]
            target_computer = None
            for computer in computers.values():
                if computer.ip == target_computer_ip:
                    target_computer = computer
                    break

            if target_computer:

                tries = 3
                locked = True
                while locked and tries != 0 and target_computer.password is not None:
                    passwd = prompt(f"{target_computer_ip}'s password: ", is_password=True)
                    if passwd == target_computer.password:
                        locked = False
                    else:
                        print("Permission denied", ", please try again." if tries > 1 else '') # FIXME_DONE it says "Permission denied, please try again" after the last try it shouldent
                        tries -= 1
                if tries == 0:
                    return

                global current_computer
                current_computer = target_computer
                global update
                update = True
                self.current_directory = [
                    list(current_computer.directories.keys())[0]]  # Reset directory to 'usr' on the new computer
            else:
                print("Computer not found.")
        else:
            print("Usage: ssh <computer>")

    def ping(self):
        if allow_ping:
            if len(self.input) == 2:
                for computer in computers.values():
                    if computer.ip == self.input[1]:
                        print("\n     IP         PASS")
                        print(f"{self.input[1]}    {computer.password is not None}")

            elif len(self.input) > 1 and self.input[1] == '-r':
                IP = self.input[2]
                MIN = self.input[3] if len(self.input) < 3 else 0
                MAX = self.input[4] if len(self.input) < 3 else 255
                valid_ips = []

                for i in range(int(MIN), int(MAX) + 1):
                    for computer in computers.values():
                        if computer.ip == f'{IP}.{i}':
                            valid_ips.append(computer)
                            break
                if len(valid_ips) > 0:

                    print("\n     IP         PASS")
                    for i in valid_ips:
                        print(f"{i.ip}    {i.password is not None}")

                else:
                    print("No ip's in range.")
            else:
                print("Usage: ping x.x.x.x")
                print("Usage: ping -r x.x.x (0-255) (0-255)")
                print("Tip: in ping range use only the first part of an ip like 192.198.4 not 192.168.4.24")

        else:
            print("This command is not available.")

    def hydra(self):
        if allow_hydra:
            if len(self.input) > 1:
                computer_pass = find_computer(self.input[-1])
                if computer_pass is not None:
                    if computer_pass.password is not None:
                        target = computer_pass.password
                        CHARS = string.ascii_letters + string.digits + string.punctuation + ' '
                        current = [random.choice(CHARS) for _ in target]
                        counter = 0

                        for index, char in enumerate(target):
                            while current[index] != char:
                                current[index] = random.choice(CHARS)
                                counter += 1
                                # print(''.join(current))
                                print(f"Cracked! The password is {''.join(current)} and took {counter} attempts.",
                                      end="\r")
                                time.sleep(.01)

                        print(f"Cracked! The password is {''.join(current)} and took {counter} attempts.")

                    else:
                        print(f"{self.input[-1]} has no password.")

                else:
                    print("Computer not found.")
            else:
                print("Usage: hydra <computer>")
        else:
            print("This command is not available.")


# def find_dir(computer, directory):
#     try:
#         current_dir = computer.directories
#         for dir_name in directory:
#             if dir_name in current_dir and isinstance(current_dir[dir_name], dict):
#                 current_dir = current_dir[dir_name]
#             else:
#                 return None
#         return current_dir
#     except KeyError:
#         return None

def find_dir(start_dir, target_directory):
    def search(current_path, current_dir, remaining_path):
        if not remaining_path:
            # If there are no more subdirectories in the target path, return the content of the current directory
            return current_dir

        first_item, rest = remaining_path[0], remaining_path[1:]

        if first_item in current_dir:
            if isinstance(current_dir[first_item], dict):
                # Continue searching in the nested directory
                return search(current_path + [first_item], current_dir[first_item], rest)
            else:
                # If the current item is not a directory, return None
                return None
        else:
            # If the current item is not found, return None
            return None

    return search([], start_dir.directories, target_directory)


def find_computer(ip):
    for computer in computers.values():
        if computer.ip == ip:
            return computer




# Create a custom completer.
class CustomCompleter(Completer):
    def get_completions(self, document, complete_event) -> list:
        current_text = document.text_before_cursor
        # if current_text == '': return
        current_dirs = find_dir(current_computer, current_directory)

        # Filter the command_list based on the current text.
        suggestions = [cmd for cmd in command_list if cmd.startswith(current_text)]  # Redundant

        # ls
        if current_text.startswith(cmd := 'ls ') or current_text.startswith(cmd := 'l '):
            suggestions = [cmd + '-a']

        # cd
        if current_text.startswith(cmd := 'cd ') or current_text.startswith(cmd := 'c '):
            suggestions = [cmd + i for i in current_dirs if
                           not i.startswith('.') and len([s for s in i.split('.') if s != '']) == 1]

        # cd .
        if current_text.startswith(cmd := 'cd .') or current_text.startswith(cmd := 'c .'):
            suggestions = [cmd.split('.')[0] + i for i in current_dirs if
                           i.startswith('.') and len([s for s in i.split('.') if s != '']) == 1]

        # cat
        if current_text.startswith(cmd := 'cat ') or current_text.startswith(cmd := 'ca '):
            suggestions = [cmd + i for i in current_dirs if
                           not i.startswith('.') and len([s for s in i.split('.') if s != '']) > 1]

        # cat .
        if current_text.startswith(cmd := 'cat .') or current_text.startswith(cmd := 'ca .'):
            suggestions = [cmd.split('.')[0] + i for i in current_dirs if
                           i.startswith('.') and len([s for s in i.split('.') if s != '']) > 1]

        # ssh

        # ping -
        if current_text.startswith(cmd := 'ping -') or current_text.startswith(cmd := 'p -'):
            suggestions = [cmd + 'r']
        # ping -r
        if re.match(r'ping\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s', current_text) or re.match(r'p\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s', current_text):
            suggestions = [current_text + '0']
        if re.match(r'ping\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\s', current_text) or re.match(r'p\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\s', current_text):
            suggestions = [current_text + '255']

        # hydra


        # help
        if current_text.startswith(cmd := 'help ') or current_text.startswith(cmd := 'h '):
            suggestions = [cmd + i for i in command_list]

        # popup
        if current_text.startswith(cmd := 'popup '):
            suggestions = [cmd + i for i in ['Enable', 'Disable']]

        # exit



        suggestions = [i for i in suggestions if i.startswith(current_text)]

        for suggestion in suggestions:
            yield Completion(suggestion, -len(current_text))


class CustomAutoSuggest(AutoSuggest):
    def get_suggestion(self, buffer, document):
        current_text = document.text_before_cursor
        suggestion = ''
        # ls
        if current_text in ('ls ', 'l '):
            suggestion = 'options'

        # cd
        if current_text in ('cd ', 'c '):
            suggestion = 'directory'
        if current_text in ('cd .', 'c .'):
            suggestion = 'secret directory'

        # cat
        if current_text in ('cat ', 'ca '):
            suggestion = 'file name'
        if current_text in ('cat .', 'ca .'):
            suggestion = 'secret file name'

        # ssh
        if current_text in ('ssh ', 's '):
            suggestion = 'ip'
# TODO suggest discovered ip's Mabye
        # ping
        if current_text in ('ping ', 'p '):
            suggestion = 'ip or options'
        if current_text in ('ping -r ', 'p -r '):
            suggestion = 'x.x.x MIN MAX'
        if re.match(r'ping\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s', current_text) or  re.match(r'p\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s', current_text):
            suggestion = 'MIN MAX'
        if re.match(r'ping\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\s', current_text) or re.match(r'p\s-r\s\d{1,3}\.\d{1,3}\.\d{1,3}\s\d{1,3}\s', current_text): # dont_FIXME change {1,3}  to [0-255]
            suggestion = 'MAX'

        # hydra
        if allow_hydra and current_text in ('hydra ', 'h '):
            suggestion = 'ip'

        # popup
        if current_text == 'popup ':
            suggestion = 'Enable or Disable'
        if current_text == 'popup E':
            suggestion = 'nable'  # todo make it so that all suggestions work this way automaticly
        if current_text == 'popup D':
            suggestion = 'isable'

        # help
        if current_text == 'help ':
            suggestion = 'cmd'

        # exit

        return Suggestion(suggestion)


# Init history and session and keybindings, this is for
history = InMemoryHistory()
session = PromptSession(history=history, completer=CustomCompleter(), auto_suggest=CustomAutoSuggest(), complete_while_typing=show_popup)  # complete_while_typing=False to not show popup
# kb = KeyBindings()
#
#
# @kb.add('c-c', filter=IsDone())
# def exit_(event):
#     event.app.exit()
#
# @kb.add('c-c', filter=~IsDone())
# def cancel_password(event):
#     # Clear the input buffer to simulate no visible password.
#     event.app.current_buffer.text = ''
#
# # Attach key bindings to the session.
# session.app.key_bindings = kb

# def complete(text, state):
#     options = ['ls', 'cd', 'cat', 'ssh', 'ping', 'hydra', 'help', 'exit']
#
#     if state == 0:
#         orig_line = readline.get_line_buffer()
#         begin = readline.get_begidx()
#         end = readline.get_endidx()
#         text = orig_line[begin:end]
#         before_text = orig_line[0:begin]
#         matches = [cmd for cmd in options if cmd.startswith(text)]
#         if len(matches) == 1:
#             return matches[0] + ' ' if matches[0] + ' ' != text else None
#     return None


# Enable tab completion
# readline.parse_and_bind('tab: complete')
# readline.set_completer(complete)

# Initialize

README = """Made BY Ali AbdurRaheem aka Kataki Takanashi
Inspired by Unix and hack RUN
Thx for playing!

"""

NOTE_TO_SELF = """Note to future self when i get around to doing this:
OMG i just looked through a .gov website and its directories are unprotected.
Anyway, there is a JS file that monitors forums and sends info to this ip: 76.107.8.87
The craziest part is. . . Well you'll see, just ping 76.107.8.87
"""

Alien_DB = """Alien Conspiracists Database
|-----------------------------------|
|id| name  | age | criminal history |
|-----------------------------------|
|0 | Allen | 37  |       YES        |
|1 | Allex | 52  |       YES        |
|2 | Brian | 19  |       NO         |
|3 | Cathy | 16  |       YES        |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|-----------------------------------|
"""

METH_DB = """Methamphetamine Database
|-----------------------------------|
|id| name  | age | criminal history |
|-----------------------------------|
|0 | Lilac |  9  |       NO         |
|1 | Tawny | 13  |       YES        |
|2 | Kacie | 17  |       NO         |
|3 | Keana | 16  |       No         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|-----------------------------------|
"""

Fentenol_DB = """Fentenol Database
|-----------------------------------|
|id| name  | age | criminal history |
|-----------------------------------|
|0 | Bella | 39  |       YES        |
|1 | Ciera | 34  |       NO         |
|2 | Delta | 30  |       NO         |
|3 | Clara | 60  |       YES        |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|-----------------------------------|
"""

Murder_DB = """Murder Database
|-----------------------------------|
|id| name  | age | criminal history |
|-----------------------------------|
|0 | Akiko | 46  |       YES        |
|1 | Daiyu | 16  |       NO         |
|2 | Brock | 19  |       YES        |
|3 | Caiou |  7  |       YES        |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|-----------------------------------|
"""

InsiderTrading_DB = """Insider Trading Database
|-----------------------------------|
|id| name  | age | criminal history |
|-----------------------------------|
|0 | Trump | 77  |       YES        |
|1 | Biden | 80  |       NO         |
|2 | Obama | 62  |       NO         |
|3 |  JFK  | 46  |       NO         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|. |   .   |  .  |        .         |
|-----------------------------------|
"""

LOGS_DB = """Database Logs
|---------------------------------------------|
|id|  DB   |     to ip    | pass (to send db) |
|---------------------------------------------|
|0 | Alien | 91.50.59.244 |     BoredAlien    |
|1 | Alien | 91.50.59.244 |     BoredAlien    |
|. |   .   |       .      |         .         |
|. |   .   |       .      |         .         |
|. |   .   |       .      |         .         |
|---------------------------------------------|
"""

Theorists_Report = """Subject: Report on Alien Conspiracy Theorists and Public Awareness

To: Admin@5.226.148.60
From: BoredAlien@91.50.59.244

Dear Admin@5.226.148.60,

I am writing to provide an overview and analysis of the phenomenon known as "Alien Conspiracy Theorists" and the public's 
awareness of extraterrestrial life. This report addresses concerns related to the public's growing awareness of extraterrestrial life,
particularly in light of recent developments in the field of space exploration.

Key Findings

Public Awareness: Despite efforts to maintain secrecy, there are indications that public awareness of extraterrestrial life is on the rise.
This awareness is partially attributed to the growing volume of information available on the internet and an increasing 
number of credible witnesses coming forward with their accounts.
Influence of Alien Conspiracy Theorists: Alien Conspiracy Theorists, while often dismissed as fringe groups, 
have played a role in bringing the topic of extraterrestrial life into public discourse. 
Their persistent claims have contributed to a growing curiosity among the general public.

Confirmation Bias: Many individuals who encounter information related to extraterrestrial life exhibit confirmation bias, 
selectively interpreting or seeking out information that supports their beliefs while ignoring contradictory evidence.

Media and Entertainment: Popular media and entertainment industries have capitalized on the fascination with aliens. 
The portrayal of extraterrestrial encounters in movies, television, and literature has both shaped and reflected public perceptions.

Impact on National Security

The public's increasing awareness of extraterrestrial life has not posed a direct threat to national security. 
However, the potential for misinformation and misinterpretation of sensitive information remains a concern.

NSA's Role

The NSA's role in this context is to monitor online discussions related to extraterrestrial life, 
not only to gauge public awareness but also to identify potential security risks stemming from misinformation. 
Our primary responsibility remains the safeguarding of national security interests.

Conclusion

In conclusion, public awareness of extraterrestrial life is growing, partially due to the efforts of Alien Conspiracy Theorists 
and the influence of media and entertainment. While this awareness has not presented a direct threat to national security, 
it underscores the importance of transparency and responsible communication regarding this topic. 
The NSA will continue to monitor and assess the situation to ensure the protection of vital national interests.

Should you have any further questions or require additional information, please do not hesitate to contact me.

Sincerely,

BoredAlien
Researcher
BoredAlien@91.50.59.244
"""

Report_Mail_Theorists = """To: Admin@5.226.148.60
From: BoredAlien@91.50.59.244
CC: 116.121.216.151
<Attachment>[Theorists.txt]

P.S. Would you please stop sending me puns about cheese and money, THX. Talkin bout u 116.121.216.151
"""

Bored_Txt = """I am sooooo Bored
its in the name
im bored
i should start a diary about how boring this job is
cant even go home
stupid dorms
"""

Captured_Specimen = """Captured Specimen: Anatomy Update
Day 561
The anatomy is strange, it is lacking certain organs.
Our running theory is that different parts of its body decays at different rates,
So that's why parts are missing.
"""

report_MAIL_Specimen = """To: Admin@5.226.148.60
From: 116.121.216.151
<Attachment>[Captured_Specimen.txt]
"""

WhoAreYou = """I dont know who you are or why you are here.
You are the same as me, were here to find out the truth.
What they have been hiding from all of us.
Aliens are real!

We should meet.
More info in the Admin's computer.
Just to make sure you are the real deal.
I wont tell you his password, just hydra his ip and ssh in.
See you on Dole!
"""

NEWS_TXT = """Big News!
The new colony on Dole is now the main colony and has issued that all Gaool (proun: goal) 
are now using the same ip protocol as earth.
"""

t2023_txt = """Area 51 Expense Report - 2023

Employee: Agent Fox Mulder
Position: Admin
Date: July 23, 2023
Department: X-Files Division, Area 51

Expenses Incurred:

Travel Expenses:

Date: June 15, 2023
Description: Round-trip airfare for an official mission to Roswell, New Mexico.
Amount: $1,500
Date: June 16, 2023
Description: Rental of a black SUV equipped with tinted windows and alien detection gear.
Amount: $750
Accommodation Expenses:

Date: June 15-17, 2023
Description: Two-night stay at the "UFO Enthusiast Inn," known for its extraterrestrial-themed rooms.
Amount: $400
Meals and Entertainment:

Date: June 16, 2023
Description: Dinner with Agent Dana Scully and a friendly alien named Zog. (Zog's ip for double checking: 139.64.168.120 (He's at Dole rn))
Amount: $150
Office Supplies:

Date: July 1, 2023
Description: Purchase of a conspiracy theory board, a set of alien-themed pens, and an "I Want to Believe" poster.
Amount: $75
Miscellaneous Expenses:

Date: July 10, 2023
Description: Reimbursement for mind-reading lessons from a psychic hotline.
Amount: $200
Total Expenses: $3,075

Receipts and Supporting Documents Attached: Maybe

Approval:

Employee Signature: Agent Fox Mulder Date: July 23, 2023
Supervisor Signature: Walter Skinner Date: July 24, 2023
Notes:

All expenses were incurred in pursuit of protecting the truth about extraterrestrial life.
Original receipts and supporting documents are attached for all expenses.
Agent Mulder's mind-reading abilities have not yet been confirmed.
"""  # http://139.64.168.120:8080

fun_txt = """My Favorite Places to Spy on Humans
http://99.243.38.96:8080/multi.html
https://ranchcameras.ranchatcanyonridge.com/ui3.htm?t=live&group=Index
"""

hello_stranger = """Hello Stranger
It seems you are curious enough to have noticed earth isent alone, you are in the network of another planet.

I contacted you because i need help, i need someone as adept as me.

I have a deal for you.

I work for an anonymous planet, its a planet of unknown location and its an enemy of most of the galaxy.

We will pay you to help.

If you are interested go to this IP: 98.166.209.128
"""  # http://98.166.209.128:8080/multi.html

view1 = """                .                                            .
     *   .                  .              .        .   *          .
  .         .                     .       .           .      .        .
        o                             .                   .
         .              .                  .           .
          0     .
                 .          .                 ,                ,    ,
 .          \          .                         .
      .      \   ,
   .          o     .                 .                   .            .
     .         \                 ,             .                .
               #\##\#      .                              .        .
             #  #O##\###                .                        .
   .        #*#  #\##\###                       .                     ,
        .   ##*#  #\##\##               .                     .
      .      ##*#  #o##\#         .                             ,       .
          .     *#  #\#     .                    .             .          ,
                      \          .                         .
____^/\___^--____/\____O______________/\/\---/\-28.166.209.130---_____________
   /\^   ^  ^    ^                  ^^ ^  '\ ^          ^       ---
         --           -            --  -      -         ---  __       ^
   --  __                      ___--  ^  ^                         --  __"""

view2 = """
           .          +        /--------------------\
  +                     _ _ _ | STOP THIS PLANET!! |
              +        /   .   |  I WANNA GET OFF!  |
  .      OOOOOOOOOOOO/OOO      \--------------------/
     OO..***......./**.....OO         .   +
    OO.....*******/***........OO
  OO......**********...........OO        +      .    .
 OO.........****...*............OO
  O............**.................O      +    .
 O...........*******.............O                +
  O..........*********............O
 OO.........********............OO        .     .
  OO.........*****.............OO    +               +
   OO........***.............OO               +
 +   OO.......**...........OO      .
   .     10.249.176.253 OO                             +
"""

# Note: Do not copy HACK run, use different story, ask ChatGPT, file names should reflect story
# TODO_DONE Implement file system

localhost = Computer('localhost', {
    'usr': {
        'Documents': {
            'NOTE_TO_SELF.txt': File('NOTE_TO_SELF.txt', NOTE_TO_SELF),
            'Docs': {}
        },
        '.README.md': File('README.md', README),
        '.SecretFolder': {
            '.secret.txt': File('.secret.txt', 'Shh this file is a secret and can only be revealed with ls -a')
        }
    }
}, '192.168.4.24')

NSA_DB = Computer('NSA_DB', {
    'Database': {
        'Drugs': {
            'Meth.db': File('Meth.db', METH_DB),
            'Fentenol.db': File('Fentenol.db', Fentenol_DB)
        },
        'Murder': {
            'Murder.db': File('Murder.db', Murder_DB)
        },
        'Conspiracy': {
            'Govt': {
                'InsiderTrading.db': File('InsiderTrading.db', InsiderTrading_DB)
            },
            'Alien.db': File('Alien.db', Alien_DB)
        },
        'Logs.db': File('Logs.db', LOGS_DB)
    }
}, '76.107.8.87')

NSA_BoredAlien = Computer('NSA_Employee', {
    'usr': {
        'Documents': {
            'Theorists.txt': File('Theorists.txt', Theorists_Report),
            '.Bored.txt': File('Bored.txt', Bored_Txt)
        },
        'Mail': {
            'Mail_IN': {},
            'Mail_OUT': {
                'Report.mail': File('Report.mail', Report_Mail_Theorists)
            }
        }
    }
}, '91.50.59.244', password='BoredAlien')

Area_51_Scientist = Computer('Scientist', {
    'usr': {
        'Documents': {
            'Reports': {
                'Captured_Specimen.txt': File('Captured_Specimen.txt', Captured_Specimen),
                'GOHERE': {
                    'GOHERE': {
                        'ISITHERE?': {
                            'NO': {
                                '.No_Really.txt': File('No_Really.txt', "Its not here")
                            }
                        }
                    },
                    'ORHERE': {
                        'WHYHERE?': {
                            'ISITHERE?': {
                                'YES': {
                                    'WhoAreYou.txt': File('WhoAreYou.txt', WhoAreYou)
                                }
                            }
                        },
                        'ORHERE': {
                            'ISITHERE?': {
                                'NO': {
                                    '.Told_you.txt': File('Told_you.txt', "Why do you even try?")
                                }
                            }
                        }
                    }
                }
            }
        },
        'Mail': {
            'Mail_IN': {
                'Report.mail': File('Report.mail', Report_Mail_Theorists)
            },
            'Mail_OUT': {
                'TOP_SECRET_Report.mail': File('TOP_SECRET_Report.mail', report_MAIL_Specimen)
            }
        }
    }
}, '116.121.216.151', password='cheddar')  # http://116.121.216.151:8080/home.html

Area_51_Admin = Computer('Admin', {
    'usr': {
        'Documents': {
            'ExpenseReports': {
                '2023.txt': File('2023.txt', t2023_txt)
            }
        },
        'Mail': {
            'Mail_IN': {
                'News!.mail': File('News!.mail', NEWS_TXT)
            },
            'Mail_OUT': {}
        }
    }
}, '5.226.148.60', password='Admin')  # http://5.226.148.60:8080/multi.html

Zog = Computer('Zog', {
    'usr': {
        '.fun.txt': File('.fun.txt', fun_txt),
        '.Hello_Stranger.txt': File('.Hello_Stranger.txt', hello_stranger)
    }
}, '139.64.168.120', password='DoleIsLit')

Relay_UnKn = Computer('Relay_UnKn', {
    'usr': {
        'first-assignment.txt': File('first-assignment.txt',
                                     'This first one is a test, we dont have the password for the Dole govt computers, we only have a part of the IP address. 158.39.114 Hint: help ping'),
        '.RelayToday.txt': File('.RelayToday.txt',
                                'This is infuriating why is my computer running the Relay today? Atleast its to hire another hacker. The one we have now is insuffrable, she really is gonna get it once the new hacker comes. Maybe we wont need her anymore :)')
    }
}, '98.166.209.128', password='freedomfromoppretion')

DoleGov1 = Computer('DoleGov1', {
    'usr': {
        'Documents': {
            'Untitled.pdf': File('Untitled.pdf', ''),
            'Untitled2.pdf': File('Untitled2.pdf', ''),
            'old_stuff': {
                'Manifesto_copy.pdf': File('Manifesto_copy.pdf',
                                           'Im done with manifestos its too difficult and i have work')
            }
        }
    }
}, '158.39.114.194', password='dh7Gsj027Frl')

DoleGov2 = Computer('DoleGov2', {
    'usr': {
        'Documents': {
            'Report.txt': File('Report.txt', 'Preliminary report on Sector 7G.'),
            'MeetingNotes.txt': File('MeetingNotes.txt', 'Notes from the secret meeting.')
        }
    }
}, '158.39.114.236', password='hd72fBdh37JD7w8')

DoleGov3 = Computer('DoleGov3', {
    'usr': {
        'Documents': {
            'Report.txt': File('Report.txt', 'Preliminary report on Sector 7G.'),
            'MeetingNotes.txt': File('MeetingNotes.txt', 'Notes from the secret meeting.')
        }
    }
}, '158.39.114.49', password='Dgsn&@ud84d0^3ng*')

DoleGov4 = Computer('DoleGov4', {
    'usr': {
        '.congrats.txt': File('.congrats.txt', 'We look forward to working with you.'),
        '.windowView.txt': File('.windowView.txt', view1)
    }
}, '158.39.114.114', password='BDHB37346^#%@hdb9273')

DarkMoon = Computer('DarkMoon', {
    'usr': {
        'window.txt': File('.window.txt', view2)
    }
}, '28.166.209.130', password='CahUt544r3')

END_TEMP = Computer('End', {
    'usr': {
        'end.txt': File('end.txt', 'This is the end of the game so far, it is a "Proof of concept" and i likely wont continue development. Thanks for playing! -Kataki')
    }
}, '10.249.176.253', password='IHopeYouHadFun!EnjoyThisReallyReallyLongPassword!!!')

computers = {
    'localhost': localhost,
    'NSA_DB': NSA_DB,
    'NSA_Employee': NSA_BoredAlien,
    'Scientist': Area_51_Scientist,
    'Admin': Area_51_Admin,
    'Zog': Zog,
    'Relay_UnKn': Relay_UnKn,
    'DoleGov1': DoleGov1,
    'DoleGov2': DoleGov2,
    'DoleGov3': DoleGov3,
    'DoleGov4': DoleGov4,
    'DarkMoon': DarkMoon,
    'END': END_TEMP

}

current_computer = localhost  # Start with the initial computer
current_directory = [list(current_computer.directories.keys())[0]]  # Set the initial directory to 'usr'
global update
update = False


def main():
    # Initialize
    global current_computer, current_directory, allow_ping, allow_hydra, update, command_list, show_popup, session

    # find_true_dir(current_computer.directories, 'Docs')

    # Main Loop --------------------------------
    while True:
        # Update
        session = PromptSession(history=history, completer=CustomCompleter(), auto_suggest=CustomAutoSuggest(),
                                complete_while_typing=show_popup)
        if update:
            # print('Updating', show_popup) # Debug
            current_directory = [list(current_computer.directories.keys())[0]]
            command_list = [i for i in
                            ['ls', 'cd', 'cat', 'ssh', 'ping' if allow_ping else '', 'hydra' if allow_hydra else '', 'popup',
                             'help', 'exit'] if i != '']
            session = PromptSession(history=history, completer=CustomCompleter(), auto_suggest=CustomAutoSuggest(),
                                    complete_while_typing=show_popup)

            update = False

        # if current_computer == 'placeholder':
        #     allow_ping = True

        if current_computer == Area_51_Scientist:
            allow_hydra = True
            command_list = [i for i in
                            ['ls', 'cd', 'cat', 'ssh', 'ping' if allow_ping else '', 'hydra' if allow_hydra else '', 'popup',
                             'help', 'exit'] if i != '']

        # completions = ["ping", "ls", "cd", "cat", None] + list(find_dir(current_computer, current_directory).keys())
        # completerer  = WordCompleter([c for c in completions if c is not None], ignore_case=True)

        try:
            cmd = session.prompt(
                f"{USER} {(current_computer.ip + ':') if current_computer.ip != '192.168.4.24' else ''}{'/'.join(current_directory)} % ")

        except EOFError:
            break

        # print(current_computer.name, current_directory)
        if len(cmd.strip()) == 0: continue
        handler = InputHandler(cmd)  # Pass current_directory as a parameter


if __name__ == '__main__':
    main()
