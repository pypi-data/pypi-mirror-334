'''
<div class="sv-panel sv-panel-primary">
				<div class="sv-panel-heading">
					<h2 class="sv-panel-title">Highest qualification details</h2>
				</div>
				<div class="sv-panel-body">
					Please provide details of the highest academic qualification you have completed.<br><br>
					<div class="sv-form-container">
						<div class="sv-form-horizontal">
							<div class="sv-form-group">
								<label for="IPQ_APONLHQL" class="sv-col-md-3 sv-control-label">What is your highest level of educational achievement successfully completed prior to this application? *</label>
								<div class="sv-col-md-4">
									<select name="IPQ_APONLHQL" id="IPQ_APONLHQL" class="" style="display: none;">
										<option value="">-- Select --</option>
										<option value="600">Secondary Qualification</option><option value="524">Certificate I</option><option value="521">Certificate II</option><option value="514">Certificate III</option><option value="511">Certificate IV</option><option value="420">Diploma</option><option value="410">Advanced Diploma and Associate Degree</option><option value="300">Bachelor Degree</option><option value="200">Graduate Diploma or Graduate Certificate</option><option value="120">Master Degree</option><option value="110">Doctoral Degree</option><option value="000">None of the above</option>
									</select><div class="chosen-container chosen-container-single" title="" id="IPQ_APONLHQL_chosen" tabindex="-1" style="width: 100%;"><a class="chosen-single">
  <span id="IPQ_APONLHQL_chosenspan">-- Select --</span>
  <div><b></b></div>
</a>
<div class="chosen-drop">
  <div class="chosen-search">
    <input class="chosen-search-input" type="text" autocomplete="off" title="-- Select --" aria-owns="IPQ_APONLHQL_ul" tabindex="0" aria-autocomplete="list" aria-label="What is your highest level of educational achievement successfully completed prior to this application? * search">
  </div>
  <ul class="chosen-results" role="listbox" tabindex="-1" aria-expanded="false" id="IPQ_APONLHQL_ul" aria-busy="true" aria-label="What is your highest level of educational achievement successfully completed prior to this application? * options"></ul>
</div></div>
									<script type="text/javascript">
										// Set the initial value of IPQ_APONLHQL
										$('#IPQ_APONLHQL').val('');
										sits_chosen_widget('#IPQ_APONLHQL',{});
									</script>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
'''

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from forms.utils.form_utils import set_value_by_id, select_option_by_id, check_button_by_id, select_radio_by_value, is_element_visible

class QualificationsHighestQualificationDetails:
    def __init__(self, driver, data):
        self.driver = driver
        self.data = data

    def run(self):
        students = self.data
        driver = self.driver
        personal_info = students[-1][0]
        
        # Get highest qualification details from data
        highest_qualification = personal_info.get('highest_qualification', {})
        
        # If no highest qualification provided, use sensible defaults
        if not highest_qualification:
            # Try to use the first academic qualification if available
            if 'academic_qualifications' in personal_info and personal_info['academic_qualifications']:
                highest_qualification = personal_info['academic_qualifications'][0]
            else:
                # Default values if no data available
                highest_qualification = {
                    'qualification_type': 'Bachelors degree',
                    'course_title': 'Bachelor of Science',
                    'institution': 'University Example',
                    'country': personal_info.get('Country', 'China (Excludes SARS and Taiwan)'),
                    'completion_year': '2022',
                    'grade': 'First Class',
                    'completed': True,
                    'full_time': True
                }
        
        # Qualification type (dropdown)
        qual_type = highest_qualification.get('qualification_type', 'Bachelors degree')
        select_option_by_id(driver, "IPQ_APONHQ1", qual_type)
        
        # Course title
        course_title = highest_qualification.get('course_title', '')
        set_value_by_id(driver, "IPQ_APONHQ2", course_title)
        
        # Institution
        institution = highest_qualification.get('institution', '')
        set_value_by_id(driver, "IPQ_APONHQ3", institution)
        
        # Country
        country = highest_qualification.get('country', personal_info.get('Country', 'China (Excludes SARS and Taiwan)'))
        select_option_by_id(driver, "IPQ_APONHQ4", country)
        
        # Completion year (dropdown)
        completion_year = highest_qualification.get('completion_year', '2022')
        select_option_by_id(driver, "IPQ_APONHQ5", completion_year)
        
        # Grade/Class
        grade = highest_qualification.get('grade', '')
        set_value_by_id(driver, "IPQ_APONHQ6", grade)
        
        # Completion status (radio buttons)
        completed = highest_qualification.get('completed', True)
        if completed:
            select_radio_by_value(driver, "IPQ_APONHQ7", "COMPLT")
        else:
            select_radio_by_value(driver, "IPQ_APONHQ7", "NOT")
        
        # Handle any conditional fields that may appear based on selections
        if is_element_visible(driver, "IPQ_APONHQ8"):
            # Study mode (full-time/part-time)
            full_time = highest_qualification.get('full_time', True)
            if full_time:
                select_radio_by_value(driver, "IPQ_APONHQ8", "F")
            else:
                select_radio_by_value(driver, "IPQ_APONHQ8", "P")
        
        # Add any additional qualification specific fields as needed
        # For example, if there's a section about uploading transcripts:
        if is_element_visible(driver, "upload_transcript_checkbox"):
            check_button_by_id(driver, "upload_transcript_checkbox")