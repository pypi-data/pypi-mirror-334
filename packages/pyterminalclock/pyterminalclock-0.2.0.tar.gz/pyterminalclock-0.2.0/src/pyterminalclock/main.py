"""
        py-terminal-clock   A simple clock display for the terminal
        Author: ffalcon31415
        License: GPLv3

        Copyright (C) 2024  ffalcon31415

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime
import os
import time

import pyfiglet

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print('\033[?25l', end="") # blinking cursor
        time_string = datetime.datetime.now().strftime('%I:%M %p').strip("0")
        time_string = " " + " ".join(time_string) #.replace(" M", "M")
        print("\n" * 10)
        large_time_string = pyfiglet.figlet_format(time_string, font= "STANDARD")
        print(large_time_string)
        time.sleep(10)

if __name__ == "__main__":
    main()