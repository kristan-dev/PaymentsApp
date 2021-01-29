import collections
from flask import Flask, jsonify, request
import re
from datetime import datetime

def validate_params(payment_info: collections.namedtuple) -> bool:

  return all([
    validate_cc(payment_info.CreditCardNumber),
    validate_cardholder(payment_info.CardHolder),
    validate_expirationdate(payment_info.ExpirationDate),
    validate_seccode(payment_info.SecurityCode),
    validate_amount(payment_info.Amount)
  ])

def validate_cc(ccnumbner: str) -> bool:
  if(re.search(r"(?:\d{4}-?){3}\d{4}", ccnumbner.replace(" ", ""))):
    return True
  return False

def validate_cardholder(cardholder: str) -> bool:
  if(re.search(r"^[a-zA-Z]+$", cardholder.replace(" ", ""))):
    return True
  return False

def validate_expirationdate(expirationdate: str) -> bool:
  try:
    ccdate = datetime.strptime(expirationdate, "%Y-%m-%d")
  except Exception as e:
    return False

  if(ccdate >= datetime.today()):
    return True
  return False

def validate_seccode(seccode: str) -> bool:
  if(re.search(r"\d{3}", seccode.replace(" ", ""))):
    return True
  return False

def validate_amount(amount: str) -> bool:
  try:
    amount = float(amount)
    if(amount>0):
      return True
  except Exception as e:
    return False
  return False


if(__name__ == '__main__'):
  test_data = {
    'CreditCardNumber': '5363-4700-1509-4092',
    'CardHolder': 'Joel Cain',
    'ExpirationDate': '2027-02-12',
    'SecurityCode': '143',
    'Amount':'500.00'
  }
  print(validate_params(test_data))
  pass