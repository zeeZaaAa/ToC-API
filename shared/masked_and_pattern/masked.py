import re

from shared.masked_and_pattern.pattern import (
    MASTER_REGEX,
)


def mask_sensitive_data(text: str) -> str:
    """
    Scans text in a single pass to mask all sensitive fields simultaneously,
    preventing replacement outputs (e.g., 'X') from breaking adjacent matches.
    """
    if not text:
        return text

    return MASTER_REGEX.sub(_mask_match, text)

def _mask_match(match: re.Match) -> str:
    group_type = match.lastgroup

    if group_type == "DOB":
        year = int(match.group("dob_year"))
        return f"DOB:XX/XX/{str(year)[:2]}XX"

    elif group_type == "EMAIL":
        username = match.group("email_user")
        at_symbol = match.group("email_at")
        domain = match.group("email_domain")

        if len(username) <= 2:
            return f"{username}{at_symbol}{domain}"

        masked_username = username[0] + ("*" * (len(username) - 2)) + username[-1]
        return f"{masked_username}{at_symbol}{domain}"

    elif group_type == "PHONE":
        return f"XXX-XXX-{match.group('phone_last4')}"

    elif group_type == "CARD":
        return f"XXXX-XXXX-XXXX-{match.group('card_last4')}"

    elif group_type == "ADDRESS":
        prefix = match.group("address_prefix")
        house_number = match.group("house_number")
        body = match.group("address_body")

        masked_house = "".join("X" if char.isdigit() else char for char in house_number)
        return f"{prefix}{masked_house} {body}"

    return match.group(0)
