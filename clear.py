import os

clear_screen = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')
