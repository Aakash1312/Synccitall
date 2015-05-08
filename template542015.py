import dropbox
import httplib2
import pprint
import time
#libraries for gdrive file upload
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
#libraries for web browsing
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#libraries for onedrive file upload

#libraries for dropbox file upload

class file:#bas class file
	authorized=False#whether authorization has taken place or not
	def __init__(self,location):
		self.address=location#address of file on pc
		
	def upload(self):
		pass
	@staticmethod
	def authorize():
		pass

class gdrivefile(file):
	drive_service=None
	def upload(self):
		if gdrivefile.authorized==False :
			gdrivefile.authorize()
			gdrivefile.authorized=True

		FILENAME = self.address
		media_body = MediaFileUpload(FILENAME, mimetype='', resumable=True)
		body = {
		  'title': FILENAME,
		  'description': '',
		  'mimeType': ''
		}

		file = gdrivefile.drive_service.files().insert(body=body, media_body=media_body).execute()
		#pprint.pprint(file)

	@staticmethod
	def authorize():
		CLIENT_ID = '268285193546-qpu3mbasinue8ofpiah50fu928lcf24b.apps.googleusercontent.com'
		CLIENT_SECRET = '0iyrUyCs-MhAIyOMeYKeeQO-'

		# Check https://developers.google.com/drive/scopes for all available scopes
		OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

		# Redirect URI for installed apps
		REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

		flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
		authorize_url = flow.step1_get_authorize_url()
		#print 'Go to the following link in your browser: ' + authorize_url
		driver=webdriver.Firefox()#depends on your browser
		driver.get(authorize_url)
		#login=driver.find_element_by_name("signIn")
		#login.send_keys(Keys.RETURN)
		accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "submit_approve_access")))
		accept.send_keys(Keys.RETURN)
    	#accept.click()
		a=driver.find_element_by_id("code")
                
		code=a.get_attribute('value')		
		driver.quit()
		#code = raw_input('Enter verification code: ').strip()#change here
		credentials = flow.step2_exchange(code)

		# Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		http = credentials.authorize(http)

		gdrivefile.drive_service = build('drive', 'v2', http=http)

class odrivefile(file):
	def upload(self):
		#code for upload
		pass

	@staticmethod
	def authorize():
		pass
		#code for authorization	

class dropboxfile(file):
	def upload(self):
		access_token=None
		if dropboxfile.authorized==False :
			dropboxfile.authorize()
			dropboxfile.authorized=True
		#code for upload
		client = dropbox.client.DropboxClient(dropbox.access_token)
		f = open('test.txt', 'rb')
		response = client.put_file('/magnum-opus.txt', f)

	@staticmethod
	def authorize():
		app_key = '0iwzfwq43mcvirb'
		app_secret = 'ivcutlb76xs5cbr'
	
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		authorize_url = flow.start()
		driver=webdriver.Firefox()#depends on your browser
		driver.get(authorize_url)
		#login=driver.find_element_by_name("signIn")
		#login.send_keys(Keys.RETURN)
		accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, "allow_access")))
		accept.send_keys(Keys.RETURN)
    	#accept.click()
		code=driver.find_element_by_id("auth-code").get_attribute("innerHTML")
                
		print code		
		driver.quit()
		dropbox.access_token, dropbox.user_id = flow.finish(code)
		#code for authorization	
add=raw_input("enter address of a file")
f1=dropboxfile(add)
f1.upload()
#f1.upload()
