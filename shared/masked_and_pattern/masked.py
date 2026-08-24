from shared.masked_and_pattern.pattern import (
    ADDRESS_REGEX,
    CREDIT_CARD_REGEX,
    DOB_REGEX,
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
)


def mask_credit_card(credit_card):
    if not (CREDIT_CARD_REGEX.fullmatch(credit_card)):
        return 'ERROR'
    masked_credit_card = CREDIT_CARD_REGEX.sub(r'XXXX-XXXX-XXXX-\g<2>', credit_card)
    return masked_credit_card


def mask_email(email):
    if not (EMAIL_REGEX.fullmatch(email)):
        return 'ERROR'
    username, domain = email.split('@', 1)
    if len(username) <= 2:
        masked_user = username[0] + '*'
    else:
        masked_user = username[0] + ('*' * (len(username) - 2)) + username[-1]
    masked_email = masked_user + '@' + domain
    return masked_email


def mask_phone_number(phone_number):
    if not (PHONE_NUMBER_REGEX.fullmatch(phone_number)):
        return 'ERROR'
    masked_phone_number = PHONE_NUMBER_REGEX.sub(r'XXX-XXX-\g<2>', phone_number)
    return masked_phone_number


def mask_dob(dob):
    if not (DOB_REGEX.fullmatch(dob)):
        return 'ERROR'
    masked_dob = DOB_REGEX.sub(r'XX/XX\g<3>XX', dob)
    return masked_dob


def mask_address(address):
    if not (ADDRESS_REGEX.fullmatch(address)):
        return 'ERROR'
    house_number = len(ADDRESS_REGEX.match(address).group(2))
    sensor = '*' * house_number
    masked_address = ADDRESS_REGEX.sub(rf'\g<1>{sensor}\g<3>', address)
    return masked_address
