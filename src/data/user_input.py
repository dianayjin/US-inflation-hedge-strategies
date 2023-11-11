from datetime import datetime

def validate_date(input_date):
    """
    Validates if the given string is in the 'YYYY-MM-DD' format.

    args:
        input_date (str): date string to validate.

    returns:
        bool: True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(input_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def input_end(input_date):
    """
    Asks for a user input string and checks format.
    """
    start_date = datetime.strptime(input_date, '%Y-%m-%d')
    while True:
        user_date = input("Enter your analysis END date in YYYY-MM-DD format: ")
        if validate_date(user_date):
            end_date = datetime.strptime(user_date, '%Y-%m-%d')
            if end_date > start_date:
                check = input(f"Your input: {user_date}\nDoes this date look right to you? (y/n): ")

                if check.lower() != 'y':
                    retry = input("Would you like to retry? (y/n): ")
                    if retry.lower() != 'y':
                        print("Exiting the program.")
                        user_date = False
                        break
                else:
                    break
            else:
                retry = input("The date entered is not later than the start date. Would you like to retry? (y/n): ")
                if retry.lower() != 'y':
                    print("Exiting the program.")
                    user_date = False
                    break
        else:
            retry = input("Invalid date format. Would you like to retry? (y/n): ")
            if retry.lower() != 'y':
                print("Exiting the program.")
                user_date = False
                break
    return user_date
 
def input_start():
    """
    Asks for a user input string and checks format.
    """
    while True:
        user_date = input("Enter your analysis START date in YYYY-MM-DD format: ")
        if validate_date(user_date):
            check = input(f"Your input: {user_date}\nDoes this date look right to you? (y/n): ")

            if check.lower() != 'y':
                retry = input("Would you like to retry? (y/n): ")
                if retry.lower() != 'y':
                    print("Exiting the program.")
                    user_date = False
                    break
            else:
                break
        else:
            retry = input("Invalid date format. Would you like to retry? (y/n): ")
            if retry.lower() != 'y':
                print("Exiting the program.")
                user_date = False
                break
    return user_date

def input_tickers():
    """
    Asks for a user input string and converts it into a list of strings, using commas as the delimiter.
    """
    while True:
        user_input = input("Enter your list of tickers, separated by commas: ")
        ticker_list = user_input.split(',')
        ticker_list = [item.upper() for item in ticker_list]
        ticker_list = [item.strip() for item in ticker_list]
        check = input(f"Your input: {ticker_list}\nDoes this list look right to you? (y/n): ")

        if check.lower() == "y":
            print("Tickers sucessfully loaded.")
            break
        else:
            again = input("Do you want to try again? (y/n): ")

            if again == "Y" or again == "y":
                continue
            else:
                print("Exiting the program.")
                ticker_list=[]
                break
    
    return ticker_list

