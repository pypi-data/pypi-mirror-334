'''
<div class="sv-form-horizontal">
	<div class="sv-form-group">
		<label class="sv-col-md-3 sv-control-label">Have you been awarded a scholarship or sponsorship to support your studies? *</label>
		<div class="sv-col-md-4">
			<div class="sv-radio"><label><input name="IPQ_APONSH13" id="IPQ_APONSH13A" type="radio" value="Y" onclick="check_IPQ_APONSH13();">&nbsp;Yes</label></div>
			<div class="sv-radio"><label><input name="IPQ_APONSH13" id="IPQ_APONSH13B" type="radio" value="N" onclick="check_IPQ_APONSH13();">&nbsp;No</label></div>
		</div>
	</div>
	<div class="sv-form-group" id="section8" style="display: none;">
		<label for="IPQ_APONSH14" class="sv-col-md-3 sv-control-label">What is the name of the scholarship or sponsor? *</label>
		<div class="sv-col-md-4">
			<input name="IPQ_APONSH14" id="IPQ_APONSH14" class="sv-form-control" type="text" maxlength="100" value="">
		</div>
	</div>
	<div class="sv-form-group">
		<label class="sv-col-md-3 sv-control-label">Have you applied for a scholarship (for which your application is pending)? *</label>
		<div class="sv-col-md-4">
			<div class="sv-radio"><label><input name="IPQ_APONSH15" id="IPQ_APONSH15A" type="radio" value="Y" onclick="check_IPQ_APONSH15();">&nbsp;Yes</label></div>
			<div class="sv-radio"><label><input name="IPQ_APONSH15" id="IPQ_APONSH15B" type="radio" value="N" onclick="check_IPQ_APONSH15();" data-gtm-form-interact-field-id="0">&nbsp;No</label></div>
		</div>
	</div>
	<div class="sv-form-group" id="section9" style="display: none;">
		<label for="IPQ_APONSH16" class="sv-col-md-3 sv-control-label">What is the name of the scholarship? *</label>
		<div class="sv-col-md-4">
			<input name="IPQ_APONSH16" id="IPQ_APONSH16" class="sv-form-control" type="text" maxlength="100" value="">
		</div>
	</div>
</div>
'''


import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scholarships:
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data

    def run(self):
        students = self.data
        driver = self.driver
        personal_info = students[-1][0]
        
        # Check if the student has been awarded a scholarship or sponsorship
        has_scholarship = personal_info.get('has_scholarship', False)
        
        if has_scholarship:
            # Select "Yes" for scholarship awarded
            self.check_button_by_id("IPQ_APONSH13A")
            
            # Wait for the scholarship name field to appear
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "section8"))
            )
            
            # Fill in scholarship name if available
            scholarship_name = personal_info.get('scholarship_name', '')
            if not scholarship_name:
                scholarship_name = "Study Abroad Scholarship"  # Default placeholder
                
            self.set_value_by_id("IPQ_APONSH14", scholarship_name)
        else:
            # Select "No" for scholarship awarded
            self.check_button_by_id("IPQ_APONSH13B")
        
        # Check if the student has applied for a pending scholarship
        has_pending_scholarship = personal_info.get('has_pending_scholarship', False)
        
        if has_pending_scholarship:
            # Select "Yes" for pending scholarship
            self.check_button_by_id("IPQ_APONSH15A")
            
            # Wait for the pending scholarship name field to appear
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "section9"))
            )
            
            # Fill in pending scholarship name if available
            pending_scholarship_name = personal_info.get('pending_scholarship_name', '')
            if not pending_scholarship_name:
                pending_scholarship_name = "International Student Merit Scholarship"  # Default
                
            self.set_value_by_id("IPQ_APONSH16", pending_scholarship_name)
        else:
            # Select "No" for pending scholarship
            self.check_button_by_id("IPQ_APONSH15B")
        
        # Country of birth (required)
        birth_country = personal_info.get('birth_country', '')
        if not birth_country:
            # Default to the regular country if birth country isn't specified
            birth_country = personal_info.get('Country', 'China (Excludes SARS and Taiwan)')
        self.select_option_by_id("IPQ_APONCOB", birth_country)
        
        # Citizenship/residency status (required)
        residency_status = personal_info.get('residency_status', '')
        if not residency_status:
            # Default to student visa for international applications
            residency_status = 'Student visa or other temporary visa'
        self.select_option_by_id("IPQ_APONLNID", residency_status)
        
        # Wait for conditional fields based on residency status selection
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "country-of-citizenship"))
        )
        
        # Handle fields that may appear conditionally
        # First arrival date (if visible)
        if self.is_element_visible("date-of-arrival-in-australia"):
            arrival_date = personal_info.get('australia_arrival_date', '01/01/2020')
            self.set_value_by_id("IPQ_APONEND", arrival_date)
        
        # Country of citizenship (if visible)
        if self.is_element_visible("country-of-citizenship"):
            citizenship = personal_info.get('citizenship_country', '')
            if not citizenship:
                citizenship = personal_info.get('Country', 'China (Excludes SARS and Taiwan)')
            self.select_option_by_id("IPQ_APONCOD", citizenship)
        
        # Visa type (if visible)
        if self.is_element_visible("visa-type"):
            visa_type = personal_info.get('visa_type', 'Student')
            self.select_option_by_id("dummy_visa_type", visa_type)
            
            # Visa start date (if visible)
            if self.is_element_visible("visa-start-date"):
                visa_start = personal_info.get('visa_start_date', '01/01/2020')
                self.set_value_by_id("IPQ_APONVSD", visa_start)
        
        # Aboriginal/Torres Strait Islander origin (required)
        indigenous_status = personal_info.get('indigenous_status', 'Neither Australian Aboriginal nor Torres Strait Islander')
        self.select_option_by_id("IPQ_APONETH1", indigenous_status)
        
        # Language spoken at home (required)
        home_language = personal_info.get('home_language', '')
        if not home_language:
            # Try to infer from country
            country = personal_info.get('Country', '').lower()
            if 'china' in country:
                home_language = 'Mandarin'
            elif 'korea' in country:
                home_language = 'Korean'
            elif 'japan' in country:
                home_language = 'Japanese'
            elif 'india' in country:
                home_language = 'Hindi'
            else:
                home_language = 'English'
        self.select_option_by_id("IPQ_APONSSL", home_language)
    
    def set_value_by_id(self, element_id, value):
        """Set value to an input field by ID"""
        element = self.driver.find_element(By.ID, element_id)
        element.clear()
        element.send_keys(value)
    
    def select_option_by_id(self, element_id, option_text):
        """Select an option from a dropdown by ID"""
        # For chosen-enhanced dropdowns, need to click and then select
        dropdown = self.driver.find_element(By.ID, f"{element_id}_chosen")
        dropdown.click()
        
        # Find and click the option with matching text
        options = self.driver.find_elements(By.CSS_SELECTOR, f"#{element_id}_chosen .chosen-results li")
        for option in options:
            if option_text.lower() in option.text.lower():
                option.click()
                break
    
    def is_element_visible(self, element_id):
        """Check if an element is visible on the page"""
        try:
            element = self.driver.find_element(By.ID, element_id)
            return element.is_displayed()
        except:
            return False
