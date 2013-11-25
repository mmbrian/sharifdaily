from django.contrib.auth.models import User
from django.db.models import Q
import re


MINIMUM_PASS_LENGTH = 6
REGEX_VALID_PASSWORD = (
	## Don't allow any spaces, e.g. '\t', '\n' or whitespace etc.
    r'^(?!.*[\s])'
    ## Check for a digit
    '((?=.*[\d])'
    ## Check for an uppercase letter
    '(?=.*[A-Z])'
    ## check for special characters. Something which is not word, digit or
    ## space will be treated as special character
    '(?=.*[^\w\d\s])).'
    ## Minimum 8 characters
    '{' + str(MINIMUM_PASS_LENGTH) + ',}$'
)

def validate_password(password):
    if re.match(REGEX_VALID_PASSWORD, password):
        return True
    return False

def username_present(username):
    if User.objects.filter(username=username).count():
        return True
    return False

def email_present(email):
    if User.objects.filter(email=email).count():
        return True
    return False

def user_present(username, email):
    return username_present(username) or email_present(email)
    # try:
    #     User.objects.get(Q(email=email) | Q(username=username))
    # except User.DoesNotExist:
    #     return False
    # return True

def diff(s1, s2):
    s1len, s2len = len(s1), len(s2)
    if s1len != s2len:
        return abs(s1len - s2len)
    else:
        return len(filter(lambda x:x[0]!=x[1], zip(s1, s2)))