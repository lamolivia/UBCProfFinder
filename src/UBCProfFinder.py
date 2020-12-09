from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

webpage = 'https://www.ratemyprofessors.com/'


class ProfFinder:

    def find_prof(self, course_dept, course_num, section):

        # Get to course page #

        url_to_html = requests.get(
            f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname="
            f"subj-section&dept={course_dept}&course={course_num}&section={section}")

        if url_to_html.status_code != 200:
            print("Cannot find course")

        soup = BeautifulSoup(url_to_html.content, "html.parser")
        # print(soup.prettify()) //check html was parsed correctly

        # Find names of professors of course #

        a_tags = soup.find_all('a')
        texts = [a_tag.text for a_tag in a_tags]

        professors = []
        for text in texts:
            if ',' in text:
                professors.append(text)

        print(professors)

        # Open rate my prof website

        if not professors:

            print("no professors found")

        else:

            for prof in professors:

                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                chrome_options.add_experimental_option("detach", True)
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(webpage)

                cookie_button = driver.find_element_by_id("ccpa-footer")
                if cookie_button.is_displayed():
                    cookie_button.find_element_by_css_selector("button").click()

                search_term = prof
                search_box = driver.find_element_by_id("searchr")
                search_box.send_keys(search_term)
                search_box.send_keys(Keys.RETURN)

                prof_schools = driver.find_elements_by_class_name('sub')

                for prof_school in prof_schools:
                    try:
                        print(prof_school.text)
                        if 'UNIVERSITY OF BRITISH COLUMBIA' in prof_school.text:
                            prof_school.click()
                        else:
                            print('could not find prof of given name teaching at UBC')
                    except exceptions.StaleElementReferenceException as e:
                        # thrown because the prof_school element text is printed but DOM has changed
                        pass
