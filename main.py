from Product_database_manipulation import start_wroking_on_database
from Product_Order_manager import start_purchasing


products_database_name = "Products_database.json"
general_store_info_file_name = "general_store_info.json"

introduction = '''
----{ PRODUCT ORDER AND DATABASE MANAGER }----
Welcome to our course 'CIT and Python Programming's Final-Project for 'Bano-Qabil 2.0'.

In this project we create a JSON database and take and validiate order from user and update database according to user purchases. This project is divided into two parts:
1. Product Database Manipulation where we can see, add, update and delete(remove product from slots) data 
2. Order Manager where we take order from user and manage things to prevent error

*Note: For further understanding of this project visit GitHub Repository Link: https://github.com/Saadullahkhan3/Product-Order-and-Database-Manager
'''
print(introduction)

while True:
    which_mode = input("\nWhich things you want to do? \n   1 For Product Database Manager \n   2 For Order Manager(purchasing product) \n   Enter 'q' if you want to quit \nEnter here : ")
    
    if which_mode == "q":
        print("Thanks for using it :)")
        quit()

    elif which_mode == "1":
        which_option = input("\nIn Product Database Manager you have 4 options: \n   1 For See data. \n   2 For Add data. \n   3 For Updating existing data. \n   4 Deleting existing data(remove from slots). \n   Enter 'q' if you want to quit. \nEnter here : ")
        
        if which_option == "q":
            print("\nThanks for using it :)")
            quit()

        elif which_option == "1":
            start_wroking_on_database(products_database_name, general_store_info_file_name, see=True)

        elif which_option == "2":
            start_wroking_on_database(products_database_name, general_store_info_file_name, add=True)

        elif which_option == "3":
            start_wroking_on_database(products_database_name, general_store_info_file_name, update=True)

        elif which_option == "4":
            start_wroking_on_database(products_database_name, general_store_info_file_name, delete=True)

        else:
            print("\nOps, Your input is invalid !")

    elif which_mode == "2":
        print("\nLet's, Start Purchasing !\n")
        start_purchasing(products_database_name, general_store_info_file_name)
 
    else:
        print("\nOhh, read guidence properly !")
