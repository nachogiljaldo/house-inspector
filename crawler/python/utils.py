import re

non_decimal = re.compile(r'[^\d]+')

def only_digits(string_to_clean):
  return non_decimal.sub('', string_to_clean)

non_decimal_or_comma = re.compile(r'[^\d,]+')
def cleanup_number(number_to_cleanup):
  return non_decimal_or_comma.sub('', number_to_cleanup)

def int_or_none(value_to_parse):
  if value_to_parse:
    return int(value_to_parse)
  else:
    None

def float_or_none(value_to_parse):
  if value_to_parse:
    return float(value_to_parse)
  else:
    None
