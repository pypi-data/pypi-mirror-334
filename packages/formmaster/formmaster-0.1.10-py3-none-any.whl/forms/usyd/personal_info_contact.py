'''
<div class="sv-form-container">
						Please provide the applicant's contact details below. Correspondance concerning this application will be only sent to the agency details listed above. Mandatory fields are marked with an asterisk (*).<br><br>
						<div class="sv-form-horizontal">
							<div class="sv-form-group">
								<label for="IPR_HTEL" class="sv-col-md-3 sv-control-label">Applicant's telephone *</label>
								<div class="sv-col-md-4">
									<input name="IPR_HTEL" id="IPR_HTEL" class="sv-form-control" type="text" maxlength="35" value="">
									<small>Include country code and area code. This field is optional if you have provided us with the applicant's mobile telephone number below.</small>
								</div>
							</div>
							<div class="sv-form-group">
								<label for="IPR_HAT3" class="sv-col-md-3 sv-control-label">Applicant's mobile</label>
								<div class="sv-col-md-4">
									<input name="IPR_HAT3" id="IPR_HAT3" class="sv-form-control" type="text" maxlength="35" value="">
									<small>Include country code and area code. This field is optional if you have provided us with the applicant's telephone number above.</small>
								</div>
							</div>
							<div class="sv-form-group">
								<label for="IPR_HAEM" class="sv-col-md-3 sv-control-label">Applicant's email *</label>
								<div class="sv-col-md-4">
									<input name="IPR_HAEM" id="IPR_HAEM" class="sv-form-control" type="email" maxlength="255" value="jinqiu.guo@mail.mcgill.ca">
									<small>Please provide the applicant's email address. Notifications about this application will only go to the agency details listed above.</small>
								</div>
							</div>
						</div>
					</div>
'''

import re
from selenium.webdriver.common.by import By
from forms.utils.form_utils import set_value_by_id, select_option_by_id, check_button_by_id

class PersonalInfoContact:
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data

    def run(self):
        students = self.data
        driver = self.driver
        personal_info = students[-1][0]
        
        # Telephone number (required unless mobile is provided)
        phone = personal_info.get('Phone', '')
        mobile = personal_info.get('Mobile', '')
        
        # At least one of phone or mobile is required
        if not phone and not mobile:
            phone = "+61 2 1234 5678"  # Default placeholder
        
        set_value_by_id(driver, "IPR_HTEL", phone)
        set_value_by_id(driver, "IPR_HAT3", mobile)
        
        # Email address (required)
        email = personal_info.get('Email', '')
        if not email:
            email = personal_info.get('email', '')  # Try alternate key
        
        if not email:
            email = "student@example.com"  # Default placeholder
            
        set_value_by_id(driver, "IPR_HAEM", email)
        
        # Country selection for permanent address
        select_option_by_id(driver, "IPR_CODC", personal_info.get('Country', 'China (Excludes SARS and Taiwan)'))
        
        # Permanent address fields
        set_value_by_id(driver, "IPR_HAD1", personal_info.get('line1', ''))
        set_value_by_id(driver, "IPR_HAD2", personal_info.get('line2', ''))
        set_value_by_id(driver, "IPR_HAD3", personal_info.get('line3', ''))
        set_value_by_id(driver, "IPR_HAD4", personal_info.get('city', ''))
        set_value_by_id(driver, "IPR_HAD5", personal_info.get('province', ''))
        
        # Handle post code
        post_code = personal_info.get('Post Code', '')
        if not re.search(r'\d+', str(post_code)):
            post_code = '0000'
        set_value_by_id(driver, "IPR_HAPC", post_code)
    
    # Methods removed as they're now imported from form_utils.py