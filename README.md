# Database Ping Utility

This Python script is a utility to continuously check for updates or maintain connectivity with a MySQL database instance.

## Prerequisites

Make sure you have the following installed:
- Python
- MySQL Connector for Python

## Usage

1. Clone the repository or download the package.
2. Execute the executable "dbping.exe" (can be found under /dist folder in repository)
3. Provide input details such as database connection, script to execute, delay between executions
4. Monitor the output

## Important Points 

1. The utility saves input credentials in a configuration file for future use, eliminating the need to repeatedly enter them if they remain unchanged. It automatically retrieves the credentials from the config file for subsequent executions.
2. The credentials configuration file is located in the "{user root folder}/.dbping/" directory.
3. The default script to execute is "SELECT 1," commonly used for pinging purposes. However, you have the flexibility to configure the SELECT statement based on your specific requirements.

![dbping - v1 0](https://github.com/makarandthengdi/dbping/assets/3303519/0d443772-2989-47e6-ab87-5984e30e056d)

