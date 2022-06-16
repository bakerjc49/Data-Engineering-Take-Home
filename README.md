## To Run ##
## Summary ##
I took the approach that this would be run sort of like a batch job that would run at a set time and go through all the messages in the queue. This would be based off of a relatively small queue size as it would not work great with a very large queue since a continuous solution was needed. The program flow works the following:

1. 
