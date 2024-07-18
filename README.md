
Tkinter is a Python binding to the Tk GUI toolkit. It is the standard Python interface to the Tk GUI toolkit, and is Python's de facto standard GUI.
This Python script integrates with Google Calendar API for efficient time management. It allows users to authenticate securely, add events with durations and descriptions to Google Calendar, and track coding hours stored in a SQLite database. A tkinter GUI provides an intuitive interface for these tasks, enhancing productivity by facilitating event scheduling and time tracking directly within the application.

# Cloning github
```bash
git clone https://github.com/sneha-at-hub/calendar-time-manager.git
```
### Install SQLite Viewer in VS Code
- Download and install the **SQLite Viewer** extension by ***Florian Klamfer*** from the VS Code marketplace.

# Installing Dependencies
You can run this command in your terminal or command prompt to install all the necessary packages (google-auth, google-auth-oauthlib, google-api-python-client, python-dateutil, pytz) for your script to function correctly. Make sure you have Python and pip installed on your system and that they are up to date.
```bash
pip install google-auth google-auth-oauthlib google-api-python-client python-dateutil pytz
```
### Running the file
**Create the database**
- Open your terminal in VS Code and run the following code.
```bash
python createTable.py
```
- This script will set up your database with the required tables.
- 
**Running the Main file** 
Now run the timeManager.py file
```bash
python timeManager.py
```
- This command executes your main application code, utilizing the database you've set up.

# Accessing your Account from Google Cloud
### 1. Create a Project
- Navigate to [Google Cloud Console](https://console.cloud.google.com/)
- On the left-hand side, hover over **IAM & Admin** and click on **Create Project**.
- Enter your project name and click **Create**.

### 2. Enable Google Calendar API:
- In the left sidebar, click on **API & Services**:
- Click **Enable APIs and Services**.
- Search for **Google Calendar**.
- Select **Google Calendar API** and click **Enable**.

### 3. Configure OAuth Consent Screen:
- Click on **OAuth consent screen** from the **APIs and services tab**.
- Choose **External** and click **Create**.
- You will be redirected to **Edit app registeration**
- Fill in the details:
        **App name**: "Time Management"
        **User support email**: Your email
        **Developer contact information**: Your email
- Click **Continue**.

### 3. Set OAuth Scopes:
- After saving the consent screen details, you'll be redirected to the OAuth consent screen settings.
- Click on **Scopes** and then **Add or Remove Scopes**
- Select all relevant Google Calendar API scopes that your application will need access to.( I would suggest to select all the API's)
- Click **Update** and then **Save and Continue**.

### 4. Create OAuth Credentials
- In the left-hand sidebar, click on **Credentials**.
- Click **Create Credentials** and select **OAuth client ID**.
- Choose **Application type** as **Desktop app**
- Enter a name for your OAuth client (e.g., "Desktop Client 1") or leave it as default.
- Click **Click Create**

### 5. Download Credentials
- After creating the OAuth client, a pop-up will display confirming the OAuth client creation.
- Click **Download JSON**. to download the client configuration file.
- Save the file to your project directory.
- Rename the downloaded JSON file to **credentials.json**.
- Move it to your Folder

### 6. Adding Test Users for OAuth Consent
To grant access to your Google account, you'll need to add test users to your OAuth consent screen. Follow these steps:
- Navigate to **APIs & Services > OAuth consent screen** in your Google Cloud Console:
        - Go to your Google Cloud Console.
        - Click on **APIs & Services** in the menu.
        - Select **OAuth consent screen**.
- Click on **Add Users**.
- Enter your email credetials to grant permissions for the application to access your Google account.

### 7. Starting with Google API
- Navigate to https://developers.google.com/calendar/api/guides/overview 
- On the left-hand side, click on **Quickstarts** and select **Python**.

## OR 
- You can directly access the Python Quickstart guide through https://developers.google.com/calendar/api/quickstart/python


### Installing Dependencies 

- Install all the dependencies. Open your terminal and run the following commands:
```bash 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
### Create and Run the Quickstart Script
Create a new Python file named quickstart.py in your project directory. Copy and paste the following code into quickstart.py:
```bash
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

```
### Adjusting OAuth Scope
- Make sure to remove readinly from SCOPE to adjust the OAuth scope to allow for read and write access as needed for your application. 
It should look like this 

```bash
SCOPES = ["https://www.googleapis.com/auth/calendar"]
```
- Open your terminal and navigate to the directory containing quickstart.py.
- Run the script using the following command
```bash 
python quickstart.py

```
- Finally, Login with your Google credentials when prompted to grant permission for the script to access your Google Calendar data.

