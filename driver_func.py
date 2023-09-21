from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("window-size=1200x600")
chrome_options.add_argument('--headless')


# navigation functions
def check(entry):
  output = []
  # set up the webdriver
  driver = webdriver.Chrome(options=chrome_options)
  print("Checking", entry["subtype"], "for", entry["place"])
  driver.get(entry["start_link"])
  # remove cookie banner if exists
  if (len(entry["cookies_steps_ids"]) > 0):
    for step_id in entry["cookies_steps_ids"]:
      if driver.find_element(By.ID, step_id).is_displayed():
        button = driver.find_element(By.ID, step_id)
        button.click()
  for step_id in entry["steps_ids"]:
    button = driver.find_element(By.ID, step_id)
    driver.implicitly_wait(10)
    print(step_id +" is visible? " + str(driver.find_element(By.ID, step_id).is_displayed()))
    ActionChains(driver).move_to_element(button).click(button).perform()
  page_source = driver.page_source
  target_text = entry["flag_check"]
  output.append({"city": entry["city"], "place":entry["place"], "service":entry["type"],"subtype":entry["subtype"], "link":entry['start_link'] ,"available": not (target_text in page_source)})
  
  driver.close()
  return output

async def check_all(data):
  output = []
  for city in data:
    for entry in data[city]:
      print("Running ",city, entry["subtype"], entry["place"])
      response = check(entry)
      output += response
  return output