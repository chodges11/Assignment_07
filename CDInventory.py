# ------------------------------------------#
# Title: CDInventory.py
# Desc: Working with Exception Handling, pickling, and shelves.
# Change Log: (Who, When, What)
# Charles Hodges(hodges11@uw.edu), 2021-Aug-22, Created File
# ------------------------------------------#

import pickle

# Variables
dic_row = {}  # dictionary data row
lst_input_options = ['l', 'a', 'i', 'd', 's', 'x']
lst_tbl = []  # list of lists to hold data
obj_file = None  # file object

# Strings
str_cancelling_reload = (
    'Canceling...\n'
    'Inventory data NOT reloaded.\n'
    'Press [ENTER] to continue to the menu.\n'
    )
str_cd_removed = 'The CD was removed.'
str_choice = ''  # User input
str_confirm_reload = (
    'Type \'yes\' to continue and reload from the file. '
    'Otherwise, the reload will be canceled. --> '
    )
str_file_name = 'CDInventory.dat'  # The data storage file
str_footer = '======================================'
str_general_error = '!General Error!'
str_header = '\n======= The Current Inventory: ======='
str_inventory_not_saved = (
    'The inventory was NOT saved to file. Press [ENTER] to return to the menu.'
    )
str_menu = (
    '\n'
    'MENU\n\n'
    '[l] Load Inventory from file\n'
    '[a] Add CD\n'
    '[i] Display Current Inventory\n'
    '[d] Delete CD from Inventory\n'
    '[s] Save Inventory to file\n'
    '[x] Exit\n'
    )
str_not_find_cd = 'Could not find this CD!'
str_reloading = 'reloading...'
str_save_inventory = (
    "Save this inventory to file? Must type 'yes' to confirm: "
    )
str_sub_header = 'ID\tCD Title \t(by: Artist)\n'
str_what_artist = 'What is the Artist\'s name? '
str_what_id = 'Enter ID: '
str_what_title = 'What is the CD\'s title? '
str_which_delete = 'Which CD would you like to delete? Please use ID: '
str_which_operation = (
    'Which operation would you like to perform?'
    '[l, a, i, d, s or x]: '
    )
str_warning = (
    'WARNING: If you continue, all unsaved data will be lost and the '
    'Inventory will be re-loaded from the file.'
    )
str_whole_num_error_msg = "Please only enter whole numbers."


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data in the table, before file interaction"""

    @staticmethod
    def add_cd(int_id_input, str_title_input,
               str_artist_input, dic_row, lst_tbl):
        """Function to manage data ingestion from User input of CD info.

        Accepts the User input of new CD information, and creates a dictionary
        object, which is appended to the list table which makes up the
        Inventory.

        Args:
            str_id_input (int): ID number of CD
            str_title_input (string): Title of CD
            str_artist_input (string): Name of CD's artist
            dic_row(dictionary): dictionary to store CD data
            lst_tbl(list): List of lists to hold data

        Returns:
            None.
        """
        dic_row = {
            'ID': int_id_input,
            'Title': str_title_input,
            'Artist': str_artist_input
            }
        lst_tbl.append(dic_row)
        IO.show_inventory(lst_tbl)

    @staticmethod
    def delete_cd(int_id_del, lst_tbl):
        """Function to delete a CD from the Inventory.

        When the User selects a CD to delete, by ID, that CD is deleted from
        the Inventory.

        Args:
            int_id_del(int) = ID value in an int, for identifying each CD
            lst_tbl(list): List of lists to hold data

        Returns:
            None.
        """
        # Search thru table and delete CD
        int_row_nr = -1
        bln_cd_removed = False
        for row in lst_tbl:
            int_row_nr += 1
            if row['ID'] == int_id_del:
                del lst_tbl[int_row_nr]
                bln_cd_removed = True
                break
        if bln_cd_removed:
            print(str_cd_removed)
        else:
            print(str_not_find_cd)
        # Display Inventory to user again
        IO.show_inventory(lst_tbl)


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(str_file_name, obj_file, lst_tbl, dic_row):
        """Function to manage data ingestion from file to a list of
           dictionaries.

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary
        row in table.

        Args:
            str_file_name(string): File name from which the data will be read
            obj_file(defaults to None): file object
            lst_tbl(list): List of lists to hold data
            dic_row(dictionary): dictionary data row

        Returns:
            lst_tbl(list): List of lists to hold data
        """
        # Clears existing data
        lst_tbl.clear()

        # Loads data from file
        obj_file = open(str_file_name, 'rb')
        try:
            lst_tbl = pickle.load(obj_file)
        except EOFError:
            pass
        obj_file.close()
        return lst_tbl

    @staticmethod
    def save_file(str_yes_no, str_file_name, obj_file, lst_tbl):
        """Function to save a file.

        After the User either confirms or declines saving this function
        processes the answer and either completes the objective to save, or
        returns the User back to the menu.

        Args:
            str_yes_no(string): User's response to save confirmation as a y/n
            str_file_name(string): File name where the data will be saved
            obj_file(defaults to None): file object
            lst_tbl(list): List of lists to hold data

        Returns:
            None.
        """
        # Process choice
        if str_yes_no == 'yes':
            # Save data
            obj_file = open(str_file_name, 'wb')
            pickle.dump(lst_tbl, obj_file)
            obj_file.close()
        else:
            input(str_inventory_not_saved)

    @staticmethod
    def create_file(str_file_name, obj_file):
        """Function to create a binary file.

        Args:
            str_file_name(string): File name where the data will be saved
            obj_file(defaults to None): file object

        Returns:
            None.
        """
        # Create file
        obj_file = open(str_file_name, 'ab')
        obj_file.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print(str_menu)

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the
            choices: l, a, i, d, s or x
        """
        choice = ' '
        while choice not in lst_input_options:
            choice = input(str_which_operation).lower().strip()
        print()  # Add extra line for layout
        return choice

    @staticmethod
    def show_inventory(lst_tbl):
        """Displays current inventory table

        Args:
            lst_tbl(list): List of lists to hold data

        Returns:
            None.

        """
        print(str_header)
        print(str_sub_header)
        for row in lst_tbl:
            print('{}\t{} \t\t(by:{})'.format(*row.values()))
        print(str_footer)

    @staticmethod
    def input_cd_info():
        """Requests and receives CD information from the User.

        Args:
            None.

        Returns:
            int_id_input(int): ID Number
            str_title_input(string): CD Title
            str_artist_input(string): Artist Name
        """
        while True:
            try:
                int_id_input = int(input(str_what_id).strip())
                break
            except ValueError:
                print(str_whole_num_error_msg)
        str_title_input = input(str_what_title).strip()
        str_artist_input = input(str_what_artist).strip()
        return int_id_input, str_title_input, str_artist_input

    @staticmethod
    def ask_to_save(str_file_name, obj_file):
        """Function to ask a User if they really want to save a file.

        This function accepts the User's y/n response, and passes it to
        a function in the FileProcessor Class, to evaluate the answer,
        and complete the User's stated objective.'

        Args:
            str_file_name(string): File name where the data will be saved

        Returns:
            None.
        """
        # Display current inventory and ask user for confirmation to save
        IO.show_inventory(lst_tbl)
        str_yes_no = input(str_save_inventory).strip().lower()
        FileProcessor.save_file(str_yes_no, str_file_name, obj_file, lst_tbl)

    @staticmethod
    def ask_to_delete():
        """Function to identify a CD to delete from the Inventory.

        User selects a CD to delete, by ID, that CD will be deleted from
        the Inventory.

        Args:
            None.

        Returns:
            None.
        """
        # Display Inventory to user
        IO.show_inventory(lst_tbl)
        # Ask user which ID to remove
        while True:
            try:
                int_id_del = int(input(str_which_delete).strip())
                break
            except ValueError:
                print(str_whole_num_error_msg)
        DataProcessor.delete_cd(int_id_del, lst_tbl)

    @staticmethod
    def ask_load_file(obj_file, lst_tbl, dic_row):
        """Function to confirm loading from the file, with the User.

        Handles the verification that the User wants to load the Inventory
        from a file, which will delete the surrent unsaved Inventory.

        Args:
            obj_file(defaults to None): file object
            lst_tbl(list): List of lists to hold data
            dic_row(dictionary): dictionary data row

        Returns:
            None.
        """
        print(str_warning)
        str_yes_no = input(str_confirm_reload)
        if str_yes_no.lower() == 'yes':
            print(str_reloading)
            lst_tbl = FileProcessor.read_file(
                str_file_name, obj_file, lst_tbl, dic_row)
            IO.show_inventory(lst_tbl)
        else:
            input(str_cancelling_reload)


# When program starts, read in the currently saved Inventory, if it exists.
# Otherwise, create the inventory file.
try:
    lst_tbl = FileProcessor.read_file(
        str_file_name, obj_file, lst_tbl, dic_row)
except FileNotFoundError:
    FileProcessor.create_file(str_file_name, obj_file)

# Start main loop
while True:
    # Display Menu to user, and get choice
    IO.print_menu()
    str_choice = IO.menu_choice()

    # Exit
    if str_choice == 'x':
        break

    # Load Inventory.
    if str_choice == 'l':
        IO.ask_load_file(obj_file, lst_tbl, dic_row)
        continue  # start loop back at top.

    # Add a CD.
    elif str_choice == 'a':
        # Ask user for new ID, CD Title and Artist,
        int_id_input, str_title_input, str_artist_input = IO.input_cd_info()
        # Add CD information to the Inventory
        DataProcessor.add_cd(
                             int_id_input,
                             str_title_input,
                             str_artist_input,
                             dic_row,
                             lst_tbl
                             )
        continue  # start loop back at top.

    # Display current inventory.
    elif str_choice == 'i':
        IO.show_inventory(lst_tbl)
        continue  # start loop back at top.

    # Delete a CD.
    elif str_choice == 'd':
        IO.ask_to_delete()
        continue  # start loop back at top.

    # Save inventory to file.
    elif str_choice == 's':
        IO.ask_to_save(str_file_name, obj_file)
        continue  # start loop back at top.

    # A catch-all, which should not be possible, as user choice gets
    # vetted in IO, but to be safe.
    else:
        print(str_general_error)
