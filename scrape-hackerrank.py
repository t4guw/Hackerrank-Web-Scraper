
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

category = 'data-structures'
URL = 'https://www.hackerrank.com/domains/' + category
count = 0 #Counts the number of problems

# driver the entity used by selenius to interact with a browser
# it should open up its own chrome window
driver = webdriver.Chrome()
driver.get(URL)

# The problem at the bottom of the page
last_problem = "" 
# the problem that used to be at the bottom of the page
previous_last_problem = "" 
# stores whether or not there are any more problems to load
reached_bottom = False

# regular expression for finding the problem sub-url
# in the <a> ... </a> division for each problem card
# Format: "/challenges/problem-name"
problem_name_regex = re.compile("/challenges/(.*?)(?=\")")

difficulty_regex = re.compile("difficulty (.*?)(?= )")

# Due to hackerrank's "infinite scrolling" feature, most of the problems
# are not yet inserted into the page's html doc. This while loop
# continually scrolls down as far as possible and waits for more
# prblems to load, until it reaches the bottom. This makes all the
# problem cards accessible in the html doc.
while not reached_bottom:
    # gets the parent <div> where all the problem cards are located
    problem_container = driver.find_element_by_class_name('challenges-list')
    # converts all html content into one huge, continuous string
    html_string = problem_container.get_attribute('innerHTML')

    # gets the name of the bottom-most problem
    last_problem = problem_name_regex.findall(html_string)[-1]
    # tests if the bottom problem is the same as when it last checked
    # If so, it has reached the bottom
    reached_bottom = last_problem == previous_last_problem

    # Tells the webpage to  execute this javascript function 
    # which scrolls to the bottom of the viewing window
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    previous_last_problem = last_problem

    # Waits three seconds for the page to load more problems.
    # Crude solution but it works
    time.sleep(3)

# creates a list of all problem cards
problem_list = html_string.split('</a>')
# for some reason, the last entry is always empty. Removes last entry
problem_list.pop()
# This stores the final urls
problem_urls = []



# For every problem card, it finds the problem name
# and inserts it into a full url and stores it in the list
for element in problem_list:
    complete_url = "https://www.hackerrank.com/challenges/" \
                    + problem_name_regex.findall(element)[0] \
                    + "/problem"
    difficulty = difficulty_regex.findall(element)
    if len(difficulty) > 0:     
        problem_urls.append([complete_url, difficulty[0]])



wait_for_login = WebDriverWait(driver, 10)
already_logged_in = False


# Removes all the html junk from the problem statement
def parse_problem_statement(statement_html):
    statement_html = re.sub('(<span)(.+)(?=</span>)(</span>)', '[expression]', statement_html)
    statement_html = re.sub('(<style)([\s\S]*)(?=</style>)(</style>)', '', statement_html)
    statement_html = re.sub('((<)(.+?)(?=>))|((</)(.+)(?=>))|>', '', statement_html)
    return statement_html


# Presses the escape key to exit a login popup
def press_esc():
    action = ActionChains(driver)
    action.key_down(Keys.ESCAPE)
    action.key_up(Keys.ESCAPE)
    action.perform()


# Automatically logs into a login popup
def log_in():
    wait_for_login.until(EC.presence_of_element_located((By.ID, 'Log in')))
    # Click the login tab
    driver.find_element_by_id('Log in').click()
    # Enter email
    driver.find_element_by_id('input-4').send_keys("HackerrankDataCollection@gmail.com")
    # Enter password
    driver.find_element_by_id('input-5').send_keys("Tech4Good")
    # click the login button
    driver.find_element_by_css_selector('#hr_v2 > div.portal-wrapper > div > div > div > section > div > div > div.tab-list-content > div.login-form.auth-form.theme-m > form > div.form-item.clearfix > button').click()


# Gets the problem statement of the current problem
def get_problem_statement():

    # This deals with a login screen that sometimes pops up
    if(not already_logged_in):
        log_in()
    else:
        press_esc()
    
    # gets the html container of element, parses out all the html, and returns it
    statement_element = driver.find_element_by_css_selector('#content > div > div > div > div.community-content > div > section > div > div > div > div.full-screen-split.split-wrap.left-pane > section.problem-statement.split > div > div > div > div > div > div.challenge_problem_statement > div > div')
    statement_string = statement_element.get_attribute('innerHTML')
    return parse_problem_statement(statement_string)


# Gets the top solution code of the current problem
def get_problem_solution():
    action = ActionChains(driver) #ActionChain object that performs clicks

# Waits until it can click the Leaderboard tab and then clicks it
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Leaderboard')))
    if count == 0:
        time.sleep(1.5)
    leader_button = driver.find_element_by_css_selector('#Leaderboard')
    action.click(leader_button)
    action.perform()
    
    #Here it tries to click the "unlock solutions" button
    #if it doesn't exist, meaning it has already been clicked before,
    # the wait.untill() call will throw an exception and it just moves on
    try:   
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
    top_solution_regex = re.compile('/rest/contests(.*?)(?=\")')

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

    return re.sub('((<pre)(.+?)(?=>)(>))|(</pre>)', '', top_solution_string)



#Returns a final problem/solution pair
def get_problem(problem_url):
    driver.get(problem_url) #Goes to the problem url
    
    statement_string = get_problem_statement() #gets the problem statement
    top_solution_string = get_problem_solution() #gets the top solution
      
    return [statement_string, top_solution_string]



output_file = open("output.txt", "w")

# Main loop that loops through the list of urls and outputs the 
# problem/solution pairs to the output file
for problem_url in problem_urls:
    data = get_problem(problem_url[0])
    already_logged_in = True
    count += 1
    output_file.write("\n----------\n" + category.capitalize() + "." + str(count) + "\n" + problem_url[1] + "\n----------")
    output_file.write("\nPROBLEM STATEMENT:\n" + data[0] + "\n----------")
    output_file.write("\nTOP SOLUTION:\n----------\n" + data[1] + "\n----------\n====================")
    output_file.flush()
    print(count)
output_file.close()

print("Done")


