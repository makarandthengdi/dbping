import mysql.connector
import time
import getpass  # Import the getpass module for secure password input
import sys  # Import the sys module for exit handling
import os # Import the sys module for folder creation 

folder = f"{os.path.expanduser('~')}\\.dbping"
filename = f"{folder}\config.config"

# Check if the directory exists
if not os.path.exists(folder):
    # Create the directory if it doesn't exist
    os.makedirs(folder)

# Function to load configuration from input.config file or prompt user for input
def load_config():
    config = {}
    global filename
    if os.path.exists(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split("=")
                config[key] = value
    
    return config

# Function to write configuration to input.config file
def write_config(config):
    global filename
    with open(filename, "w") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")

def format_input_string(text, length, skip_masking_for_initial_chars):
    if length < 0:
        raise ValueError("Length cannot be negative.")
    if skip_masking_for_initial_chars < 0:
        raise ValueError("Skip masking for initial chars cannot be negative.")

    masked_text = ""
    for i, char in enumerate(text):
        if i < skip_masking_for_initial_chars:
            masked_text += char
        else:
            if i - skip_masking_for_initial_chars < length:
                masked_text += "*"
    
    return masked_text

# Function to connect to the database and execute a SELECT statement
def execute_query(config, query):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Execute the given query
            cursor.execute(query)
            # Fetch all the rows
            result = cursor.fetchall()
            
            for row in result:
                print(row)
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Load configuration from input.config file or prompt user for input
config = load_config()


# Get database connection details from the user or use values from config
host = input(f"Enter host [{format_input_string(config.get('host', ''),6,2)}]: ") or config.get('host', '')
database = input(f"Enter database [{format_input_string(config.get('database', ''),6,2)}]: ") or config.get('database', '')
username = input(f"Enter username [{format_input_string(config.get('user', ''),6,2)}]: ") or config.get('user', '')

# Use getpass to securely input the password or use value from config
password = getpass.getpass(f"Enter password [{format_input_string(config.get('password', ''),6,0)}]: ") or config.get('password', '')

# Store the connection details in a dictionary
config = {
    'user': username,
    'password': password,
    'host': host,
    'database': database
}

# Get the query to execute from the user
query = input("Enter the query to execute (default query `SELECT 1`): ")
query = int(query) if query else 'SELECT 1'

# Get the sleep time from the user, with a default of 5 seconds if not provided
sleep_time_input = input("Enter the sleep time between queries in seconds (default is 5 seconds): ")
sleep_time = int(sleep_time_input) if sleep_time_input else 5

# Write configuration to input.config file for future executions
write_config(config)

try:
    # Execute the query indefinitely with a delay of the specified number of seconds
    print("\n## Press 'Ctrl+C' to stop the loop. ##\n")
    while True:
        execute_query(config, query)
        time.sleep(sleep_time)

except KeyboardInterrupt:  # Handle Ctrl+C (KeyboardInterrupt) signal
    print("\nLoop interrupted by user.")
    sys.exit()  # Exit the script gracefully
