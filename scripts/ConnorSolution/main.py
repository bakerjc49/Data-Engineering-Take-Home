from queue_service import QueueService
from hashlib import sha256
from database_manager import DatabaseManager
import json
from datetime import datetime, timezone

# Queue Variables
queue_url = 'http://localhost:4566/000000000000/login-queue'
max_request_messages = 50

# DB Variables
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
database = 'postgres'

insert_query = """
insert into user_logins select * from
json_populate_recordset(NULL::user_logins, %s);
"""


# Formats the data as expected by the DB and appends a create date element
def format_data(data):
    # Add masked fields and pop the old one's
    # Must pop from the JSON then encode before hashing and converting to a string
    data['masked_ip'] = sha256(data.pop('ip').encode('utf-8')).hexdigest()
    data['masked_device_id'] = sha256(data.pop('device_id').encode('utf-8')).hexdigest()

    # The DB expects app version as an integer so remove the periods
    data['app_version'] = int(data['app_version'].replace('.', ''))

    # Append the current timestamp to the JSON
    data.update({'create_date': datetime.now(timezone.utc)})

    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Initialize the queue
    queue_service = QueueService(queue_url=queue_url)
    user_logins = []
    messages = queue_service.get_messages(max_request_messages)
    while len(messages) > 0:
        for message in messages:
            # Clean up raw data
            clean_data = format_data(message)
            # Append to be stored later
            user_logins.append(clean_data)

        messages = queue_service.get_messages(max_request_messages)

    user_logins = json.dumps(user_logins, default=str)

    # Commit to DB
    db_manager = DatabaseManager(user=user, password=password, host=host, port=port, database=database)
    db_manager.setup_connection()
    db_manager.execute_query(insert_query, user_logins)
    db_manager.close_connection()
