from datetime import date

from shared.masked_and_pattern.pattern import (
    ADDRESS_REGEX,
    CREDIT_CARD_REGEX,
    DOB_REGEX,
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
)


def mask_credit_card(match):
    """
    1234-5678-9012-3456
    ->
    XXXX-XXXX-XXXX-3456
    """
    return f"XXXX-XXXX-XXXX-{match.group('last4')}"


def mask_email(match):
    """
    john.doe@example.com
    ->
    j******e@example.com

    a@example.com
    ->
    a@example.com

    ab@example.com
    ->
    ab@example.com
    """
    email = match.group(0)

    # Support both:
    #   user@example.com
    #   user\@example.com
    separator = r"\@" if r"\@" in email else "@"

    username, domain = email.split(separator, 1)

    # 1 or 2 characters -> nothing can be hidden while preserving
    # both first and last characters.
    if len(username) <= 2:
        return email

    masked_username = (
        username[0]
        + ("*" * (len(username) - 2))
        + username[-1]
    )

    return f"{masked_username}{separator}{domain}"


def mask_phone_number(match):
    """
    093-245-7894
    ->
    XXX-XXX-7894
    """
    return f"XXX-XXX-{match.group('last4')}"


def mask_dob(match):
    """
    DOB:25/12/2549
    ->
    DOB:XX/XX/25XX

    Invalid dates are left untouched.
    """

    day = int(match.group("day"))
    month = int(match.group("month"))
    year = int(match.group("year"))

    try:
        date(year, month, day)
    except ValueError:
        return match.group(0)

    return f"DOB:XX/XX/{str(year)[:2]}XX"


def mask_address(match):
    """
    Address: 689 ...
    ->
    Address: XXX ...

    Address: 12/34 ...
    ->
    Address: XX/XX ...

    Address: 123-125 ...
    ->
    Address: XXX-XXX ...
    """

    prefix = match.group("prefix")
    house_number = match.group("house_number")

    masked_house_number = "".join(
        "X" if char.isdigit() else char
        for char in house_number
    )

    return f"{prefix}{masked_house_number}"


def mask_sensitive_data(text: str) -> str:
    """
    Scan arbitrary text and mask every supported sensitive value.

    Supports:
        - multiple emails
        - multiple credit cards
        - multiple phone numbers
        - multiple DOBs
        - multiple addresses
        - mixed values
        - values touching each other with no spaces
    """

    if not text:
        return text

    # Each regex only modifies its own type, so applying them sequentially
    # does not prevent another type from being detected later.
    text = CREDIT_CARD_REGEX.sub(mask_credit_card, text)
    text = EMAIL_REGEX.sub(mask_email, text)
    text = PHONE_NUMBER_REGEX.sub(mask_phone_number, text)
    text = DOB_REGEX.sub(mask_dob, text)
    text = ADDRESS_REGEX.sub(mask_address, text)

    return text