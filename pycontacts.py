import sqlite3
import os

def clear_terminal():
    """
    Clears the terminal depending on what OS the user is running.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def wait_for_input():
    """
    Waits for the user to press enter.
    """
    print("Press [Enter] to continue...") 
    input()
    
    

def add_new_contact():
    """
    Allows the user to create a new contact.
    """
    contact = {"firstname": "", "lastname": "", "phone_number": "",
               "email_address": "", "address": "", "birthday": ""}
    contact = add_info(contact, "firstname")
    contact = add_info(contact, "lastname")
    contact = add_info(contact, "phone_number")
    contact = add_info(contact, "email_address")
    contact = add_info(contact, "address")
    contact = add_info(contact, "birthday")
    
    clear_terminal()
    print("Add a new contact\n")
    print("Firstname: ", contact["firstname"], "\nLastname: ", contact["lastname"],  
          "\nPhone number: ", contact["phone_number"], "\nEmail: ", 
          contact["email_address"], "\nAddress: ", contact["address"], 
          "\nBirthday: ", contact["birthday"], "\n\n")
    
    # Opens a connexion to the database.
    connexion = sqlite3.connect("contacts.db")
    cur = connexion.cursor()
    
    # Creates the query and executes it.
    query = "INSERT INTO Contact (firstname, lastname, phone_number, \
            email_address, address, birthday) VALUES (:firstname, :lastname, \
            :phone_number, :email_address, :address, :birthday);"
    cur.execute(query, contact)
    connexion.commit()
    connexion.close()
    print("Contact added successfully!", end=" ")
    wait_for_input()
    
def add_info(info, query):
    """
    Asks the required information to the user and adds it to the contact.

    Args:
        info (array): the conact's information.
        query (str): the required information.

    Returns:
        array: the updated contact's information.
    """
    clear_terminal()
    print("Add a new contact\n")
    print("Firstname: ", info["firstname"], "\nLastname: ", info["lastname"],  
          "\nPhone number: ", info["phone_number"], "\nEmail: ", info["email_address"], 
          "\nAddress: ", info["address"], "\nBirthday: ", info["birthday"], "\n")
    info[query] = input("Enter the " + query.replace("_", " ") + ": ")
    return info

# Display method
def display_contact():
    """
    Displays the contacts with the same firstname as the one entered by the user.
    """
    clear_terminal()
    wanted_firstname = input("Enter the firstname of the contact you want to display: ")
    
    clear_terminal()
    print("Contacts with the firstname " + wanted_firstname + ":\n")
    connexion = sqlite3.connect("contacts.db")
    cur = connexion.cursor()
    for contact in cur.execute("SELECT * FROM Contact WHERE firstname = ?;", (wanted_firstname,)):
        print("\tFirstname: ", contact[1], "\n\tLastname: ", contact[2],  
          "\n\tPhone number: ", contact[3], "\n\tEmail: ", contact[4], 
          "\n\tAddress: ", contact[5], "\n\tBirthday: ", contact[6], "\n")
    connexion.close()
    wait_for_input()
    

# Display for a precise letter method
def display_all_contacts():
    """
    Displays all the contacts present in the database.
    """
    clear_terminal()
    print("Your contacts:\n")
    
    connexion = sqlite3.connect("contacts.db")
    cur = connexion.cursor()
    for contact in cur.execute("SELECT * FROM Contact;"):
        print("\tFirstname: ", contact[1], "\n\tLastname: ", contact[2],  
          "\n\tPhone number: ", contact[3], "\n\tEmail: ", contact[4], 
          "\n\tAddress: ", contact[5], "\n\tBirthday: ", contact[6], "\n")
    connexion.close()
    wait_for_input()

# Delete a contact method
def delete_contact():
    """
    Displays the contact with the same firstname as the one entered by the user.
    """
    clear_terminal()
    wanted_firstname = input("Enter the firstname of the contact you want to delete: ")
    
    clear_terminal()
    connexion = sqlite3.connect("contacts.db")
    cur = connexion.cursor()
    contacts = cur.execute("SELECT * FROM Contact WHERE firstname = ?;", (wanted_firstname,)).fetchall()
    
    if len(contacts) == 0:
        print("No contact with the firstname " + wanted_firstname + " was found.", end=" ")
    elif len(contacts) == 1:
        cur.execute("DELETE FROM Contact WHERE firstname = ?;", (wanted_firstname,))
        connexion.commit()
        print("The contact with the firstname \"" + wanted_firstname + "\" has been deleted.", end=" ")
    else :
        print("Multiple contacts with the firstname " + wanted_firstname + " were found:\n")
        for i in range(len(contacts)):
            print("\t" + str(i) + ". " + contacts[i][1] + " | " + contacts[i][2] +
                    " | " + contacts[i][3] + " | " + contacts[i][4] + " | " + 
                    contacts[i][5] + " | " + contacts[i][6] + "\n")
        
        choice = input("Enter the number of the contact you want to delete: ")
        while not choice.isdigit() or int(choice) < 0 or int(choice) >= len(contacts):
            print("Please enter a valid choice.")
        
        cur.execute("DELETE FROM Contact WHERE id = ?;", contacts[int(choice)][0])
        connexion.commit()
        
        #FIXME ValueError: parameters are of unsupported type
        
        print("The contact " + choice + " has been deleted.", end=" ")
            
    connexion.close()
    wait_for_input()
    

# Delete all conctacts method
def delete_all_contacts():
    """
    Deletes all the contacts in the database.
    """
    clear_terminal()
    choice = input("Are you sure you want to delete all your contacts? (y/n) ")
    while choice.upper() not in ["Y", "N"]:
        choice = input("Please enter a valid choice (y/n) ")
    if choice.upper() == "Y":
        # Connects to the database and deletes all the contacts.
        con = sqlite3.connect("contacts.db")
        cur = con.cursor()
        cur.execute("DELETE FROM Contact;")
        con.commit()
        con.close()
    print("All your contacts have been deleted.", end=" ")
    wait_for_input()

# Exit method
def exit_program():
    """
    Displays a goodbye message and exits the program.
    """
    print("See you soon!")
    exit()

def choice_manager(choice):
    """
    Calls the right function given the user's choice.

    Args:
        choice (str): the user's choice
    """
    match choice:
        case "1":
            add_new_contact()
        case "2":
            display_contact()
        case "3":
            display_all_contacts()
        case "4":
            delete_contact()
        case "5":
            delete_all_contacts()
        case "6":
            exit_program()

def main_menu():
    while True:
        clear_terminal()
        print("Welcome to PyContacts!\n\n")
        print("1. Add a new contact")
        print("2. Display a contact")
        print("3. Display all contacts")
        print("4. Delete a contact")
        print("5. Reset your contacts")
        print("6. Exit")
        choice = input("\nWhat do you wish to do? ")
        
        while choice not in ["1","2","3","4","5","6"]:
            choice = input("Please, choose a correct number (1,2,3,4,5 or 6): ")
    
        choice_manager(choice)

if __name__ == "__main__":
    main_menu()
    

    
    