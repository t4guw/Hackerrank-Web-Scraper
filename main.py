import re
import time

from scrape_hackerrank import get_problem
from selenium import webdriver


URL = 'https://www.hackerrank.com/domains/algorithms'
count = 0

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

output_file = open("output.txt", "w")

# For every problem card, it finds the problem name
# and inserts it into a full url and stores it in the list
for element in problem_list:
    complete_url = "https://www.hackerrank.com/challenges/" \
                    + problem_name_regex.findall(element)[0] \
                    + "/problem"
    difficulty = difficulty_regex.findall(element)[0]
    problem_urls.append([complete_url, difficulty])


wait_for_login = WebDriverWait(driver, 10)
already_logged_in = False

for problem_url in problem_urls:
    data = get_problem(problem_url[0])
    already_logged_in = True
    count += 1
    output_file.write("\n----------\nALGORITHMS." + str(count) + "\n" + problem_url[1] + "\n----------")
    output_file.write("\nPROBLEM STATEMENT:\n" + data[0] + "\n----------")
    output_file.write("\nTOP SOLUTION:\n----------\n" + data[1] + "\n----------\n====================")
    output_file.flush()
output_file.close()

print("Done")
