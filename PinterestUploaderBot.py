import time
import os
import glob
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from random import randint

index = 0
image_count = 0
count = 1
start_time = time.time()

# ADD your Pinterest account login details below. 
username = "" 
password = "" 

# ADD the boards you want to upload your media.
boardName = [""]
boards = []

# Add full folder path directory for which media files to upload 
image_directory = ""
os.chdir("")

# Defining chrome driver (Change this below if you are using a different web browser). The driver will install and update to the latest version of your browser. 
driver = webdriver.Chrome(ChromeDriverManager().install())

# presets for locating different web elements with xpath and url's
pinterest_url = "https://pinterest.ca/"
pin_builder_url = "https://www.pinterest.ca/pin-builder/"

home_login_button = '/html/body/div[1]/div[1]/div/div/main/div[1]/div[1]/div[2]/div[2]/button'
username_input = '//*[@id="email"]'
password_input = '//*[@id="password"]'
post_login_button = '/html/body/div[1]/div[1]/div/div/main/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/form/div[5]/button'

title_pin = "//*[starts-with(@id, 'pin-draft-title-')]"
media_input = "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/input"
board_menu = "//button[@data-test-id='board-dropdown-select-button']"
save_button = "//button[@data-test-id='board-dropdown-save-button']"

# Getting images from directory
imageList = []
extension = ['*.png','*.PNG','*.jpg','*.JPG','*.jpeg','*.JPEG','*.mp4','*.MP4','*.MOV','*.mov','*.WEBP','*.webp']
for i in extension:
    for filename in glob.glob(i):
        imageList.append(filename)

# Creating a list of available boards
def boardList():
    boards_webelement_list = driver.find_elements_by_xpath('//div[@class="tBJ dyH iFc yTZ pBj DrD IZT mWe z-6"]')
    for board in boards_webelement_list:
        boardName.append(board.get_attribute("innerHTML"))

# Prompting the selection of board from the user
def boardChoice():
    global index
    boardList()
    for num in range(len(boardName)):
        print(str(num)+"-"+boardName[num])
    choice = int(input("Input the number associated with your selected board above: "))
    if choice>=0 and choice<=(len(boardName))-1:
        index = choice
    else:
        boardChoice()
    boardFormat()

# Converting the boards name to a xpath format
def boardFormat():
    for itr in boardName:
        boards.append("//*[@title='{0}']".format(itr))

# Slicing the image name
def prename():
    ind = img.find(".")
    find_ind = img[:(ind)]
    prename = find_ind.replace("_", " ")
    prename = prename.upper()
    return prename

# To get the boards
def getBoards():
    driver.get(pin_builder_url)
    time.sleep(5)
    driver.find_element_by_xpath(board_menu).click()
    time.sleep(3)
    boardChoice()

# To upload the media file to your board
def upload() :
    driver.get(pin_builder_url)
    time.sleep(5)

    driver.find_element_by_xpath(media_input).send_keys(image_directory + img)
    time.sleep(2)

    driver.find_element_by_xpath(title_pin).send_keys(name.title())
    time.sleep(2)

    driver.find_element_by_xpath(board_menu).click()
    time.sleep(3)

    driver.find_element_by_xpath(boards[index]).click()
    time.sleep(3)

    driver.find_element_by_xpath(save_button).click()
    time.sleep(5)

# Login to your account
def login():
    driver.get(pinterest_url)
    driver.find_element_by_xpath(home_login_button).click()
    driver.find_element_by_xpath(username_input).send_keys(username)
    driver.find_element_by_xpath(password_input).send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath(post_login_button).click()
    time.sleep(5)

# Login to your pinterest account
login()
getBoards()

# when there are files in the folder the imageList will be > 1
while image_count < len(imageList):
    for img in imageList:
        name = prename()
        print(str(count)+".", name.title(), "....")
        upload()
        image_count += 1
        count += 1
        time.sleep(randint(12,20))

time.sleep(5)
print("Finished! {} images have been pinned!".format(image_count))

driver.quit()

# Amount of time taken
end_time = time.time()
duration = round(end_time - start_time, 2)
print("Total time taken to complete: " + str(duration))