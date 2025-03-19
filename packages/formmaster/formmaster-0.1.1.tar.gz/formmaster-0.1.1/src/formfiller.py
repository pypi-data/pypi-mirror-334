from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver import Firefox, FirefoxOptions
from threading import Lock

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

from etl import load
from forms.mod1 import mod1
from forms.mod2 import mod2

import os
import argparse
import subprocess
import socket
import time
import sys

lock = Lock()
is_win = (True if os.name == 'nt' else False)
main_application_handle = None
module = None
driver = None
run_mode = 0

def on_click(x, y, button, pressed):
    global main_application_handle
    global driver
    
    if pressed:
        return
    
    #print('DEBUG >>> ', driver.window_handles, driver.current_window_handle)
    with lock:
        if button.name == 'middle':        
            module.run()
            return
        
        elif button.name == 'left':
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            if driver.window_handles[-1] != driver.current_window_handle:
                print('>>> window switching done')
                driver.switch_to.window(driver.window_handles[-1])
            return
        else:
            return



def run(dir = ('C:\\work\\data\\13. 懿心ONE Bonnie' if is_win else '/home/hmei/data/13. 懿心ONE Bonnie'), uni = 'usyd', mode = 0):

    global main_application_handle
    global module
    global driver
    global run_mode

    run_mode = mode

    if is_win:
        server_address = ('127.0.0.1', 9222)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(server_address)
        except:    
            print(' start the browser ... ')
            chromes = [
                f"{os.environ[basedir]}\Google\Chrome\Application\chrome.exe" 
                for basedir in ['ProgramFiles', 'ProgramFiles(x86)', 'LocalAppData'] 
                if basedir in os.environ] + ['/opt/google/chrome/chrome'
            ]
            for chrome in chromes:
                if os.path.isfile(chrome):
                    profiledir = f"{os.environ['LocalAppData']}\selenium\ChromeProfile" if is_win else f"{os.environ['HOME']}/selenium/ChromeProfile"
                    cmd = [chrome, '--remote-debugging-port=9222', f'--user-data-dir={profiledir}']
                    print('use browser: ', cmd)
                    subprocess.Popen(cmd)
                    break
        finally:
            sock.close()
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
        try:
            # First try to use an existing Chrome instance via the remote debugging port
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Failed to connect to existing Chrome instance: {e}")
            try:
                # If that fails, try to use webdriver_manager to get ChromeDriver
                print("Trying to install ChromeDriver using webdriver_manager...")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e2:
                # If that fails too, check for locally installed driver in common locations
                print(f"Failed to install ChromeDriver automatically: {e2}")
                # Check installation directory and drivers folder
                local_driver_paths = [
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'drivers', 'chromedriver', 'chromedriver.exe'),
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drivers', 'chromedriver.exe'),
                    "C:\\drivers\\chromedriver.exe"
                ]
                
                for path in local_driver_paths:
                    if os.path.exists(path):
                        print(f"Using local ChromeDriver at {path}")
                        service = Service(executable_path=path)
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                        break
                else:
                    # If all else fails, raise a clear error
                    raise RuntimeError("Could not find or install ChromeDriver. Please install it manually and ensure it is in your PATH.")
    else:
        options = FirefoxOptions()
        options.set_preference("network.protocol-handler.external-default", False)
        options.set_preference("network.protocol-handler.expose-all", True)
        options.set_preference("network.protocol-handler.warn-external-default", False)
        driver = Firefox(options=options)

    students = []
    if not run_mode:
        students = load(dir)
        #print(students)

    if uni == 'usyd':
        module = mod1(driver, students, run_mode)
    elif uni == 'unsw':
        module = mod2(driver, students, run_mode)
    else:
        print('uni not yet supported, exit.')
        return

    main_application_handle = module.login_session()
    try:
        mouse_listener = MouseListener(on_click=on_click)
        mouse_listener.start()

        # do this idle loop
        while True:
            time.sleep(10)
    except:
        print('failing exit')
    finally:
        mouse_listener.stop()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Form-Master - Automate form filling for university applications.')
    
    parser.add_argument('--dir', type=str, 
                      default='C:\\work\\data\\13. 懿心ONE Bonnie' if is_win else '/home/hmei/data/13. 懿心ONE Bonnie',
                      help='Directory containing student data')
    
    parser.add_argument('--uni', type=str, choices=['usyd', 'unsw'], default='usyd',
                      help='Target university (usyd or unsw)')
    
    parser.add_argument('--mode', type=int, default=0,
                      help='Operation mode (0 for normal operation)')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    run(dir=args.dir, uni=args.uni, mode=args.mode)
