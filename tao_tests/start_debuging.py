from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.get("http://spielplatz.taocloud.org/sprint80/")

print(driver.command_executor._url)
print(driver.session_id)

driver.get('http://crossbrowsertesting.github.io/drag-and-drop.html')
sleep(3)
# maximize the window - DESKTOPS ONLY
# print('Maximizing window')
# self.driver.maximize_window()

# grab the first element
print('Grabbing draggable element')
draggable = driver.find_element_by_id("draggable")

# then the second element
print('Grabbing the droppable element')
droppable = driver.find_element_by_id("droppable")

# we use ActionChains to move the element
print('Dragging the element')
actionChains = ActionChains(driver)
actionChains.drag_and_drop(draggable, droppable).perform()

# let's assert that the droppable element is in the state we want it to be
droppableText = driver.find_element_by_xpath('//*[@id="droppable"]/p').text
assert 'Dropped!' == droppableText
sleep(3)
driver.close()
