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
import logging
from datetime import datetime

lock = Lock()
is_win = (True if os.name == 'nt' else False)
main_application_handle = None
module = None
driver = None
run_mode = 0
logger = None

# Setup logging
def setup_logging():
    global logger
    # Create a timestamp for the log filename
    timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    log_filename = f"formmaster_{timestamp}.log"
    log_filename = os.path.join(os.environ.get('USERPROFILE', ''), '.formmaster', log_filename)

    # Configure logging with encoding specified for file handler
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Create logger for this module
    logger = logging.getLogger('formmaster')
    logger.info(f"Logging setup complete. Log file: {log_filename}")
    return logger

def on_click(x, y, button, pressed):
    global main_application_handle
    global driver
    
    if pressed:
        return
    
    #logger.debug(f'DEBUG >>> {driver.window_handles}, {driver.current_window_handle}')
    with lock:
        if button.name == 'middle':        
            module.run()
            return
        
        elif button.name == 'left':
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            if driver.window_handles[-1] != driver.current_window_handle:
                logger.info('>>> window switching done')
                driver.switch_to.window(driver.window_handles[-1])
            return
        else:
            return

def run(dir = ('C:\\work\\data\\13. 懿心ONE Bonnie' if is_win else '/home/hmei/data/13. 懿心ONE Bonnie'), uni = 'usyd', mode = 0):
    global main_application_handle
    global module
    global driver
    global run_mode
    global logger
    
    # Setup logging
    logger = setup_logging()
    
    run_mode = mode

    if is_win:
        server_address = ('127.0.0.1', 9222)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(server_address)
        except:    
            logger.info('Starting the browser...')
            chromes = [
                f"{os.environ[basedir]}\Google\Chrome\Application\chrome.exe" 
                for basedir in ['ProgramFiles', 'ProgramFiles(x86)', 'LocalAppData'] 
                if basedir in os.environ] + ['/opt/google/chrome/chrome'
            ]
            for chrome in chromes:
                if os.path.isfile(chrome):
                    profiledir = f"{os.environ['LocalAppData']}\selenium\ChromeProfile" if is_win else f"{os.environ['HOME']}/selenium/ChromeProfile"
                    cmd = [chrome, '--remote-debugging-port=9222', f'--user-data-dir={profiledir}']
                    logger.info(f'Using browser: {cmd}')
                    subprocess.Popen(cmd)
                    break
        finally:
            sock.close()
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        path = os.path.join(os.environ.get('USERPROFILE', ''), '.formmaster', 'chromedriver.exe')
        if os.path.exists(path):
            logger.info(f"Using local ChromeDriver at {path}")
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            logger.info("Using ChromeDriverManager")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    else:
        options = FirefoxOptions()
        options.set_preference("network.protocol-handler.external-default", False)
        options.set_preference("network.protocol-handler.expose-all", True)
        options.set_preference("network.protocol-handler.warn-external-default", False)
        driver = Firefox(options=options)

    students = []
    if not run_mode:
        logger.info(f"Loading student data from {dir}")
        students = load(dir)
        logger.info(f"Loaded {len(students)} student records")

    if uni == 'usyd':
        logger.info("Initializing Sydney University module")
        module = mod1(driver, students, run_mode)
    elif uni == 'unsw':
        logger.info("Initializing UNSW module")
        module = mod2(driver, students, run_mode)
    else:
        logger.error(f"University '{uni}' not supported, exiting.")
        return

    main_application_handle = module.login_session()
    try:
        logger.info("Starting mouse listener")
        mouse_listener = MouseListener(on_click=on_click)
        mouse_listener.start()

        # do this idle loop
        logger.info("Running main loop - waiting for events")
        while True:
            time.sleep(10)
    except Exception as e:
        logger.exception("Exception in main loop")
        logger.error(f"Failing exit: {e}")
    finally:
        logger.info("Stopping mouse listener")
        mouse_listener.stop()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='FormMaster - Automate form filling for university applications.')
    
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
