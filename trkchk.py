import requests
import os
from rich.console import Console
from rich.table import Table
from termcolor import colored

# Tracker file
TRACKER_FILE = 'data/trackers.txt'
MENU = [
    { 'item': 1, 'name': 'Check for open signups', 'function': 'checkForOpenSignups' },
    { 'item': 2, 'name': 'List trackers', 'function': 'listTrackers' },
    { 'item': 3, 'name': 'Add a tracker to the list', 'function': 'addTrackerToFile' },
    { 'item': 4, 'name': 'Remove a tracker from the list', 'function': 'removeTrackerFromFile' },
    { 'item': 5, 'name': 'Exit', 'function': 'exit' }
]

# Logo
def displayLogo():
    print('████████ ██████  ██   ██  ██████ ██   ██ ██   ██'); 
    print('   ██    ██   ██ ██  ██  ██      ██   ██ ██  ██ '); 
    print('   ██    ██████  █████   ██      ███████ █████  '); 
    print('   ██    ██   ██ ██  ██  ██      ██   ██ ██  ██ '); 
    print('   ██    ██   ██ ██   ██  ██████ ██   ██ ██   ██');
    print('-------------------------------------------------');


# Menu + input
def getMenuInput():
    for menuItem in MENU:
        print('[' + str(menuItem['item']) + '] ' + menuItem['name'])
    userInput = input('> ')
    print('\n')
    return userInput

# Check that the tracker file exists
def checkTrackerFileStatus():
    if not os.path.isfile(TRACKER_FILE):
        print(colored('[ERROR]', 'red') + ' Tracker list not found!')
        input('Press enter to exit...')
        exit()

# List trackers
def listTrackers():

    checkTrackerFileStatus()
    
    rows = []
    columns = ['ID', 'Name', 'Reg. URL', 'Closed text']

    # Open the file and read the trackers into an array
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        i = 1
        for line in lines:
            line = line.strip()
            tracker = line.split('|')
            trackerName = tracker[0]
            trackerUrl = tracker[1]
            trackerText = tracker[2]
            rows.append([str(i), tracker[0], tracker[1], tracker[2]])
            i = i + 1

    # Print the trackers in a table format
    table = Table(title='Trackers')
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*row, style='bright_green')
    console = Console()
    console.print(table)

# Check for open signups
def checkForOpenSignups():

    checkTrackerFileStatus()

    print('[CHECKING FOR OPEN SIGNUPS]')
    trackers = []

    # Open the file and read the trackers into an array
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            tracker = line.split('|')
            trackerName = tracker[0]
            trackerUrl = tracker[1]
            trackerText = tracker[2]
            trackers.append([tracker[0], tracker[1], tracker[2]])
    
    # Check each tracker
    for tracker in trackers:

        # Get the tracker's response
        try:
            response = requests.get(tracker[1])
        except:
            print(colored('[ERROR]', 'red') + ' Could not connect to ' + colored(tracker[0], 'yellow'))
            continue

        # If the response includes the text we are looking for it is closed
        if tracker[2] in response.text:
            print(colored(tracker[0], 'yellow') + ' is ' + colored('closed', 'red'))

        # If the response doesn't include the text we are looking for it is open
        else:
            print(colored(tracker[0], 'yellow') + ' is ' + colored('open', 'green') + ' | ' + colored(tracker[1], 'blue'))

# Add tracker to file
def addTrackerToFile():

    print('[ADD TRACKER TO LIST]')
    tracker = input('Tracker name: ')
    url = input('Tracker registration URL: ')
    text = input('Text to look for: ')

    # Add the tracker to the list
    with open(TRACKER_FILE, 'a', encoding='utf-8') as f:
        f.write(tracker + '|' + url + '|' + text + '\n')

    print(colored('Tracker added!', 'green'))

# Remove tracker from file
def removeTrackerFromFile():

    checkTrackerFileStatus()

    print('[REMOVE TRACKER FROM LIST]')
    listTrackers()
    trackerInput = input('Tracker ID: ')

    # Remove tracker from the list based on the ID (line number)
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        # Check that the tracker ID is a valid line number
        if int(trackerInput) > len(lines):
            print(colored('[ERROR]', 'red') + ' Tracker ID not found!')
            input('Press enter to exit...')
            exit()
        
        # Remove the tracker from the list
        lines.pop(int(trackerInput) - 1)
        with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    print(colored('Tracker removed!', 'green'))

# Logo
displayLogo()

while True:

    # Grab user input
    userInput = getMenuInput()

    # Check if the user entered a valid number
    if userInput.isdigit():
        userInput = int(userInput)
        if userInput == 5:
            exit()
        if userInput > 0 and userInput <= len(MENU):
            locals()[MENU[userInput - 1]['function']]()
        else:
            print(colored('[ERROR]', 'red') + ' Invalid menu item!')
            input('Press enter to exit...')