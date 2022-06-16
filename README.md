## To Run ##
To run you just need to run `make start` and it will spin up a new container after the existing 2, wait 30s for the queue to be up and running then install requirements and run though the queue. I did modify the indentation on the Makefile since it wouldn't run on my ubuntu box but it's the same as the original other than that.

After the docker container is closed the data will be in the database.

## Summary ##
I took the approach that this would be run sort of like a batch job that would run at a set time and go through all the messages in the queue. This would be based off of a relatively small queue size as it would not work great with a very large queue since a more continuous solution was needed. I tried to expand upon the existing docker compose file so that this was well integrated and easy to test. The program flow works the following:

1. Data gets read into a JSON object from the queue in batches of 100 and processed until the queue is empty.
2. Each response message is formatted to mask the required fields, convert the app version to an integer as per the DB schema, and stamp the message with a create date.
3. Once the queue is empty a connection with the DB is made and the list of formatted messages is inserted.

## Future Improvements ##
If I was going to expand upon this project I would do the following:

1. Create a config file to store values so they are not hard coded.
2. Add logging so the system could be better monitored.
3. Moved the code to delete the queue messages until after they were committed to the DB so data wouldn't potentially be lost on errors.
4. Run performance tests to see what a good value for the `max_request_messages` should be (if any limit).
5. Try and multithread the processing+storing vs the AWS request so that there's less waiting on the data.
6. Find a better solution than storing the app version as an integer since that can lose data on conversion (at least I think)
7. Find a better way than sleeping for 30 seconds to know the AWS queue is set up and ready to send messages.
8. Add a way of knowing when the job has finished such as an email alert.
