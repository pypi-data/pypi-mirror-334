import re

# from https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document :
#regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

# from https://developers.google.com/edu/python/regular-expressions
regex = re.compile(r'[\w\.-]+@[\w\.-]+')

def get_email_addresses(text: str) -> str:
    """Receives a string and returns a unique list of email addresses found within that string."""
    match = re.findall(regex, text)

    unique = [*set(match)]

    return(unique)