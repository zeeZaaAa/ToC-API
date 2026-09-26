import re

from shared.masked_and_pattern.pattern import (
    CONCAT_CARD,
    CONCAT_DOB,
    CONCAT_EMAIL,
    CONCAT_PHONE,
    MASTER_REGEX,
)


def _preprocess_concatenated_fields(text: str) -> str:
    """
    Inserts spaces between ANY sensitive fields glued together without whitespace.
    """
    if not text:
        return text

    text = CONCAT_CARD.sub(' ', text)
    text = CONCAT_PHONE.sub(' ', text)
    text = CONCAT_DOB.sub(r'\1 ', text)
    text = CONCAT_EMAIL.sub(r'\1 ', text)

    return text


def mask_sensitive_data(text: str) -> str:
    """
    Scans text in a single pass to mask all sensitive fields simultaneously.
    """
    if not text:
        return text

    text = _preprocess_concatenated_fields(text)

    return MASTER_REGEX.sub(_mask_match, text)


def _mask_match(match: re.Match) -> str:
    group_type = match.lastgroup
    masked_val = ''

    if group_type == 'DOB':
        year_str = match.group('dob_year').zfill(4)
        masked_val = f'DOB:XX/XX/{year_str[:2]}XX'

    elif group_type == 'EMAIL':
        username = match.group('email_user')
        at_symbol = match.group('email_at')
        domain = match.group('email_domain')

        if len(username) <= 2:
            masked_val = f'{username}{at_symbol}{domain}'
        else:
            masked_username = username[0] + ('*' * (len(username) - 2)) + username[-1]
            masked_val = f'{masked_username}{at_symbol}{domain}'

    elif group_type == 'PHONE':
        masked_val = f'XXX-XXX-{match.group("phone_last4")}'

    elif group_type == 'CARD':
        masked_val = f'XXXX-XXXX-XXXX-{match.group("card_last4")}'

    elif group_type == 'ADDRESS':
        prefix = match.group('address_prefix')
        house_number = match.group('house_number')
        body = match.group('address_body')

        masked_house = ''.join('X' if char.isdigit() else char for char in house_number)
        masked_val = f'{prefix}{masked_house} {body}'

    else:
        return match.group(0)

    return f'<{group_type}>{masked_val}</{group_type}>'
