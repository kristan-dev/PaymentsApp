import collections
from validations import validate_params
import requests
from requests.adapters import HTTPAdapter

class Payments:
  validation_status = False
  payment_info = None   

  def init_payment(self, pay_paramns):
    payment_data = collections.namedtuple(
      typename="PaymentData",
      field_names=[
        "CreditCardNumber",
        "CardHolder",
        "ExpirationDate",
        "SecurityCode",
        "Amount"
        ]
    )

    self.payment_info = payment_data(
      CreditCardNumber=pay_paramns["CreditCardNumber"],
      CardHolder=pay_paramns["CardHolder"],
      ExpirationDate=pay_paramns["ExpirationDate"],
      SecurityCode=pay_paramns["SecurityCode"],
      Amount=pay_paramns["Amount"]
    )
  
  def validate_payment(self):
    self.validation_status = validate_params(payment_info=self.payment_info)
  
  def process_payment(self) -> bool:
    sesh= requests.Session()
    if(self.validation_status is True):
      try:
        if(self.payment_info.Amount < 20):
          sesh.get('http://127.0.0.1:5000/cheappayment')
        elif(self.payment_info.Amount>=21 and self.payment_info.Amount <=500):
          sesh.mount('http://127.0.0.1:5000/expensivepayment', HTTPAdapter(max_retries=1))
          res = sesh.get('http://127.0.0.1:5000/expensivepayment')
          if(res.status_code != 200):
            sesh.get('http://127.0.0.1:5000/cheappayment')
        elif(self.payment_info.Amount > 500):
          sesh.mount('http://127.0.0.1:5000/premiumppayment', HTTPAdapter(max_retries=3))
          sesh.get('http://127.0.0.1:5000/premiumppayment')
        return True
      except Exception as e:
        return False

    return False

if(__name__ == "__main__"):
  test_data = {
    'CreditCardNumber': '5363-4700-1509-4092',
    'CardHolder': 'Joel Cain',
    'ExpirationDate': '2027-02-12',
    'SecurityCode': '143',
    'Amount':'500.00'
  }
  pass