from Flags_and_Format_for_table import flag_unexpected, flag_wrong
from General_Product_task import GeneralProductTask
import json
from time import strftime as time_strftime

class ProductOrderManager(GeneralProductTask):
    def __init__(self, products_json_file_path, general_info_json_file):
        # Calling parent class '__init__' for initialize instance variables
        super().__init__()
        # Attributes for Products database
        self.products_json_file_path = products_json_file_path
        self.org_products_data = dict()
        self.temp_products_file_name = "temp_products.json"
        self.temp_products_data = dict()
        self._store_general_info_file_name = general_info_json_file


    def update_total_issued_slip_no(self, general_info_txt_file_name: str, no_of_new_issued_purchase_slip: int):
        '''
        Increment the number of issued purchase slips in the general info JSON file.

        Args:
            general_info_txt_file_name (str): The path to the general info JSON file.
            no_of_new_issued_purchase_slip (int): The number of new purchase slips (usually one).

        Updates:
            _store_total_purchase_slip_issued_no (int): The total number of purchase slips issued.

        Note:
            This method updates the `_store_total_purchase_slip_issued_no` attribute to keep track
            of the total number of purchase slips issued without the need to read the file again.
        '''
        self._store_general_info["total_purchase_slip_issued_no"] += no_of_new_issued_purchase_slip
        with open(general_info_txt_file_name, "w") as _general_info_writer:
            # Update the dictionary that will be written to the file
            json.dump(self._store_general_info, _general_info_writer, indent=4)

        # Update the attribute to keep using it without needing to read the file again
        self._store_total_purchase_slip_issued_no += no_of_new_issued_purchase_slip

    
    def show_products_table(self, temp_products_data):
        '''
        Display the updated product data in a formatted table.

        Args:
            temp_products_data (dict): A dictionary containing updated product data.
                Each key represents a product ID, and the corresponding value is a dictionary
                containing product information.

        Returns:
            A list of product IDs that are displayed in the table (used for order placement).
        '''
        # Update ids attribute and show only availabel products
        availabael_ids_index_0 = self.segment_product_ids_by_characteristics(temp_products_data)
        formatted_rows = self.generate_formatted_product_rows(availabael_ids_index_0[0], temp_products_data)
        self.print_formatted_product_rows_with_store_and_table_header(formatted_rows)
        return availabael_ids_index_0[0]


    def take_order(self, displayed_product_ids):
        '''
        Facilitates the process of placing an order for products.

        Args:
            displayed_product_ids (list): A list of product IDs that are currently displayed and available for purchase.

        Returns:
            list: A list containing tuples, each tuple representing a product ID and the quantity ordered.
                Example: [(product_id_1, quantity_1), (product_id_2, quantity_2), ...]
        '''
        # Display guidance for purchasing products
        guidance = """
Guidance for Purchasing Product :)
    >> First Enter Product ID and then enter available quantity you want to purchase.
    >> Keep in mind if you enter invalid input so it will ask you again.
    >> Enter 'OK' if you want to complete your order to get your purchase slip.
    >> Enter 'q' if you want to dismiss all things and the program will stop.
    >> Enter 'show' to view Product Table again.
        *Note: When you enter 'show', you will see an updated product table.
    >> Enter 'g' for viewing this guide again.
        """
        print(guidance)

        # List to store tuples containing product ID and quantity
        self.ordered_products_id_and_quantity = []

        # Infinite loop for keep asking until quit it
        while True:
            # Prompt user for input
            user_order = input("\nEnter here | Product ID | 'q' | 'g' | 'OK' | 'show' |: ")

            # Check user input is id(which ids that are displayed on table)
            if user_order in displayed_product_ids:
                # Extract product info
                choosed_product = self.temp_products_data[user_order]
                # Infinite loop until get right quantity or dismissed
                while True:
                    print("\nMinimum quantity is 1 and maximum is shown on the table")
                    
                    product_quantity = input(f"Enter 'no' to dismiss the product or enter the quantity of {choosed_product['name']} | {choosed_product['weight']} : ")

                    # Check if input is a number
                    if product_quantity.isdigit():
                        product_quantity = int(product_quantity)

                        # When user enter availabel quantity
                        if 0 < product_quantity <= choosed_product["quantity"]:
                            print("Your product is added. Product database is updated. Let's continue!")
                            self.ordered_products_id_and_quantity.append((user_order, product_quantity))
                            
                            # Update product data & attributes
                            self.update_product_data(self.temp_products_file_name, [user_order], [product_quantity])
                            
                            self.temp_products_data = self.read_product_data(self.temp_products_file_name)
                            
                            self.segment_product_ids_by_characteristics(self.temp_products_data)
                            break

                        print("Please enter a valid quantity. The minimum is 1 and the maximum is shown on the table. Or enter 'no' to dismiss the product.")
                    
                    # Dismiss product
                    elif product_quantity == "no":
                        print("\nProduct is dismissed.")
                        break

                    # Handle unexpected input
                    else:
                        print(f"{flag_unexpected} Please enter a quantity as a number or enter 'no' to dismiss this product.")

            # Show guidance again
            elif user_order == "g":
                print(guidance)

            # Create purchase slip
            elif user_order == "OK":
                # Check that user is really purchased something
                if self.ordered_products_id_and_quantity:
                    # Update original product data when the user confirms the purchase
                    self.update_total_issued_slip_no(self._store_general_info_file_name, 1)
                    
                    # Getting name before updating original data to prevent our database form EOF error
                    customer_name = input("Enter your name : ")
                    
                    self.create_purchase_slip(customer_name, self.products_json_file_path, self.ordered_products_id_and_quantity, self.temp_products_data)
                    break

                else:
                    print(f"{flag_unexpected} Wait, you not purchased anything \nFirst purchased somethings or if you want to quit, so you can enter 'q' to quit!")
                
            # Show product table again
            elif user_order == "show":
                displayed_product_ids = self.show_products_table(self.temp_products_data)

            # Quit
            elif user_order == "q":
                print("Thank you for using! :)")
                return "leaved"
        
            # Handle wrong inputs
            else:
                print(f"{flag_wrong} Please enter a valid input.")

        return self.ordered_products_id_and_quantity


    def update_product_data(self, products_json_file_path, product_id: list, product_quantity: list):
        '''
        Updates the quantity of chosen products in the product JSON file.

        Args:
            products_json_file_path (str): The file path to the product JSON file.
            product_id (str)/(list): The ID or list of IDs of the chosen product(s).
            product_quantity (list)/(int): The ordered quantity or list of quantities of the chosen product(s).
        '''
        
        # Loop through product IDs and quantities when multiple products
        for _id, quantity in zip(product_id, product_quantity):
            # Read the product JSON file 
            with open(products_json_file_path, "r") as products_database:
                product_dict_data = json.load(products_database)

            # Get the original value of the quantity
            quantity_attribute = product_dict_data[_id]["quantity"]
        
            # Update the quantity attribute by subtracting the ordered quantity from the original value
            product_dict_data[_id]["quantity"] = (quantity_attribute - quantity)

            # Write the updated data back to the file
            with open(products_json_file_path, "w") as data:
                # Update the data
                json.dump(product_dict_data, data, indent=4)


    def create_purchase_slip(self, customer_name_input, original_products_json_file_name, ordered_products_id_and_quantity, temp_product_dict):
        '''
        Create a Purchase slip (txt file)

        Args:
            original_products_json_file_name (str): Original file name to update original data because at this time user confirms purchase.
            ordered_products_id_and_quantity (list of tuple): User ordered purchased products ids and quantities in the format [(product_id, quantity), ..]
        '''
        # Update ids attributes
        self.segment_product_ids_by_characteristics(temp_product_dict)
        # Create Report.txt file
        self.report_product_out_of_stock(self.out_of_stock_products_ids, temp_product_dict)

        org_product_dict = self.read_product_data(original_products_json_file_name, temp_file=False)
        
        self.slip_name = self.for_purchase_slip_naming()

        with open(self.slip_name, "w") as slip:
            # Writing Header
            slip.write(self._store_header + "\n")
            
            # Date & Time
            date = time_strftime("%d-%b-%Y")
            waqt = time_strftime("%H:%M:%S")
            date_and_time = f"Date: {date}" + "".center(self.table_row_len - 31) + f"Time: {waqt}"
            
            slip.write(date_and_time + "\n")

            # Customer name
            slip.write(f"Customer: {customer_name_input}\n")

            # Line ~~~
            slip.write("".center(self.table_row_len, "~") + "\n") 

            # Product Table
            slip.write(self.table_header + "\n")
            slip.write(self.table_row_separator + "\n")

            self.total_price = list()
                
            # Writing products to slip
            for product_id, product_quantity in ordered_products_id_and_quantity:
                # Product ID attributes
                product_name = org_product_dict[product_id]["name"]
                product_brand = org_product_dict[product_id]["brand"]
                product_weight = org_product_dict[product_id]["weight"]
                product_price = org_product_dict[product_id]["price"]
                # Writing in file (formatted by function)
                units_x_price = product_quantity * product_price
                self.total_price.append(units_x_price)
                product_slip_row = self.show_product_row(product_id, product_name, product_brand, product_weight, product_price, product_quantity)
                
                slip.write(product_slip_row + "\n")

            # Line ---
            slip.write(self.table_row_separator + "\n")

            # Prices Summary
            discount_rate_and_price = self.get_rate_and_calculate_discount(sum(self.total_price))
            
            prices_summary = self.formatted_prices_row(sum(self.total_price), discount_rate_and_price[0], discount_rate_and_price[1], self.table_row_len)

            slip.write(prices_summary + "\n")

            # Line ---
            slip.write(self.table_row_separator + "\n")

            # Taxes and final price
            self.fbr_pos_charges_str = f"FBR POS CHARGES - {self._store_fbr_pos_charges}"

            self.invoice_value = discount_rate_and_price[1] + self._store_fbr_pos_charges
            self.invoice_value_str = f"Invoice value - {self.invoice_value}"

            slip.write(self.fbr_pos_charges_str + "".center(self.table_row_len  - (len(self.fbr_pos_charges_str) + len(self.invoice_value_str))) + self.invoice_value_str)

            # Line ___
            slip.write("\n" + "_" * self.table_row_len)

            # Contacts
            self.e_mail = "E-mail - SaadForContact@gmail.com"
            self.uan = "UAN - 021 111 446 248"
            contacts = "\n" + self.e_mail + "".center(self.table_row_len - (len(self.e_mail) + len(self.uan))) + self.uan

            slip.write(contacts + "\n")

            slip.write("{ Thank You & Come Again }".center(self.table_row_len, "~") + "\n")
            slip.write("XXX - XXX - XXX".center(self.table_row_len))  

        # Updating original database & Extracting ids and quantities from list for passing to function
        only_ids = [_id[0] for _id in ordered_products_id_and_quantity]
        only_quantities = [quantity[1] for quantity in ordered_products_id_and_quantity]
        self.update_product_data(original_products_json_file_name, only_ids, only_quantities)


    def report_product_out_of_stock(self, out_of_stock_ids: list, products_database):
        '''
        Creates a report file named 'Report.txt' containing products that are out of stock.

        Args:
            out_of_stock_products (list): A list of fully formatted products that were prepared for display in the table but are now out of stock.
        '''
        # Run when products out of stock
        if out_of_stock_ids:
            formatted_out_of_stock_rows = self.generate_formatted_product_rows(out_of_stock_ids, products_database)
            # Open the Report file
            with open("Report.txt", "w") as report:
                # Write store header
                report.write(self._store_header + "\n")
                # Write section header for out-of-stock products
                report.write(f"{' OUT OF STOCK PRODUCTS '.center(self.table_row_len, '|')}\n{self.table_header}\n{self.table_row_separator}")
                # Write each out-of-stock product to the report
                for out_of_stock_product in formatted_out_of_stock_rows:
                    report.write("\n" + out_of_stock_product)


    def get_rate_and_calculate_discount(self, total_price: int):
        '''
        Calculates the discount according to the total price.

        Minimum discount is 0.5%
        1000 - 1%
        3000 - 1.5%
        5000 - 2%
        10000 - 3%
        15000+ - 3.5%

        Args:
            total_price (int): The total price of all products that are purchased.

        Returns:
            tuple: A tuple containing the discount rate and the calculated discounted price.
                - discount_rate (float): The discount rate as a percentage.
                - calculated_discount (int): The discounted price after applying the discount.
        '''
        # Getting the discount rate
        discount_rate = int()
        if total_price < 1000:
            discount_rate = 0.5 
        elif total_price >= 1000 and total_price < 3000:
            discount_rate = 1
        elif total_price >= 3000 and total_price < 5000:
            discount_rate = 1.5
        elif total_price >= 5000 and total_price < 10000:
            discount_rate = 2
        elif total_price >= 10000 and total_price < 15000:
            discount_rate = 3
        else:
            discount_rate = 3.5

        # Calculating the discounted price
        discounted_price = total_price - (total_price * discount_rate/100)

        return (discount_rate, round(discounted_price))


    def formatted_prices_row(self, total_price, discount_rate, discounted_price, table_row_len):
        '''
        Generates a formatted row containing total price, discount rate, discounted price, and additional spaces for alignment.

        Args:
            total_price (int): The total price of all products that are purchased.
            discount_rate (float): The discount rate obtained from the get_rate_and_calculated_discount method.
            discounted_price (float): The discounted price obtained from the get_rate_and_calculated_discount method.
            table_row_len (int): The length of the table row in which the formatted string will be displayed.
        
        Returns:
            str: A formatted string containing the total price, discount rate, and discounted price, with additional spaces for alignment.
        '''
        total_str = f"TOTAL: {total_price}"
        discount_rate_str = f"Discount: {discount_rate}%"
        discounted_price_str = f"Net: {discounted_price}"

        # Calculate the spaces needed for alignment
        total_spaces = table_row_len - len(total_str) - len(discount_rate_str) - len(discounted_price_str)
        left_spaces = total_spaces // 2
        right_spaces = total_spaces - left_spaces

        # Construct the formatted string
        formatted_str = total_str + " " * left_spaces + discount_rate_str + " " * right_spaces + discounted_price_str

        return formatted_str


    def for_purchase_slip_naming(self):
        '''
        Generates a name for the purchase slip to prevent overwriting.

        Returns:
            str: The name of the purchase slip with a .txt extension.
        '''
        slip_name = f"Purchase Slip - {self._store_total_purchase_slip_issued_no}.txt"
        return slip_name    
   

    def __str__(self):
        return "This is an object used for order management. It can read product data from JSON files, show products to users, take orders, update product databases, create a report of out of product(if any) and create purchase slips for users."

    def __repr__(self):
        return "ProductOrderManager(products_json_file_path, general_info_json_file_path)"



def start_purchasing(products_data_json_file, general_store_info_json_file):
    # initialize an instance named 'user'
    user = ProductOrderManager(products_data_json_file, general_store_info_json_file)
    # Calling dependencies function for ready to work
    user.read_product_data(user.products_json_file_path, user.temp_products_file_name, temp_file=True)
    user.product_table_format(user.temp_products_data)
    user.read_general_info(user._store_general_info_file_name)

    # Showing product table & and taking order
    displayed_product_ids = user.show_products_table(user.temp_products_data)
    user_response = user.take_order(displayed_product_ids)
    
    # When user quit program
    if user_response == "leaved":
        return user_response

    # Finally showing purchase slip name to user, so user identify its slip 
    print(f"\nThank you! Your purchase slip is named '{user.slip_name}'.\n  *Note: This slip name will not be displayed again. \n")
   
    return "Order Completed!"
