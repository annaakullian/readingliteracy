"""Retrieving data from google spreadsheets.

This file retrieves all information from google spreadsheets and updates the database.
"""
from model import Scholar, Goal, Book, BookLog, Rating, session as dbsession
import gspread
import datetime 
import os

gmail_address = os.environ.get('GMAIL_ADDRESS')
gmail_pw = os.environ.get("GMAIL_PW")

# Login with your Google account
gc = gspread.login(gmail_address, gmail_pw)

#open a spreadsheet by name
#sh = gc.open("testdata")
#open a spreadsheet by url
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1o0Q5492SsrqS6IsMBfruMu-ynJ0xXSg-N3RSc3wTVr8/edit#gid=1751888819')
sh2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/10QnF4dgaAXUE78Y-XnkZLd2NygoiIcHdXvS7XGUE9j0/edit#gid=1751888819')
#select a worksheet
list_sheets = [sh, sh2]

for sheet in list_sheets:
	worksheets = []
	worksheets.append(sheet.get_worksheet(0))

for worksheet in worksheets:
	list_of_lists = worksheet.get_all_values()
	while True:
		for row_list in list_of_lists:
			if row_list[0] == none:
				return False
			else:
				for cell in row_list:
					#put all info into db



#get list_of_lists
list_of_lists = worksheet.get_all_values()

val = worksheet.acell('C4').value
print val