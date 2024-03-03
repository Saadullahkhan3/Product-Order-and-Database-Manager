# Product Order and Database Manager

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

## How Program Works?
As you know we divided this program has two parts but some dependencies so first talk about it.
### Program dependencies

---
Chart for navigate file content.
#### Python Files
| File | Content |
| --- | --- |
| Flag_and_Format_for_table.py | Flags / FormatForTable() |
| General_Product_Task.py | GeneralProductTask()
| Product_database_manipulation.py | ProductManipulation() |
| Product_Order_manger.py | ProductOrderManager() |
#### Database Files
| File | Content |
| --- | --- |
| Products_database.json | Products DB |
| general_store_info.json | General info such as store name, location, etc |

---

### Summary of all program parts
#### Flags --> *Variables*
> We create two (wrong, unexpected) flag variables raises according to user input. We use str() method `.center()` for their formatting to align in center by 50 spaces(both sides) and this variables are kept in `Flag_and_Format_for_table.py` 

---

#### FormatForTable()  --> *Class*
> A Python class that use for auto-alignment of Product tables are uses in both Order manager, Database manager.

---

#### GeneralProductTask() --> *Class*
> A Python class derived from `FormatForTable()`. This class contain general task will be done by both (Order manager, Database manager) such as reading (JSON) files, generate formatted product rows for table(alignment are auto), showing formatted rows where need with table and store header, segment and sort product ids on their availability

--- 

#### ProductManipulation() --> *Class*
> A Python class derived from `GeneralProductTask()`. This class contain all general task as derived and that method uses for seeing, adding, updating and deletion of product with proper functionality

---

#### ProductOrderManager() --> *Class*
> A Python class derived from `GeneralProductTask()`. This class containa all general task as derived and that method uses for show products, taking order, validiate order, create a report of out of stock products, create purchase slip for user and some more helper methods. 

#### Product_database --> *JSON*
> A JSON file for storing products. Each product has it own sequential number ID and each ID contain a dict that contain this ID(product) data.
An example of one product:
```json
{
  "1": {
      "name": "Biryani Masala",
      "brand": "Shan",
      "weight": "75 g",
      "price": 90,
      "quantity": 10
    }
```

---

#### general_store_info --> *JSON*
> A JSON file contain information of our business(store) and in this information we kept name, location(city), e-mail, UAN, TAX for each slip, and a variable that contain number of total issued slip that is used for naming of purchase slip as we create purchase slip in same directory so prevent overwrite we use this technique to prevent overwriting and other data such as name, location are used when showing product table and e-mail, uan, also name, location are used in purchase slip.
Here our general info file:
```json
{
    "store_name": "AL-SF MART",
    "location": "KARACHI",
    "e_mail": "SaadforContact@gmail.com",
    "uan": "021 111 446 248",
    "total_purchase_slip_issued_no": 0,
    "fbr_pos_charges": 1
}
```

---

####


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

> When download these files so keep them is same directory and run `main.py` as this file is responsible for running entire program
_**Note:**_ Product database are initially empty so first add some products *(watch guide video provided below to see guidence)*

---

## Guide Video with Subtitles
Video link : [Guide Video of Product Order and Database Manager](https://drive.google.com/file/d/15z5b1iZ7i4-6SLeBxhtS5PwEAl8yujhE/view?usp=sharing)
