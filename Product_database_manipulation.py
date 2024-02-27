from Flags_and_Format_for_table import flag_unexpected, flag_wrong
from General_Product_task import GeneralProductTask
import json
from random import randint      # use for generating random code for confirm deletion of product

class ProductManipulation(GeneralProductTask):
    def __init__(self, products_data_json_file_name, general_info_file_name):
        # Calling parent class '__init__' for initialize instance variables
        super().__init__()
        self.products_data_json_file_name = products_data_json_file_name
        self.products_dict = None
        self.general_info_file_name = general_info_file_name


    def show_products_by_mode(self, all_products_ids, availabel_products_ids, unavailabel_products_ids, products_database):
        '''
        Show products by mode where mode is taking inside it. There are four mode where (all ids, availabel ids, out of stock ids, blank slots ids) are displayed and also a quit option

        Args:
            can be getted by segement of products ids
        '''
        while True:
            which_mode = input("\nEnter Number according to which mode you want to choose \n   1 For Show all products. \n   2 For Show Only available products. \n   3 For Show Only out of stock products. \n   4 For Show Only one product(you need to enter that product id). \n   5 For Blank slots IDs. \n   Type 'q' to leave it. \nEnter here : ")

            if which_mode == "q":
                break

            # Checking that input is integers only
            elif which_mode.isdigit():
                # Check show options
                if which_mode == "1":
                    all_ids_without_blank_ids = availabel_products_ids + unavailabel_products_ids 
                    formatted_rows = self.generate_formatted_product_rows(all_ids_without_blank_ids, products_database)
                    self.print_formatted_product_rows_with_store_and_table_header(formatted_rows)
                
                elif which_mode == "2":
                    formatted_rows = self.generate_formatted_product_rows(availabel_products_ids, products_database)
                    self.print_formatted_product_rows_with_store_and_table_header(formatted_rows)
                
                elif which_mode == "3":
                    formatted_rows = self.generate_formatted_product_rows(unavailabel_products_ids, products_database)
                    self.print_formatted_product_rows_with_store_and_table_header(formatted_rows)
                
                elif which_mode == "4":
                    while True:
                        which_id = input("Enter product id you want to see OR enter 'q' to leave it : ")
                        if which_id in all_products_ids:
                            formatted_rows = self.generate_formatted_product_rows([which_id], products_database)
                            self.print_formatted_product_rows_with_store_and_table_header(formatted_rows)
                            break
                        elif which_id == "q":
                            break
                        else:
                            print(f"This id -> '{which_id}' is not found in database. Try Different!")

                elif which_mode == "5":
                    print("\n" + self._store_header)
                    for _id in self.blank_slot_ids:
                        print(f"Showing Blank Slots IDs \n->> {_id}")

                else:
                    print(f"{flag_wrong} Please enter a valid option")

            else:
                print(f"{flag_wrong} Please enter a valid option. \n")


    def update_attributes_by_rereading(self):
        '''
        Reads product data from the JSON file and segments the product IDs based on their characteristics. Main purpose that is call this function when database update so program will also update accurately.
        '''
        self.read_product_data(self.products_data_json_file_name)
        self.segment_product_ids_by_characteristics(self.products_dict)


    def write_product_to_databse(self, products_database: dict, products_data_json_file_name: str):
        '''
         Writes the updated product database to a JSON file.

        Args:
            products_database (dict): A dictionary containing the updated product data.
                Each key represents a product ID, and the corresponding value is a dictionary
                containing product information.
            products_data_json_file_name (str): The file path to the JSON file where the product data will be written.

        Raises:
            FileNotFoundError: If the specified JSON file path does not exist.

        Notes:
            This function updates the product database by writing the provided dictionary
            containing product data to the specified JSON file. The data is formatted with an
            indentation of 4 spaces for improved readability. 
        '''
        with open(products_data_json_file_name, "w") as product_writer:
            json.dump(products_database, product_writer, indent=4)


    def get_valid_attribute_info(self, input_message, quit_option=False, name=False, price=False, quantity=False, datatype=str):
        '''
        Use for taking our needed input for attributes of products
        
        Arg:
            input_message (str): Indicate user that what input is needed here.
            quit_option (bool, optional): Keep it Ture when quit option by entering 'q' in 'input_message' is provided.
            Note: Keep only one arg True from below three args at a time or not.
            name (bool, optional): when True, apply name condition that must be satisfied.
            price (bool, optional): when True, apply price condition that must be satisfied.
            quantity (bool, optional): when True, apply quantity condition that must be satisfied.
            datatype (str or int): When int, accept only int datatype.
                Default is str. 
        Returns:
            Checked and validated attribute(it can be affected by default arg except quit_option).
            Status of work
        '''
        # Because of nested loop define outside loop's conditon in var so it can changed inside nested loop
        run_loop = True
        while run_loop:
            product_attribute = input(input_message).strip()
  
            # For quit option
            if quit_option and product_attribute == "q":
                return "leaved"
            
            # When datatype is set to int
            if datatype == int:
                if product_attribute.isdigit():
                    product_attribute = int(product_attribute)
                else:
                    print(f"{flag_unexpected} Please enter a valid integer input!")
                    continue

            # When quantity arg is True
            if quantity:
                    if product_attribute < 0 or product_attribute > 10:
                        print(f"Minimum limit is 1 (0 for out of stock) and Maximum limit of any product is 10 ! \n")
                        continue

                    elif product_attribute == 0:
                        # while True:
                        is_confirm = input(f"Do you want to out of stock it! \nType 'y' for yes OR press 'Enter' to give value again. \nEnter here: ")
                        if is_confirm == "y":
                            return product_attribute
                        
                        continue

            # When price arg is True
            elif price:
                if not product_attribute >= 5:
                    print(f"{flag_unexpected} Price must be greater than or equal to 5 ! \n")
                    continue
            
            # When name arg is True
            elif name:
                if product_attribute == "0000":
                    print(f"{flag_unexpected} This name --> {product_attribute} is not valid, it is for blank slots")
                    continue
                elif len(product_attribute) < 3:
                    price("\Product name contain atleast 3 characters")

            # Starting a infinite loop until gets needed value
            while True:
                # Asking for validiate input
                print(f"\n{product_attribute} <-- is Correct?")
                is_confirm = input("Type 'y' if it correct OR Type 'c' to change it. \nEnter here : ")
                # When right returned it
                if is_confirm == "y":
                    return product_attribute
                
                # When want to change stop nested loop and shift to outside loop
                elif is_confirm == "c":
                    print("Enter value again! \n")
                    break
                else:
                    print(f"{flag_unexpected} Please enter a valid option")
            

    def add_products(self, products_database):
        '''
        Add product in dictionary with proper validiation. This dictionary can be used writing it in JSON file as data

        Args:
            products_database (dict): Added data will write in dictionary
        
        Returns:
            Status of work
        '''
        # Infiite loop for asking that user really want to add some things
        while True:
            want_to_add = input("Type 'yes' to add new product OR Type 'no' to dismiss it. \nEnter here : ")
            if want_to_add == "no":
                return "leaved"
            # when not yes
            elif want_to_add != "yes":
                print(f"{flag_wrong} Enter a valid choice!")
            # yes because we check not yes above if it not yes so it ask again but it is yes no != is False
            else:
                break

        # Check if any slot is availabel, if not so create a new one by adding 1 in max id
        if self.blank_slot_ids:
            new_product_id = self.blank_slot_ids[0]
        else:
            new_product_id = str(int(self.all_ids[-1]) + 1)

        print(f"\n--> Enter {new_product_id} ID's Product Info:")
        product_name = self.get_valid_attribute_info("Enter Name of New Product: ", name=True)
        product_brand = self.get_valid_attribute_info(f"Enter Brand of {product_name}: ")
        product_weight = self.get_valid_attribute_info(f"Enter Weight of New Product: ")
        product_price = self.get_valid_attribute_info(f"Enter Price of {product_name}(Minimum price is 5): ", price=True, datatype=int)
        product_quantity = self.get_valid_attribute_info(f"Enter Quantity of {product_name}(Minimum is 1 and Maximum is 10): ", quantity=True, datatype=int)

        # Writing getted values in dictionary
        products_database[new_product_id] = { 
            "name": product_name,
            "brand": product_brand,
            "weight": product_weight,
            "price": product_price,
            "quantity": product_quantity
        }
        # Showing getted values
        print(f"\nHere is getted info of ID no {new_product_id}, Please confrim it !.")
        print(f" Name: {products_database[new_product_id]["name"]} \n Brand: {products_database[new_product_id]["brand"]} \n Weight: {products_database[new_product_id]["weight"]} \n Price: {products_database[new_product_id]["price"]} \n Quantity: {products_database[new_product_id]["quantity"]}")
        
        # Todo: Add a option that if user want to update info
        # Confirm to user that data showed above is right or not
        while True:
            is_right_info = input("\nType 'yes' to finally add into database OR Type 'no' if you want to reject it. \nEnter here : ")

            if is_right_info == 'yes':
                self.write_product_to_databse(products_database, self.products_data_json_file_name)
                self.update_attributes_by_rereading()
                return "Product Added"                

            elif is_right_info == 'no':
                return "Product Addition is Rejected!"

            else:
                print(f"{flag_wrong} Please enter a valid choice !")


    def update_attribute(self, all_ids: list, products_data_json_file_name, products_database):
        '''
        Use for updating attribute of products(ids)

        Args:
            all_ids (list): List of all ids include(availabel, out of stock and blank slots ids)
            products_data_json_file_name (str): Product JSON database path
            products_database (dict): Product database that actually update and then write it into database
        '''
        # Because of nested loop define outside loop's conditon in var so it can changed inside nested loop
        run_loop = True
        while run_loop:
            which_way_or_id = input("\nEnter Product id to change its info OR enter 'q' to leave it. \nEnter here : ")

            if which_way_or_id == "q":
                return "leaved"
            
            elif which_way_or_id in all_ids:
                extracted_info = self.extract_one_product_attributes(which_way_or_id, products_database)
                
                # This is used for knowing object var name and then assigning values to object var 
                attibute_name = str()
                while True:
                    print("Showing current info and enter that attribute number for update :")
                    which_attribute = input(f"   1 For Name: {extracted_info[1]}\n   2 For Brand: {extracted_info[2]}\n   3 For Weight: {extracted_info[3]}\n   4 For Price: {extracted_info[4]}\n   5 For Quantity: {extracted_info[5]} \n   'q' For quit \nEnter here: ")
                    
                    if which_attribute == "q":
                        return "leaved"

                    elif which_attribute == "1":
                        attibute_name = "name"      # Assign 
                        updated_info = self.get_valid_attribute_info(f"Enter New Name : ", quit_option=True, datatype=str)                        
                        # Stop outside infinite loop
                        run_loop = False
                        break
                    
                    elif which_attribute == "2":
                        attibute_name = "brand"
                        updated_info = self.get_valid_attribute_info(f"Enter New Brand : ", quit_option=True, datatype=str)
                        # Stop outside infinite loop
                        run_loop = False
                        break

                    elif which_attribute == "3":
                        attibute_name = "weight"
                        updated_info = self.get_valid_attribute_info(f"Enter New Weight : ", quit_option=True, datatype=str)
                        # Stop outside infinite loop
                        run_loop = False
                        break

                    elif which_attribute == "4":
                        attibute_name = "price"
                        updated_info = self.get_valid_attribute_info(f"Enter New Price : ", quit_option=True, price=True, datatype=int)
                        # Stop outside infinite loop
                        run_loop = False
                        break

                    elif which_attribute == "5":
                        attibute_name = "quantity"
                        updated_info = self.get_valid_attribute_info(f"Enter New Quantity : ", quit_option=True, quantity=True, datatype=int)
                        # Stop outside infinite loop
                        run_loop = False
                        break

                    else:
                        print(f"{flag_unexpected} Enter a valid option OR enter 'q' to leave it !")
            else:
                print(f"{flag_unexpected} ID -> {which_way_or_id} not found OR you enter a invalid input!. \nPlease enter a valid input!.")

        # When user not quit inside nested loop so run below code
        if updated_info != "leaved":
            self.products_dict[which_way_or_id][attibute_name] = updated_info
            # Write into file
            self.write_product_to_databse(products_database, products_data_json_file_name)
            self.update_attributes_by_rereading()
            return "Attribute Updated"
        
        return updated_info        


    def _remove_one_product(self, products_database: dict):
        '''
        It add default value in place of old values of given id(it take id input itself). It only remove product info and make that id as blank that can be used when adding products. For confirm deletion it ask for enter 4-digit random code(updated everytime) and after confirm deletion write product database dictionary in database.  

        Args:
            products_database (dict): Product database dictionary. 
        
        Returns:
            Status of work
        '''
        while True:
            product_id_input = input("Enter Product ID to delete it OR enter 'q' to leaved it : ")
            if product_id_input == "q":
                return "leaved"
            
            elif product_id_input in self.all_ids:
                while True:
                    # Random code to confirm deletion
                    four_str_char_random_code = "".join([str(randint(1,9)) for code in range(4)])
                    # Extract and Format user entered product's info 
                    product_info = self.extract_one_product_attributes(product_id_input, products_database)
                    formetted_info = self.show_product_row(*product_info)   # Pass tuple

                    print(f"Your given id {product_id_input}'s info. Confirm this product.\n{formetted_info}")
                    # asking for confirmation of deletion or dismiss deletion
                    remove_or_not = input(f"Type the 4-digit code -> {four_str_char_random_code} to confirm the removal of the product. Alternatively, type 'q' to cancel the operation. \nEnter here: ")
                    # If confirm write default data
                    if remove_or_not == four_str_char_random_code:
                        products_database[product_id_input] = {
                            "name": "0000",
                            "brand": "",
                            "weight": "",
                            "price": 5,
                            "quantity": -1
                        }
                        # Write to file
                        self.write_product_to_databse(products_database, self.products_data_json_file_name)
                        self.update_attributes_by_rereading()
                        return "Removed"
                    
                    # For cancel this operation
                    elif remove_or_not == "q":
                        return "Cancelled"
                    
                    # When code not matched
                    else:
                        print(f"Your input -> {remove_or_not} is not match to code. \n Are you want to cancel it so Type 'q' OR its Typo so type code again! \n")
                        # It will ask again because of while True (infinite loop)
            else: 
                print(f"{flag_wrong} Invalid input OR --> {product_id_input} is not found :( ")


    def __str__(self):
        return "This is an object for database manipulatin. It can read data from JSON, write data , update existing data, deleting data."
    
    def __repr__(self):
        return "ProductManipulation(products_json_file_path, general_info_json_file_path)"


def start_wroking_on_database(products_data_json_file, general_store_info_json_file, see=False, add=False, update=False, delete=False):
    # initialize an instance named 'administer'
    administer = ProductManipulation(products_data_json_file, general_store_info_json_file)
    # Calling dependencies function for ready to work 
    administer.products_dict = administer.read_product_data(administer.products_data_json_file_name)
    administer.product_table_format(administer.products_dict)
    administer.read_general_info(administer.general_info_file_name)
    availabel_ids, unavailabel_ids, blank_slots_ids = administer.segment_product_ids_by_characteristics(administer.products_dict)    
    
    # Calling functions according to conditions
    if see:
        # For Showing
        administer.show_products_by_mode(administer.all_ids, availabel_ids, unavailabel_ids, administer.products_dict)

    if add:
        # For Adding
        add_response = administer.add_products(administer.products_dict)
        print("Add Response --> ", add_response)
    
    if update:
        # For Updating 
        update_response = administer.update_attribute(administer.all_ids, administer.products_data_json_file_name, administer.products_dict)
        print("Update Response --> ", update_response)
    
    if delete:
        # For Deleting 
        delete_response = administer._remove_one_product(administer.products_dict)
        print("Delete Response --> ", delete_response)

