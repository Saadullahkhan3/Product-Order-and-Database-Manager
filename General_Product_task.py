from Flags_and_Format_for_table import FormatForTable
import json
import os   # use for checking json file size if size is 0 so write default data in it

class GeneralProductTask(FormatForTable):
    '''
    This class is derived from 'FormatForTable'.
    This class will be used for product general tasks such as reading(product database/general info), segment product ids, generating formatted rows for table(alignments get by 'FormatForTable'), etc
    '''
    def __init__(self):
        # Calling parent class '__init__' for initialize instance variables
        super().__init__()
        # Attributes for ids
        self.all_ids = list()
        self.blank_slot_ids = list()
        self.available_products_ids = list()
        self.out_of_stock_products_ids = list()
        # Attribute for Store 
        self._store_general_info = dict()
        self._store_header = str()
        self._store_name = str()
        self._store_location = str()
        self._store_e_mail = str()
        self._store_uan = str()
        self._store_total_purchase_slip_issued_no = int()
        self._store_fbr_pos_charges = int()


    def read_general_info(self, general_info_json_file_name):
        '''
        Read general info JSON file containing store information and assign object variables.

        Args:
            general_info_json_file_name (str): The path to the JSON file containing general store information.

        Instance Attributes:
            _store_header (str): A formatted header containing store name and location.
            _store_general_info (dict): The entire general information dictionary.
                Protected Variables:
                    _store_name (str): The name of the store.
                    _store_location (str): The location of the store.
                    _store_e_mail (str): The email of the store.
                    _store_uan (str): The UAN (Universal Access Number) of the store.
                    _store_total_purchase_slip_issued_no (int): The total number of purchase slips issued.
                    _store_fbr_pos_charges (int): The FBR (Federal Board of Revenue) tax for each issued slip.
        '''
        # Read and load existing data
        with open(general_info_json_file_name, "r") as _general_info_data:
            self._store_general_info = json.load(_general_info_data)

        # Extracting info and assign to instance variables
        self._store_name = self._store_general_info["store_name"]
        self._store_location = self._store_general_info["location"]
        self._store_e_mail = self._store_general_info["e_mail"]
        self._store_uan = self._store_general_info["uan"]
        self._store_total_purchase_slip_issued_no = self._store_general_info["total_purchase_slip_issued_no"]
        self._store_fbr_pos_charges = self._store_general_info["fbr_pos_charges"]

        # Format the store header with name and location
        self._store_header = f" {self._store_name} ".center(self.table_row_len, "|") + "\n" + f"[-{{ {self._store_location} }}-]".center(self.table_row_len)


    def read_product_data(self, products_json_file_name, temp_products_file_name=None, temp_file=False):
        '''
        Read JSON file containing product data and convert it into a dictionary.

        Args:
            products_json_file_name (str): The path to the JSON file containing product data.
            temp_file (bool, optional): Specifies whether to create a temporary copy of the original file.
                Default is False.
        
        Returns:
            dict: A dictionary containing product data.
                The keys are product IDs, and the values are dictionaries
                containing product information.

        Raises:
            FileNotFoundError: If the specified file is not found.
            JSONDecodeError: If there is an issue decoding JSON data in the file.
        '''
        try:
            # When file empty so write one blank slot to prevent error of --> json.load()         
            if os.path.getsize(products_json_file_name) == 0:
                # File is empty, write default data
                with open(products_json_file_name, "w") as file_writer:
                    default_data =  { "1":{
                            "name": "0000",
                            "brand": "",
                            "weight": "",
                            "price": 5,
                            "quantity": -1
                    }}
                    json.dump(default_data, file_writer, indent=4)
            
            with open(products_json_file_name, "r") as product_data:
                # Load product data from the JSON file
                product_database = json.load(product_data)
                
                # If temp_file is True, create a temporary copy of the original file
                if temp_file:
                    with open(temp_products_file_name, "w") as temp_file_writer:
                        json.dump(product_database, temp_file_writer, indent=4)
                    # Read the temporary file and return its data
                    with open("temp_products.json", "r") as temp_file_reader: 
                        self.temp_products_data = json.load(temp_file_reader)
                        return self.temp_products_data
                    
                # When no temporay file request so return the original product data dictionary
                return product_database

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{products_json_file_name}' not found.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Error: Unable to decode JSON data in '{products_json_file_name}'.")


    def sort_ids_and_remove_duplication(self, ids: list, all_ids=False, availabel_ids=False, out_of_stock_ids=False, blank_ids=False):
        '''
        To sort ids list because id is str so this function will sort them
        
        Args:
            ids (list of str): List of ids and ids will be str and numeric
            -> DEFAULT ARGS BUT ONE NECESSARY
            all_ids=False | availabel_ids=False | out_of_stock_ids=False | blank_ids=False

        Update:
            Update Instance variabel (get instance reference by argument)
        '''
        # Convert item(ids) in int and then is set() for remove duplication and then again in int and then sort them and again convert items(ids) in str
        int_ids = [int(_id) for _id in ids]
        remove_duplicate = set(int_ids)
        int_ids = list(remove_duplicate)
        int_ids.sort()
        str_ids = [str(_id) for _id in int_ids]
        
        # Assign sorted and non-duplicated list of ids to instance var(s) for ease of use
        if all_ids:
            self.all_ids = str_ids
        elif availabel_ids:
            self.available_products_ids = str_ids
        elif out_of_stock_ids:
            self.out_of_stock_products_ids = str_ids
        elif blank_ids:
            self.blank_slot_ids = str_ids
        # if even not default argument is given(True), then raise error for getting them
        else:
            raise "Defaul argument of sort_ids_and_remove_duplication() is required but only one"


    def segment_product_ids_by_characteristics(self, products_database: dict):
        '''
        Use for dividing product ids according to their conditions
        
        Args:
            products_database (dict): Products entire database for separating each id
        
        Instance variables:
            self.all_ids (list): List of all ids except their conditions
            self.availabel_ids (list): List of only available products ids
            self.out_of_stock_ids (list): List of only out of stock products ids
            self.blank_slots_ids (list): List of ids of deleted product(used for add new products in these slots(ids))
        '''
        self.all_ids = [_id for _id in products_database]
        # Clear all ids list each time to prevent same ids in multiple lists such as one availabel id in availabel list but it refresh and it out of stock so it also append in out of stock list 
        self.available_products_ids.clear()
        self.out_of_stock_products_ids.clear()
        self.blank_slot_ids.clear()

        for _id in self.all_ids:
            # For Blank Slots
            if products_database[_id]["name"] == "0000":
                self.blank_slot_ids.append(_id)
                self.sort_ids_and_remove_duplication(self.blank_slot_ids, blank_ids=True)
                continue

            # For Availabel Products
            if products_database[_id]["quantity"] >= 1:
                self.available_products_ids.append(_id)
                self.sort_ids_and_remove_duplication(self.available_products_ids, availabel_ids=True)
                continue    # Shift to next iterate

            # For Out Of Stock 
            self.out_of_stock_products_ids.append(_id)
            self.sort_ids_and_remove_duplication(self.out_of_stock_products_ids, out_of_stock_ids=True)
    
        return (self.available_products_ids, self.out_of_stock_products_ids, self.blank_slot_ids)


    def extract_one_product_attributes(self, one_product_id: str, product_dict: dict):
        '''
        Use for extracting attributes of product by id. Only appilicable for one product at a time but loop can be help in using it multiple item

        Args:
            one_product_id (str): ID of only one product
            product_dict (dict): Product database

        Returns:
            tuple of attribute where are product's --> (id, name, brand, weight, price, quantity)
        '''
        for _ in range(1):
            # Extract product attributes
            name = product_dict[one_product_id]["name"]
            brand = product_dict[one_product_id]["brand"]
            weight = product_dict[one_product_id]["weight"]
            price = product_dict[one_product_id]["price"]
            quantity = product_dict[one_product_id]["quantity"]

        return (one_product_id, name, brand, weight, price, quantity)


    def generate_formatted_product_rows(self, ids: list, products_database: dict):
        '''
        Use for generating formatted row of product's info for table

        Args:
            ids (list): List of those ids to get their formatted rows 
            products_database (dict): Product databse
        
        Returns:
            list of formatted rows(use loop to print them separately)
        '''
        formatted_rows = []
        for _id in ids:
            product_info = self.extract_one_product_attributes(_id, products_database)
            formatted_row = self.show_product_row(*product_info)    # * <- because there are tuple
            formatted_rows.append(formatted_row)
        return formatted_rows


    def print_formatted_product_rows_with_store_and_table_header(self, formatted_products_rows: list):
        '''
        Use for printing of formatted product rows with store header(store name,location) and table header

        Args:
            formatted_products_rows (list of str): A list of product with proper formatting and alignment 
        '''
        print("\n" + self._store_header)
        print(self.table_row_separator)
        print(self.table_header)
        print(self.table_row_separator)
        for product in formatted_products_rows:
            print(product)
        print(self.table_row_separator)
