import re

CREDIT_CARD_PATTERN = r"""
\d{4}-\d{4}-\d{4}-(?P<card_last4>\d{4})
"""

CREDIT_CARD_REGEX = re.compile(
    CREDIT_CARD_PATTERN,
    re.VERBOSE,
)

EMAIL_PATTERN = r"""
(?P<email_user>
    [A-Za-z0-9._%+\-]+
)
(?P<email_at>\\?@)
(?P<email_domain>
    [A-Za-z0-9-]+
    (?:\.[A-Za-z0-9-]+)*
    \.(?:(?!(?:DOB:|Address:|\d{3}-\d{3}-\d{4}|\d{4}-\d{4}-\d{4}-\d{4}))[A-Za-z]){2,}
)
"""
EMAIL_REGEX = re.compile(
    EMAIL_PATTERN,
    re.VERBOSE,
)

PHONE_NUMBER_PATTERN = r"""
\d{3}-\d{3}-(?P<phone_last4>\d{4})
"""

PHONE_NUMBER_REGEX = re.compile(
    PHONE_NUMBER_PATTERN,
    re.VERBOSE,
)

DOB_PATTERN = r"""
DOB:
(?P<dob_day>\d{2})
/
(?P<dob_month>\d{2})
/
(?P<dob_year>\d{4})
"""

DOB_REGEX = re.compile(
    DOB_PATTERN,
    re.VERBOSE,
)

ADDRESS_PATTERN = r"""
(?P<address_prefix>
    Address:[ \t]*
)

(?P<house_number>
    \d+
    (?:[/-]\d+)*
)

[ \t]+

(?P<address_body>
    .*?
    (?:
        ซอย
        [^,\r\n]*?
        [ \t]+
    )?

    ถนน
    [^,\r\n]*?
    [ \t]+
    
    (?:แขวง|ตำบล)
    [^,\r\n]*?
    [ \t]+

    (?:เขต|อำเภอ)
    [^,\r\n]*?
    [ \t]+

    (?:(?!Address:|DOB:|\d{3}-\d{3}-\d{4}|\d{4}-\d{4}-\d{4}-\d{4}|[A-Za-z0-9._%+\-]+@)[^,\r\n])+
)
"""
ADDRESS_REGEX = re.compile(
    ADDRESS_PATTERN,
    re.VERBOSE ,
)

MASTER_PATTERN = rf"""
(?P<ADDRESS>{ADDRESS_PATTERN})
|
(?P<DOB>{DOB_PATTERN})
|
(?P<PHONE>{PHONE_NUMBER_PATTERN})
|
(?P<CARD>{CREDIT_CARD_PATTERN})
|
(?P<EMAIL>{EMAIL_PATTERN})
"""

MASTER_REGEX = re.compile(MASTER_PATTERN, re.VERBOSE)

ALL_REGEXES = (
    CREDIT_CARD_REGEX,
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
    DOB_REGEX,
    ADDRESS_REGEX,
)

