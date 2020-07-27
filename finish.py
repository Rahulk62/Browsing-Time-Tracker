import pickle
import pprint
import time
from selenium import webdriver
import webbrowser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary
import time
import easygui as es
import PIL


def start_window( ):
	msg = "Enter Time in Seconds you want to use"
	title = "Running Time"
	fieldNames = ["Time in Seconds"]
	fieldValues = []  # we start with blanks for the values
	fieldValues = es.multenterbox(msg,title, fieldNames)
	print(fieldValues)
# make sure that none of the fields was left blank
	while 1:
		print("inside while")
		errmsg = ""
		if fieldValues == None:
			errmsg = errmsg + ('"%s" Cancel is not the right option.\n\n' % fieldNames[0])
			fieldValues=['0']
		elif fieldValues[0] == '0':
			errmsg = errmsg + ('"%s" Zero is not accepted give number more than 1.\n\n' % fieldNames[0])
			fieldValues = es.multenterbox(errmsg, title, fieldNames, fieldValues)
		elif(not(fieldValues[0].isnumeric())):
			errmsg = errmsg + ('"%s" numbers are only accepted.\n\n' % fieldNames[0])
			fieldValues = es.multenterbox(errmsg, title, fieldNames, fieldValues)
		elif errmsg == "":
			return(fieldValues) # no problems found
def readconfig( ):
	text_file = open("config.txt",'r')
	l = text_file.readlines()
	raw = []
	for i in l:
		i=i.strip('\n')
		raw.append(i)
		
	return(raw)





def save_cookies(driver, location):    #this function to save cookies

    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url=None):

    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    #driver.get("https://google.com" if url is None else url)
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):#Checks if the instance expiry a float 
            cookie['expiry'] = int(cookie['expiry'])# it converts expiry cookie to a int 
        driver.add_cookie(cookie)

def delete_cookies(driver, domains=None):

    if domains is not None:
        cookies = driver.get_cookies()
        original_len = len(cookies)
        for cookie in cookies:
            if str(cookie["domain"]) in domains:
                cookies.remove(cookie)
        if len(cookies) < original_len:  # if cookies changed, we will update them
            # deleting everything and adding the modified cookie object
            driver.delete_all_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        driver.delete_all_cookies()
def all_fav_sites(chrome):
	# Initial load of the domain that we want to save cookies for
	chrome.maximize_window()
	meta_data = readconfig( )
	for i in range(len(meta_data)):
		print(i,meta_data[i])
	chrome.get(meta_data[0]) #here it will find the url in webserver
	username=chrome.find_element_by_id(meta_data[1]) #search id for username input box
	username.send_keys(meta_data[2]) # fill it with that
	password = chrome.find_element_by_id(meta_data[3]) #find for password input box in webpage
	password.send_keys(meta_data[4]) #outmatically fill it my password
	signInButton = chrome.find_element_by_id(meta_data[5]) 
	signInButton.click()
	time.sleep(3)
	site1 = "(window.open('"+meta_data[6]+"'))"
	print(site1)
	chrome.execute_script(site1)
	time.sleep(3)
	site2 = "(window.open('"+meta_data[7]+"'))"
	chrome.execute_script(site2)
	time.sleep(3)
	site3 = "(window.open('"+meta_data[8]+"'))"
	chrome.execute_script(site3)
	time.sleep(3)
	load_cookies(chrome, cookies_location)
	

def end_session(driver):
	save_cookies(driver,cookies_location)
	tabs = len(driver.window_handles)
	print("number of windows "+str(tabs))
	driver.close()
	for i in range(tabs-1):
		driver.switch_to.window(driver.window_handles[-1])
		driver.close()

def last_warning( ):
	reply = ''
	image = "time.png"
	title = "ALERT !!"
	msg = "web-browser is going to shut down\ndo you want to extend time to 30 Second ?"
	choices = ["Yes","No"]
	reply = es.buttonbox(msg,title,image=image, choices=choices)
	if reply == "Yes":
		tm = 10
		print("time extend by 30 sec")
	else:
		tm = 3
		print("extention denied closing in 3 sec")

	msg_2 ='\n\n\tweb-browser will be close in '+str(tm)+' Seconds'
	es.msgbox(msg_2,title = 'confirmation')
	time.sleep(tm)
	return(reply)




# Path where you want to save/load cookies to/from aka C:\my\fav\directory\cookies.txt

cookies_location = "C:/Users/Rahul/Desktop/web scraping/cookies.txt"
try :
	t_time=start_window( ) #user input for total second want to use
	print(t_time)
	chrome = webdriver.Chrome() #webdriver create a handle to control chrome 
	all_fav_sites(chrome)
	print (t_time[0])
	time.sleep(int(t_time[0]))
	last_warning( )
	print('window is going to stop by ',t_time[0])
	end_session(chrome)
	pprint.pprint(chrome.get_cookies())
except Exception as e:
	print("Can't close the web-browser"+str(e))
