from function import *
from setting import *
import keyboard
import time

if __name__ == '__main__':
    print(Fore.RED + (FONT.renderText('F.R I')))
    print('-------------------------------')

    while True:
        if keyboard.is_pressed('windows') and keyboard.is_pressed('shift'):
            main()

            time.sleep(0.1)