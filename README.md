# Product Order and Database Manager

---

Welcom to our course **CIT and Python Programming** Final-Project from **Bano-Qabil 2.0** 

---

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

---

## Which technology is used?
Python programming language that really and a general purpose language use in Machine Learnig, Web scraping, Backend of web, etc
We use some Python libraries's function listed below with purpose:
- random module's randint --> used for generate 4-digit random code to confirm deletion.
- os module --> To check the size of our database file, if size is zero so write default value in it to prevent other potential error.
- json module --> Used for reading and writing our database and general info file as they are JSON file.
- time module's strftime --> To get accurate date and time for writing in purchase slip

---

## How to use it?
You need this 7 files in same directory:
### Python Files
1. `Flag_and_Format_of_table.py`
2. `General_Product_task.py`
3. `Product_database_manipulation.py`
4. `Product_Order_manager.py`
5. `main.py` 
### Database and General Info File
6. `Products_database.json`
7. `general_store_info.json`

When download these files run `main.py` as this file is responsible for running entire program

---

## Guide Video - Program Runnig Guide with (subtitles)
Video link (embedding not works): [Guide Video of Product Order and Database Manager](https://drive.google.com/file/d/15z5b1iZ7i4-6SLeBxhtS5PwEAl8yujhE/view?usp=sharing)
