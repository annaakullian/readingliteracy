"""Retrieving data from google spreadsheets.

This file retrieves all information from google spreadsheets and updates the database.
"""

import gspread

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

print list_of_lists[1][0]
print val