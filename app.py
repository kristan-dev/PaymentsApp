from flask import Flask, json, jsonify, request
from flask.helpers import make_response
from flask_cors import CORS
from flask_restful import Api, Resource
from payments import Payments

app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': '*'}})
api = Api(app)


class ProcessPayment(Resource):
  def get(self):
    return jsonify(message="GET invoked", category="SUCCESS", status=200)
  
  def post(self):
    try:
      raw_data = request.get_json()

      this_payment = Payments()
      this_payment.init_payment(pay_paramns=raw_data)
      this_payment.validate_payment()

      if(this_payment.process_payment() is True):
        return make_response("OK", 200)
      else:
        return make_response("Bad Request", 400)
    except Exception as e:
      return make_response("Internal Server Error", 500)


api.add_resource(ProcessPayment, '/processpayment')

if(__name__ == '__main__'):
  app.run()
  pass