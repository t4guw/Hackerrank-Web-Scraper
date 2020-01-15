
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# Presses the escape key to exit a login popup
def press_esc(driver):
    action = ActionChains(driver)
    action.key_down(Keys.ESCAPE)
    action.key_up(Keys.ESCAPE)
    action.perform()


# Automatically logs into a login popup
def log_in(driver):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'Log in')))
    # Click the login tab
    driver.find_element_by_id('Log in').click()
    # Enter email
    driver.find_element_by_id('input-4').send_keys("HackerrankDataCollection@gmail.com")
    # Enter password
    driver.find_element_by_id('input-5').send_keys("Tech4Good")
    # click the login button
    driver.find_element_by_css_selector('#hr_v2 > div.portal-wrapper > div > div > div > section > div > div > div.tab-list-content > div.login-form.auth-form.theme-m > form > div.form-item.clearfix > button').click()


def remove_html_escapes(s):
    html_escapes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in html_escapes:
        s = s.replace(code[1], code[0])
    return s

# Removes all the html junk from the problem statement
def decode_statement_html(s):
    remove_html_escapes(s)
    # Replaces <span>...</span> elements with "[expression]". These are formatted math equations
    s = re.sub('(<span)(.+)(?=</span>)(</span>)', '[expression]', s)
    # Deletes <style>...</style> elements
    s = re.sub('(<style)([\s\S]*)(?=</style>)(</style>)', '', s)
    # Deletes anything else between <angle brackets> to remove the remaining html code
    s = re.sub('((<)(.+?)(?=>))|>', '', s) 
    return s


# Removes all the html junk from the solution
def decode_solution_html(s):
    remove_html_escapes(s)
    # Deletes <pre>...</pre> elements
    s = re.sub('((<pre)(.+?)(?=>)(>))|(</pre>)', '', s)
    return s


# Gets the problem statement of the current problem
def get_problem_statement(driver, already_logged_in):

    # This deals with a login screen that sometimes pops up
    if(not already_logged_in):
        log_in(driver)
    else:
        press_esc(driver)
    
    # gets the html container of element, parses out all the html, and returns it
    statement_element = driver.find_element_by_css_selector('#content > div > div > div > div.community-content > div > section > div > div > div > div.full-screen-split.split-wrap.left-pane > section.problem-statement.split > div > div > div > div > div > div.challenge_problem_statement > div > div')
    statement_string = statement_element.get_attribute('innerHTML')
    return decode_statement_html(statement_string)


# Gets the top solution code of the current problem
def get_problem_solution(driver, count):
    action = ActionChains(driver) #ActionChain object that performs clicks

    # Waits until it can click the Leaderboard tab and then clicks it
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Leaderboard')))
    if count == 0:
        time.sleep(1.5)
    leader_button = driver.find_element_by_css_selector('#Leaderboard')
    action.click(leader_button)
    action.perform()
    
    # Here it tries to click the "unlock solutions" button
    # if it doesn't exist, meaning it has already been clicked before,
    # the wait.until() call will throw an exception and it just moves on
    try:   
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > div > div > div.community-content > div > div.challenge-leaderboard > div > div > div.ui-tabs-wrap > div > section > div:nth-child(1) > div > button > div')))    
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > div > div > div > div.community-content > div > div.challenge-leaderboard > div > div > div.ui-tabs-wrap > div > section > div:nth-child(1) > div > button > div')))    
        unlock_button = driver.find_element_by_css_selector('#content > div > div > div > div.community-content > div > div.challenge-leaderboard > div > div > div.ui-tabs-wrap > div > section > div:nth-child(1) > div > button')
        action.click(unlock_button)
        action.perform()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#hr_v2 > div.portal-wrapper > div > div > div > section > div > div.ui-dialog-body > div > div > button.btn.hr_primary-btn.hr-dialog-button')))
        driver.find_element_by_css_selector('#hr_v2 > div.portal-wrapper > div > div > div > section > div > div.ui-dialog-body > div > div > button.btn.hr_primary-btn.hr-dialog-button').click()
         
    except:
        x = "Do Nothing"

    # Regex to parse out the link to the top solution, and the top solution from its html element
    top_link_regex = re.compile('/rest/contests(.*?)(?=\")')

    # Waits for the top solution's link to be found, then visits that link
    # Sometimes there are no solution links and it returns 'SOLUTION NOT FOUND'
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > div > div > div.community-content > div > div.challenge-leaderboard > div > div > div.ui-tabs-wrap > div > section > div.general-table-wrapper > div > div > div.table-body > div:nth-child(1) > div > div.table-row-column.ellipsis.solutions')))
        top_solution_link = top_link_regex.findall(driver.find_element_by_css_selector('#content > div > div > div > div.community-content > div > div.challenge-leaderboard > div > div > div.ui-tabs-wrap > div > section > div.general-table-wrapper > div > div > div.table-body > div:nth-child(1) > div > div.table-row-column.ellipsis.solutions').get_attribute('innerHTML'))[0]
        driver.get("https://www.hackerrank.com/rest/contests" + top_solution_link)
    except:
        return 'SOLUTION NOT FOUND'
    
    # Waits until it finds the html solution element and then gets its html container
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    top_solution_string = driver.find_element_by_css_selector('body').get_attribute('innerHTML')
    
    top_solution_string = decode_solution_html(top_solution_string)

    return top_solution_string



#Returns a final problem/solution pair
def get_problem(driver, problem_url, count):
    driver.get(problem_url) #Goes to the problem url
    
    statement_string = get_problem_statement(driver, count > 0) #gets the problem statement
    top_solution_string = get_problem_solution(driver, count) #gets the top solution
      
    return [statement_string, top_solution_string]
