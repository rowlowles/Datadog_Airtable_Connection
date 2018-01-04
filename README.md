# Datadog/Airtable Connection 

The intent was to create a basic integration to connect both Datadog and Airtable, allowing users to track important statistics in either software. This was inspired by my time at Grobo, where I used Airtable extensively and begun the work to implement Datadog into our services.

Airtable is an online table/database software, allowing users to create tables to store all manner of data. Common uses are to track inventory, test results, records of units that are built, etc. 

Datadog is an incredibly powerful tool for monitoring your infrastructure health and performance, tracking usage data, etc. 

# Operation

Currently, this script watches a select set of Airtables for updates, and when a new row is added to one of those tables it will create an event in Datadog. As an example, if one Airtable tracks the number of "failures" for some unit that can not be monitored via software (ie, how many times a fan broke), this script would automatically create an event in Datadog. 
