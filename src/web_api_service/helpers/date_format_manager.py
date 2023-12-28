# importing datetime module
import datetime

# giving the date format
# DATE_FORMAT = '%d-%m-%Y'
DATE_FORMAT = "%d/%m/%Y"
# DATE_FORMAT = "%m/%d/%Y"


def date_formatter(**kwargs):
    """
    :param kwargs:
    :return:
    """
    pass


def find_date_format_using_excel(current_date):
    """this find_date_format_using_excel method get the date format
    for the Excel putting data
    :param current_date: input excel
    :return:
    """
    # using try-except blocks for handling the exceptions
    try:
        print("current_date---------", current_date)
        # formatting the date using strptime() function
        date_obj = datetime.datetime.strptime(str(current_date), DATE_FORMAT)
        return True if date_obj else None
    # If the date validation goes wrong
    except ValueError:

        # printing the appropriate text if ValueError occurs
        print("Incorrect data format, should be dd/mm/yyyy")
        return None
