import re

CREDIT_CARD_PATTERN = (
	r'^([0-9]{4}-[0-9]{4}-[0-9]{4}-)'
	r'([0-9]{4})$'
)

EMAIL_PATTERN = (
	r'^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*'
	r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

PHONE_NUMBER_PATTERN = (
	r'^([0-9]{3}-[0-9]{3}-)'
	r'([0-9]{4})$'
)

DOB_PATTERN = (
	r'^DOB:(0[1-9]|[12][0-9]|3[01])'
	r'/(0[1-9]|1[0-2])'
	r'(/(?!0000)[0-9]{2})([0-9]{2})$'
)

ADDRESS_PATTERN = (
    r'^Address:\s*'
    r'\d+(?:/\d+)?\s+'
    r'(?:ซอย.+?\s+)?'
    r'ถนน.+?\s+'
    r'(?:แขวง|ตำบล).+?\s+'
    r'(?:เขต|อำเภอ).+?\s+'
    r'.+$'
)

CREDIT_CARD_REGEX = re.compile(CREDIT_CARD_PATTERN)
EMAIL_REGEX = re.compile(EMAIL_PATTERN)
PHONE_NUMBER_REGEX = re.compile(PHONE_NUMBER_PATTERN)
DOB_REGEX = re.compile(DOB_PATTERN)
ADDRESS_REGEX = re.compile(ADDRESS_PATTERN)
