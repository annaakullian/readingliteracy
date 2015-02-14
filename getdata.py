"""Retrieving data from google spreadsheets.

This file retrieves all information from google spreadsheets and updates the database.
"""
from model import Scholar, Goal, Book, BookLog, Rating, session as dbsession
import gspread
import datetime 
import os

gmail_address = os.environ.get('GMAIL_ADDRESS')
gmail_pw = os.environ.get('GMAIL_PW')
# Login with your Google account
gc = gspread.login('annaakullian@gmail.com', 'monkeyban')

#open a spreadsheet by name
#sh = gc.open("testdata")
#open a spreadsheet by url
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1o0Q5492SsrqS6IsMBfruMu-ynJ0xXSg-N3RSc3wTVr8/edit#gid=1751888819')

#select a worksheet
worksheet = sh.get_worksheet(0)

#get list_of_lists
list_of_lists = worksheet.get_all_values()

val = worksheet.acell('C4').value

#print list_of_lists[1][0]
#print val

#Queries 
# adds a scholar to the db
scholar1 = Scholar(name = worksheet.acell('B2').value, school = worksheet.acell('D2').value, last_log_in = datetime.datetime.now())
dbsession.add(scholar1)
dbsession.commit()

#adds two goals to the database
goal1 = Goal(scholar_id = scholar1.id, achieved = True, status = 50)
dbsession.add(goal1)
dbsession.commit()

def populate_db():
	"""This function will run every 24 hours to repopulate the db from the google docs with updates
	"""
	#open every sheet and then put them into a list
	#for each sheet in the list of sheets 
	while True:
		for row in sheet:
			if :
			#if B row+1 is blank than return false
			else:
				#add the info from that row into the database

#looping through database to update
#for row in range

# print dbsession.query(Scholar).filter_by(id = 1).first().name
print dbsession.query(Scholar).filter_by(id = 1).first().goals