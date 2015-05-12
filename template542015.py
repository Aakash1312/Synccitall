import dropbox
import httplib2
import pprint
import time
import os
import shutil
import ntpath
#import urllib2
#libraries for gdrive file upload
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors
from apiclient import http
#libraries for web browsing
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#libraries for onedrive file upload

#libraries for dropbox file upload
import Tkinter
import tkFileDialog
 
def main():
 
    Tkinter.Tk().withdraw() # Close the root window
    in_path = tkFileDialog.askdirectory()
    return in_path

class file:#bas class file
	authorized=False#whether authorization has taken place or not
	listupdated=False#whether file list is updated or not
	downloadfilepath=None
	found=1
	def __init__(self,location):
		self.address=location#address of file on pc
		
	def upload(self):
		pass
	@staticmethod
	def authorize():
		pass

class gdrivefile(file):
	drive_service=None
	filelist=[]

	def upload(self):
		if gdrivefile.authorized==False :
			gdrivefile.authorize()
			gdrivefile.authorized=True

		FILENAME = self.address
		media_body = MediaFileUpload(FILENAME, mimetype='', resumable=True)
		body = {
		  'title': ntpath.basename(FILENAME),
		  'description': '',
		  'mimeType': ''
		}
		try:
			file = gdrivefile.drive_service.files().insert(body=body, media_body=media_body).execute()
			#iINSERT CODE TO UPDATE FILE LIST
		except errors.HttpError,error :
			print("error in uploading file")
	
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
		try:		
			driver=webdriver.Firefox()#depends on your browser
						
			driver.get(authorize_url)
			cookies=driver.get_cookies()
			for cookie in cookies:
				driver.add_cookie(cookie)			
			#login=driver.find_element_by_name("signIn")
			#login.send_keys(Keys.RETURN)
			accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "submit_approve_access")))
			accept.send_keys(Keys.RETURN)
    			#accept.click()
			a=driver.find_element_by_id("code")
                
			code=a.get_attribute('value')		
			driver.quit()
			gdrivefile.authorized=True
		except:
			print "Could not authorize to Google Drive"
			return None
		#code = raw_input('Enter verification code: ').strip()#change here
		credentials = flow.step2_exchange(code)

		# Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		http = credentials.authorize(http)

		gdrivefile.drive_service = build('drive', 'v2', http=http)
	@staticmethod
	def updatefilelist():#information about files on your drive
		if gdrivefile.authorized==False :
			return None
		page_token = None
		while True:
			try:
				param={}
				if page_token:
					param['pageToken']=page_token
				dfiles=gdrivefile.drive_service.files().list(**param).execute()
				gdrivefile.filelist.extend(dfiles['items'])
				page_token=dfiles.get('nextPageToken')
				gdrivefile.listupdated=True
				if not page_token:
					break
			except errors.HttpError:
				print("error in udating list")
				break
	@staticmethod
	def getfile(add,add2):
		if gdrivefile.listupdated==False:
			gdrivefile.updatefilelist()
		ref=[]	
		sample=add
		for gfile in gdrivefile.filelist:
			if sample in gfile['title']:
				if sample==gfile['title']:
					return gfile
				ref.append(gfile['title'])
		dropboxfile.download(add,add2)
		if file.found==1:
			return None		
		print("No match found.Following are the related files")
		for name in ref:
			print(name)	
		return None				



	@staticmethod					
	def download(add2,add):
		file2download=gdrivefile.getfile(add,add2)
		if file2download==None:
			return
		else:
			downloadedfile=open(file2download.get('title'),"wb")

			download_url=file2download.get('downloadUrl')
			if download_url:
				resp ,content=gdrivefile.drive_service._http.request(download_url)
				if resp.status==200:
					#print('Status',resp)
					downloadedfile.write(content)
					
					src=add2+"/"+ file2download.get('title')
					dest=os.getcwd()+"/"+ file2download.get('title')
					#shutil.move(dest,src)	

					downloadedfile.close()
					#os.rename(dest,src)
					shutil.move(dest,src)
					
				else :
					print("An error occured in downloading")
			else:
				print("No such file exists ")
				 			
class odrivefile(file):
	def upload(self):
		#code for upload
		pass

	@staticmethod
	def authorize():
		pass
		#code for authorization	

class dropboxfile(file):
	client=None
	def upload(self):
		
		if dropboxfile.authorized==False :
			dropboxfile.authorize()
			dropboxfile.authorized=True
		#code for upload
		
		f = open(self.address, 'rb')
		response = dropboxfile.client.put_file(ntpath.basename(self.address), f)

	@staticmethod
	def authorize():
		app_key = '0iwzfwq43mcvirb'
		app_secret = 'ivcutlb76xs5cbr'
	
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		authorize_url = flow.start()
		try:
			driver=webdriver.Firefox()#depends on your browser
			
			driver.get(authorize_url)
			#login=driver.find_element_by_name("signIn")
			#login.send_keys(Keys.RETURN)
			accept= WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, "allow_access")))
			accept.send_keys(Keys.RETURN)
    			#accept.click()
			code=driver.find_element_by_id("auth-code").get_attribute("innerHTML")
                
				
			driver.quit()
			dropboxfile.authorized=True
		except:
			print "Could not authorize to dropbox"
			return None
		dropbox.access_token, dropbox.user_id = flow.finish(code)
		dropboxfile.client = dropbox.client.DropboxClient(dropbox.access_token)
		#code for authorization	
	@staticmethod
	def download(add,add2):
		if dropboxfile.authorized==False :
			return None
		try:		
			f, metadata = dropboxfile.client.get_file_and_metadata("/"+add)
		except TypeError:
			file.found=0
		out = open(add2+"/"+add, 'wb')
		out.write(f.read())
		out.close()

gdrivefile.authorize()
dropboxfile.authorize()
'''
f1=dropboxfile(add)
f1.upload()
'''

if gdrivefile.authorized or dropboxfile.authorized:
	add=raw_input("Enter file to download")
	#print "Please specify download directory. Enter 'n' if you wand default directory"
	#add2=raw_input("Enter response")
	add2=main()
	gdrivefile.download(add2,add)
