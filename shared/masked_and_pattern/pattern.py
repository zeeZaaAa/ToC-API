import re

# ---------------------------------------------------------------------------
# Credit card
# Required format:
#     1234-5678-9012-3456
#
# Must not match:
#     1234567890123456
#     1234 5678 9012 3456
# ---------------------------------------------------------------------------

CREDIT_CARD_PATTERN = r"""
(?<!\d)
\d{4}-\d{4}-\d{4}-(?P<last4>\d{4})
(?!\d)
"""

CREDIT_CARD_REGEX = re.compile(
    CREDIT_CARD_PATTERN,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# Email
#
# Supports:
#     john@example.com
#     john.doe+test@example.co.th
#
# Also supports a literal '\@' because your example included:
#     adder\@gmail.com
#
# One/two-character usernames are considered valid and remain unchanged
# because both first and last characters must be preserved.
# ---------------------------------------------------------------------------

EMAIL_PATTERN = r"""
(?<![A-Za-z0-9._%+\-])
[A-Za-z0-9]
[A-Za-z0-9._%+\-]*
\\?@
[A-Za-z0-9]
[A-Za-z0-9.-]*
\.[A-Za-z]{2,}
(?![A-Za-z0-9._%+\-])
"""

EMAIL_REGEX = re.compile(
    EMAIL_PATTERN,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# Phone number
# Required format:
#     093-245-7894
#
# Must not match:
#     0932457894
#     093 245 7894
# ---------------------------------------------------------------------------

PHONE_NUMBER_PATTERN = r"""
(?<!\d)
\d{3}-\d{3}-(?P<last4>\d{4})
(?!\d)
"""

PHONE_NUMBER_REGEX = re.compile(
    PHONE_NUMBER_PATTERN,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# DOB
# Required format:
#     DOB:25/12/2549
#
# Regex validates the shape.
# Actual calendar validity is checked separately in mask_dob().
# Buddhist year must be 25xx.
# ---------------------------------------------------------------------------

DOB_PATTERN = r"""
(?<![A-Za-z0-9])
DOB:
(?P<day>0[1-9]|[12]\d|3[01])
/
(?P<month>0[1-9]|1[0-2])
/
(?P<year>25\d{2})
(?!\d)
"""

DOB_REGEX = re.compile(
    DOB_PATTERN,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# Address
#
# The address requirement is intentionally split into:
#
#   1. Detect "Address:"
#   2. Detect the house number immediately after it
#
# We do NOT make the entire address one giant regex because your input may
# contain other sensitive data inside the address text:
#
# Address: 689 ซอยลำดกระบัง adder@gmail.com 19 ถนนลำดกระบัง ...
#
# In that case the email must still be independently detected and masked.
#
# Supported house numbers:
#     99
#     689
#     12/34
#     123-125
# ---------------------------------------------------------------------------

ADDRESS_PATTERN = r"""
(?P<prefix>
    \bAddress:
    [ \t]*
)
(?P<house_number>
    \d+
    (?:[/-]\d+)?
)
(?=[ \t]|,|$)
"""

ADDRESS_REGEX = re.compile(
    ADDRESS_PATTERN,
    re.VERBOSE | re.IGNORECASE,
)


ALL_REGEXES = (
    CREDIT_CARD_REGEX,
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
    DOB_REGEX,
    ADDRESS_REGEX,
)
