import requests
import numpy as np
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

# Connect to both APIs for authentication purposes
print("connecting to Mailshake API")
Mailshake_api_key = 'YOUR MAILSHAKE API KEY'
print("connecting to sheets and drive API from Google")
sheets_scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
sheets_credentials = Credentials.from_service_account_file(
    'YOUR CREDENTIAL FILES FOR GOOGLE DRIVE AND SHEETS',
    scopes=sheets_scopes
)

# Type of email replies you want to retreived from your campaigns on Mailshake - please type 'bounce', 'unsubscribe' or 'reply'
# Please refer to the documentation for further details
# Create worksheet with data retrieved from this category for later upload into google spreadsheets
email_reply_type = 'reply'
print("retrieving data from: " + str(email_reply_type))
worksheet_title = email_reply_type

# ID of spreadsheet to be updated
id_of_spreadsheet = 'YOUR SPREADSHEET ID'

# Connect to the /campaign/list end point.  Retrieve Mailshake's campaign IDs - This will access all campaigns you have done on Mailshake
url = "https://api.mailshake.com/2017-04-01/campaigns/list"
payload = {'apiKey' : Mailshake_api_key, 'perPage':'100'}
campaign_list_response = requests.post(url, data=payload)
retrieve_results = campaign_list_response.json()
campaign_ID = []
for i in range(len(retrieve_results['results'])):
    campaign_ID.append(retrieve_results['results'][i]['id'])

# Check these campaign IDs with your campaign URLs
print("Here are the IDs of the campaigns we are extracting data from:")
print(campaign_ID)

# Connect to the /activity/replies endpoint to retrieve information such as email reply types
url = "https://api.mailshake.com/2017-04-01/activity/replies"
for i in range(len(campaign_ID)):

 # initialisation - we will need to collect the original json response in a list and then the nextToken in an array for pagination looping described later.  Subsequently we will collect relevant recipient details - email addresses, time of action, name of recipient if any and the title of the campaign.  Last but not least, we will repeat this main loop to retrieve the data from all campaigns that you have done on Mailshake.  
 # Please note that it is assumed that you have already understood the details in the json responses you will be getting

    print("Initalisation and start API call")
    x = list() # initialise variable for json response
    pagenext = [] # for collecting nextToken
    
    # Initialise empty arrays to collect various details later -
    collected_email_add = [] # email addresses
    collected_email_name = [] # name behind email address
    collected_email_time = [] # time of action - time of reply/bounce/unsubscribe
    collected_campaign_title = [] # campaign title
    
    # Initialise this variable for each campaign ID
    campaignid = campaign_ID[i]

    # Extract original json response and put them in a list.  We will extract information one campaign at a time
    print("current campaign id is: ", campaignid)
    payload = {'apiKey' : Mailshake_api_key,'replyType':email_reply_type,
               'campaignID': campaignid,'receipentEmailAddress': 'firmxyz.com', 'perPage': '100'}
    all_collected_emails = requests.post(url, data=payload)
    x.append(all_collected_emails.json())
    
    # Pagination - check whether you will need to go to the next page since you can retrieve up to 25 entries per page, the next token is used to go into the next page
    print("let's find out the length of the current json result")
    print(len(x[0]['results'])) # check the length of results
    pagenext = x[0]['nextToken'] # get nextToken for this json result
    
    # if the current page has 25 entries, we will have to paginate.
    if (len(x[0]['results'])) == 25:
        print("into pagination loop, send another API call to paginate")
        url = "https://api.mailshake.com/2017-04-01/activity/replies"
        total = len(x[0]['results'])
	# initialisation of variable useful for below loop
        j = 0
        
        # keep covering the subsequent pages until we reach a page with less than 25 entries.  The following page after this will have an empty array for pagenext which captures the nextToken data and it will break the while loop and proceed with other parts of remaining code.  
	# If you have just 25 entries for this particular campaign, the pagenext Token will register an empty string. Then we will automatically skip this while loop and move on.
        while len(pagenext) != 0:
            print("Still looping:" + str(j))
            j = j+1
            print("Current Token is: " + pagenext)
            payload = {'apiKey' : Mailshake_api_key,'replyType':email_reply_type,
                       'campaignID': campaignid,'receipentEmailAddress': 'firmxyz.com','nextToken': pagenext}
            collected_email_specific_2 = requests.post(url, data=payload)
            x.append(collected_email_specific_2.json())
            pagenext = x[j]['nextToken']
            print(len(x[j]['results']))
            total += len(x[j]['results'])
            print("loop check for current total of json results and nextToken")
            print(total)
            print(pagenext)
    	
	# delete any empty keys found in the json response
        print("Delete any empty key value")
        x = list(filter(None, ({key: val for key, val in sub.items() if val} for sub in x)))
        
	# collect all relevant details by parsing the original json response and into csv
        print("extract requested data")
        for a in range(len(x)):
            length = len(x[a]['results'])
            print("Current length of json results under current campaign is " + str(length))
            for b in range(length):
                collected_email_add.append(x[a]['results'][b]['recipient']['emailAddress'])
                collected_email_name.append(x[a]['results'][b]['recipient']['fullName'])
                collected_email_time.append(x[a]['results'][b]['recipient']['created'])
                collected_campaign_title.append(x[a]['results'][b]['campaign']['title'])        
        print("Check total number of email addresses for this current campaign: " + str(campaignid))
        print(len(collected_email_add))
 
	# create a dataframe       
        print("export data into csv")
        rows = {'collected_email_addresses': collected_email_add,
                'collected_names': collected_email_name, 
                'time_of_action': collected_email_time, 
                'campaign_action': collected_campaign_title
               }
        df = pd.DataFrame(data = rows)
        df['time_of_action'] = pd.to_datetime(df['time_of_action'], format='%Y-%m-%d %H:%M')
        df.to_csv("path_to_csv_file", header = False, mode = 'a', index = False)
        print("Campaign ID " + str(campaignid) + " collection of emails complete")
        
    # if pagination is not required
    else:
        print("No need for pagination, continue to extract requested data")
        
	# delete any empty keys found in the json response
        print("Delete any empty key value")
        x = list(filter(None, ({key: val for key, val in sub.items() if val} for sub in x)))
        
	# collect all relevant details by parsing the original json response and into csv
        print("extract requested data")
        for c in range(len(x)):
            length = len(x[c]['results'])
            print("Current length of json results under current campaign is " + str(length))
            for d in range(length):
                collected_email_add.append(x[c]['results'][d]['recipient']['emailAddress'])
                collected_email_name.append(x[c]['results'][d]['recipient']['fullName'])
                collected_email_time.append(x[c]['results'][d]['recipient']['created'])
                collected_campaign_title.append(x[c]['results'][d]['campaign']['title'])        
        
        print("Check total number of email addresses for this current campaign: " + str(campaignid))
        print(len(collected_email_add))
        
	# create a dataframe
        print("export data into csv")
        rows = {'collected_email_addresses': collected_email_add,
                'collected_names': collected_email_name, 
                'time_of_action': collected_email_time, 
                'campaign_title': collected_campaign_title
               }
        df = pd.DataFrame(data = rows)
        df['time_of_action'] = pd.to_datetime(df['time_of_action'], format='%Y-%m-%d %H:%M')
        df.to_csv("path_to_csv_file", header = False, mode = 'a', index = False)
        print("Campaign ID " + str(campaignid) + " collection of emails complete")

# Export csv to googlesheets
print("authorise credentials for sheets and drive")
gc = gspread.authorize(sheets_credentials) # authorise same google credentials to enable gspread to upload data into google sheets
print("export dataframe of collected data into google spreadsheet")
df2 = pd.read_csv('marcus_mailshake.csv', header = None) # create dataframe for uploaded csv
df2.columns = ['emailaddress','fullname','timeofaction','campaigntitle']
sh = gc.open_by_key(id_of_spreadsheet) # open log, retrieve API key from previous code
worksheet = sh.worksheet(worksheet_title) # assumes the worksheet for specific email category is present within an existing spreadsheet
sh.del_worksheet(worksheet) # delete any existing worksheets as this code will upload a fresh batch of data, you can opt not to use this
# upload
worksheet = sh.add_worksheet(title = worksheet_title, rows = '1000', cols = '8')
set_with_dataframe(worksheet, df2)
sh.share('intended_google_email_account', perm_type = 'user', role = 'writer')
print(sh) #print spreadsheet id, please check your drive
