# Internal tool for managing mailshake campaign data and uploads into Google Sheets.
This tool is created to automate a contact's process of retrieving data from Mailshake campaigns and upload onto Google Spreadsheets.  The actual process is meant to allow a user to keep track of outbound email activity.

# Version 1.0
This version features script based tools.  Please refer to documentation and various articles on the webs to confirm your API access to both Mailshake and Google Sheets and understand their authentication process.  These scripts assume that you have already settled both things.

You can run the create_spreadsheets_for_log.py to create your own spreadsheet.  Please make sure you are able to retrieve their spreadsheet ID, which will be needed in the main script.  If you already have your own google spreadsheet, please take note of its ID, found on the last portion of its URL when you access it normally.

For the main script, please note the "configurable" variables that you can adjust accordingly:
- email_reply_type - You can input "unsubscribe", "reply" or "bounce"
- id_of_spreadsheet - basically select spreadsheet you want collected Mailshake data to be uploaded to.

# Version 2.0 (WIP)
This internal tool will have a simple GUI for a user to go through the same process in a familiarly intuitive manner.  I also aim to have this tool to be used on both Windows or Mac.
Here is a clip of what in the works:


https://user-images.githubusercontent.com/34641712/123149601-02abe480-d494-11eb-942f-0180fd35d117.mp4

