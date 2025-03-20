from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException

def set_value_by_id(driver, element_id, value):
    """Set value to an input field by ID"""
    try:
        element = driver.find_element(By.ID, element_id)
        element.clear()
        element.send_keys(value)
    except InvalidElementStateException:
        # If element can't be cleared, try using JavaScript
        driver.execute_script(f"document.getElementById('{element_id}').value = '{value}';")
    except Exception as e:
        print(f"Error setting value for element {element_id}: {e}")

def select_option_by_id(driver, element_id, option_text):
    """Select an option from a dropdown by ID"""
    try:
        # For chosen-enhanced dropdowns, need to click and then select
        dropdown = driver.find_element(By.ID, f"{element_id}_chosen")
        dropdown.click()
        
        # Find and click the option with matching text
        options = driver.find_elements(By.CSS_SELECTOR, f"#{element_id}_chosen .chosen-results li")
        for option in options:
            if option_text.lower() in option.text.lower():
                option.click()
                break
    except Exception as e:
        print(f"Error selecting option for element {element_id}: {e}")

def check_button_by_id(driver, element_id):
    """Check a checkbox or radio button by ID"""
    try:
        element = driver.find_element(By.ID, element_id)
        if not element.is_selected():
            element.click()
    except Exception as e:
        print(f"Error checking element {element_id}: {e}")

def select_radio_by_value(driver, name, value):
    """Select a radio button by its name and value attributes"""
    try:
        # Find all radio buttons with the given name
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, f"input[name='{name}'][value='{value}']")
        
        # Click the first matching radio button if found
        if radio_buttons:
            if not radio_buttons[0].is_selected():
                radio_buttons[0].click()
    except Exception as e:
        print(f"Error selecting radio button {name}={value}: {e}")

def is_element_visible(driver, element_id):
    """Check if an element is visible on the page"""
    try:
        element = driver.find_element(By.ID, element_id)
        return element.is_displayed()
    except:
        return False
