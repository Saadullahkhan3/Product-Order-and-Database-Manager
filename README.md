# Product Order and Database Manager
---
Welcom to our course **CIT and Python Programming** Final-Project from **Bano-Qabil 2.0** 

## What is this?
This project is about managing JSON-based database where how we can see, add, update, delete and how to present it to user that user can easily purchase productd. For simplicity we divived this project into two parts: 

1. Product Database Manager
- See.
- Add.
- Update.
- Delete.

2. Product Order Manager
- Show product(with proper formatting).
- Take order.
- Create report of out of stock product(if any).
- Create purchase slip.

## How to use it?
For using this project you need all 9 files as they are dependencies of `main.py`, because this is hub of all connection and responsible to make program usable.

## Which technology is used?
Python programming language that really and a general purpose language use in Machine Learnig, Web scraping, Backend of web, etc
We use some Python libraries's function listed below with purpose:
- random's randint --> used for generate 4-digit random code to confirm deletion.
- os module --> To check the size of our database file, if size is zero so write default value in it to prevent other potential error.
- json module --> Used for reading and writing our database and general info file as they are JSON file.
- time's strftime --> To get accurate date and time for writing in purchase slip


