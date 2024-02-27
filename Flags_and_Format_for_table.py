
# Flags raise according to situation
flag_wrong = "\n" + "{ Wrong }".center(50, "~") + "\n"
flag_unexpected = "\n" + "( Unexpected )".center(50, "~") + "\n"

class FormatForTable():
    '''
    This is used for auto and proper alginment of table that will show to user for better experience
    '''
    def __init__(self):
        self.table_header = None
        self.table_id_margin = None 
        self.table_name_margin = None
        self.table_brand_margin = None
        self.table_weight_margin = None
        self.table_price_margin = None
        self.table_row_len = None
        self.table_row_separator = None

    def product_table_format(self, product_dict):
        '''
        Formats the product table for better readability and presentation.

        Args:
            product_dict (dict): A dictionary containing product data.

        Assign Instance Attributes:
            self.table_header (str): The formatted header for the product table.
            self.table_row_len (int): The length of the table header, used for formatting.
            self.table_row_separator (str): The separator line used to visually separate rows in the table.
            self.table_id_margin (int): The maximum length of the ID column.
            self.table_name_margin (int): The maximum length of the product name column.
            self.table_brand_margin (int): The maximum length of the brand column.
            self.table_weight_margin (int): The maximum length of the weight column.
            self.table_price_margin (int): The maximum length of the price column, ensuring it's at least 5 characters.

        Returns:
            None
        '''
        
        # Calculate the maximum length of strings in each column for proper alignment
        self.table_id_margin = max(len(product_id) for product_id in product_dict)
        self.table_name_margin = max(len(product_dict[product_id]["name"]) for product_id in product_dict)
        self.table_brand_margin = max(len(product_dict[product_id]["brand"]) for product_id in product_dict)
        self.table_weight_margin = max(len(product_dict[product_id]["weight"]) for product_id in product_dict)

        # Ensure that the price column is at least 5 characters long to prevent misalignment
        temp_table_price_margin = max(len(str(product_dict[product_id]["price"])) for product_id in product_dict) 
        self.table_price_margin = 5 if temp_table_price_margin < 5 else temp_table_price_margin 

        # Table Header 
        self.table_header = f'{"ID".ljust(self.table_id_margin)} | {"Product Name".ljust(self.table_name_margin)} | {"Brand".ljust(self.table_brand_margin)} | {"Weight".ljust(self.table_weight_margin)} | {"Price".ljust(self.table_price_margin)} | {"Quantity"}'.ljust(50)
        
        # Calculate the length of the header for formatting purposes
        self.table_row_len = len(self.table_header)
        
        # Create the separator line for the table
        self.table_row_separator = "".center(self.table_row_len, "-")

    
    def show_product_row(self, product_id, product_name, product_brand, product_weight, product_price, product_quantity):
        '''
        Formats a table row containing product information.

        Args:
            product_id (str): The ID of the product.
            product_name (str): The name of the product.
            product_brand (str): The brand of the product.
            product_weight (str): The weight of the product.
            product_price (float): The price of the product.
            product_quantity (int): The quantity of the product.

        Returns:
            str: The formatted table row.
        '''
        
        # Format the row with proper alignment and padding
        _row = f'{product_id.ljust(self.table_id_margin)} | {product_name.ljust(self.table_name_margin)} | {product_brand.ljust(self.table_brand_margin)} | {product_weight.ljust(self.table_weight_margin)} | {str(product_price).ljust(self.table_price_margin)} | {product_quantity}'.ljust(50)

        return _row
