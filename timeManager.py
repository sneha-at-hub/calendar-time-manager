from __future__ import print_function

from datetime import datetime, timedelta, date, timezone
import os.path
import sqlite3
import webbrowser
import tkinter as tk
from tkinter import messagebox

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser
import pytz  # Import pytz for time zone handling

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# ADD YOUR CALENDAR ID HERE
YOUR_CALENDAR_ID = 'a7f77ce08de269bea5611a7f053192aa482ec19f77ce0d4bd65f9a008569ccf7@group.calendar.google.com'
YOUR_TIMEZONE = 'Asia/Kathmandu'  # Nepal Standard Time

creds = None

def authenticate():
    global creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def add_event(duration, description):
    try:
        start = datetime.now(pytz.timezone(YOUR_TIMEZONE))
        end = start + timedelta(hours=int(duration))
        start_formatted = start.isoformat()
        end_formatted = end.isoformat()

        event = {
            'summary': description,
            'start': {
                'dateTime': start_formatted,
                'timeZone': YOUR_TIMEZONE,
            },
            'end': {
                'dateTime': end_formatted,
                'timeZone': YOUR_TIMEZONE,
            },
        }

        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId=YOUR_CALENDAR_ID, body=event).execute()
        messagebox.showinfo('Event created', f"Event created: {event.get('htmlLink')}")
        commit_hours()
    except HttpError as error:
        messagebox.showerror('Error', f'An error occurred: {error}')

def commit_hours():
    try:
        service = build('calendar', 'v3', credentials=creds)

        today = datetime.now(pytz.timezone(YOUR_TIMEZONE)).date()
        time_start = datetime.combine(today, datetime.min.time()).isoformat() + 'Z'
        time_end = datetime.combine(today, datetime.max.time()).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId=YOUR_CALENDAR_ID, timeMin=time_start, timeMax=time_end,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            messagebox.showinfo('No events', 'No upcoming events found.')
            return

        conn = sqlite3.connect('hours.db')
        cur = conn.cursor()

        for event in events:
            event_id = event['id']
            # Check if event_id already exists in database
            cur.execute("SELECT COUNT(*) FROM hours WHERE EVENT_ID=?", (event_id,))
            count = cur.fetchone()[0]

            if count == 0:  # If event_id does not exist, add it to the database
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                start_formatted = parser.isoparse(start).astimezone(pytz.timezone(YOUR_TIMEZONE))
                end_formatted = parser.isoparse(end).astimezone(pytz.timezone(YOUR_TIMEZONE))
                duration = (end_formatted - start_formatted).total_seconds() / 3600

                event_description = event.get('summary', 'Event')  # Example: Use event summary as description

                event_data = (today.isoformat(), 'CODING', duration, event_description, event_id)
                cur.execute("INSERT INTO hours (DATE, CATEGORY, HOURS, EVENT_DESCRIPTION, EVENT_ID) VALUES (?, ?, ?, ?, ?);", event_data)

        conn.commit()
        conn.close()

        messagebox.showinfo('Success', 'Coding hours added to database successfully')
    except HttpError as error:
        messagebox.showerror('Error', f'An error occurred: {error}')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def get_hours(number_of_days):
    try:
        today = date.today()
        past_date = today - timedelta(days=int(number_of_days))
        today_iso = today.isoformat()
        past_date_iso = past_date.isoformat()

        conn = sqlite3.connect('hours.db')
        cur = conn.cursor()
        cur.execute("SELECT DATE, HOURS FROM hours WHERE DATE BETWEEN ? AND ?", (past_date_iso, today_iso))

        hours = cur.fetchall()

        total_hours = 0
        output = ''
        for element in hours:
            output += f"{element[0]}: {element[1]}\n"
            total_hours += float(element[1])  # Convert to float if necessary

        average_hours = total_hours / float(number_of_days)
        output += f"Total hours: {total_hours}\nAverage hours: {average_hours}"
        messagebox.showinfo('Hours', output)
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def add_event_gui():
    duration = duration_entry.get()
    description = description_entry.get()
    add_event(duration, description)

def get_hours_gui():
    number_of_days = days_entry.get()
    get_hours(number_of_days)

def open_google_calendar():
    webbrowser.open('https://calendar.google.com/calendar/u/0/r')

def create_table_if_not_exists():
    conn = sqlite3.connect('hours.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS hours (
    DATE TEXT NOT NULL,
    CATEGORY TEXT NOT NULL,
    HOURS REAL NOT NULL,
    EVENT_DESCRIPTION TEXT NOT NULL,
    EVENT_ID TEXT NOT NULL  -- Assuming EVENT_ID is a text field
);''')
    conn.commit()
    conn.close()

def main_gui():
    global duration_entry, description_entry, days_entry

    create_table_if_not_exists()  # Ensure the table exists

    root = tk.Tk()
    root.title("Time Manager")

    tk.Label(root, text="Duration (hours):").grid(row=0)
    tk.Label(root, text="Description:").grid(row=1)
    tk.Label(root, text="Number of days:").grid(row=2)

    duration_entry = tk.Entry(root)
    description_entry = tk.Entry(root)
    days_entry = tk.Entry(root)

    duration_entry.grid(row=0, column=1)
    description_entry.grid(row=1, column=1)
    days_entry.grid(row=2, column=1)

    tk.Button(root, text='Add Event', command=add_event_gui).grid(row=3, column=0, pady=4)
    tk.Button(root, text='Get Hours', command=get_hours_gui).grid(row=3, column=1, pady=4)
    tk.Button(root, text='Open Google Calendar', command=open_google_calendar).grid(row=4, columnspan=3, pady=4)

    root.mainloop()

if __name__ == '__main__':
    authenticate()
    main_gui()
