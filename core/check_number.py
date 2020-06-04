import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

def check_no(number):
    value = False
    try:
        value = carrier._is_mobile(number_type(phonenumbers.parse(number)))
    except:
        value = False
    finally:
        return(value)
