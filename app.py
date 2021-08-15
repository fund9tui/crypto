#prerequsite : 
#https://code.visualstudio.com/docs/python/tutorial-flask 

# before run
# & c:/Users/9Tui_Lenovo700/CryptoAlert/env/Scripts/Activate.ps1
# $env:FLASK_ENV = "development"
#> $env:FLASK_APP = "app.py"
#> flask run
#https://youtu.be/gMRee2srpe8?list=PLbWPa4Ld0yBweAd69rP2JNBwK9pi68pzG
import json, config ,urllib , requests 
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

URL = "https://notify-api.line.me/api/notify"
image_ext = ['jpg','jpeg','png']
line_limit = [0,0,9,0,'01/01/2017']
line_remain = ['ddddd']

def sendline(message_text , ltoken ):
    LINE_HEADERS = {
     'Authorization': 'Bearer ' + ltoken 
    }
    payload = {"message" :  message_text}
 
    try:
     
     response = requests.post(
     url=URL,
     headers=LINE_HEADERS,
    params=payload 
     )
   
#     print(response.headers)
#     print(response.text)
     
     line_limit[0] = response.headers.get('X-RateLimit-Limit')
     line_limit[1] = response.headers.get('X-RateLimit-Remaining') 
     line_limit[2] = response.headers.get('X-RateLimit-ImageLimit')
     line_limit[3] = response.headers.get('X-RateLimit-ImageRemaining')   
     line_limit[4] = response.headers.get('Date')   
     line_remain[0] = ("Message : " + response.headers.get('X-RateLimit-Remaining')  + "/" +  response.headers.get('X-RateLimit-Limit') 
                      + "  Image  : " + response.headers.get('X-RateLimit-ImageRemaining')  + "/" +  response.headers.get('X-RateLimit-ImageLimit')  ) 
#     print("Line Remain : ",line_remain[0])
#     print(line_limit)     
#     print('Response HTTP Status Code: {status_code}'.format( status_code=response.status_code))
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
     
    return 1  
def sendlineimage(message_text , message_pict , ltoken ):
    LINE_HEADERS = {
     'Authorization': 'Bearer ' + ltoken 
    }
    payload = {"message" :  message_text}
 
    try:
     files = {"imageFile": open(message_pict, "rb")}   
     
     response = requests.post(
     url=URL,
     headers=LINE_HEADERS,
    params=payload, 
    files=files
     )
   
#     print(response.headers)
#     print(response.text)
     
     line_limit[0] = response.headers.get('X-RateLimit-Limit')
     line_limit[1] = response.headers.get('X-RateLimit-Remaining') 
     line_limit[2] = response.headers.get('X-RateLimit-ImageLimit')
     line_limit[3] = response.headers.get('X-RateLimit-ImageRemaining')   
     line_limit[4] = response.headers.get('Date')   
     line_remain[0] = ("Message : " + response.headers.get('X-RateLimit-Remaining')  + "/" +  response.headers.get('X-RateLimit-Limit') 
                      + "  Image  : " + response.headers.get('X-RateLimit-ImageRemaining')  + "/" +  response.headers.get('X-RateLimit-ImageLimit')  ) 
#     print("Line Remain : ",line_remain[0])
#     print(line_limit)     
#     print('Response HTTP Status Code: {status_code}'.format( status_code=response.status_code))
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
     
    return 1 



#client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
#        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
#    order_response = order(side, quantity, "DOGEUSD")

#    if order_response:
#        return {
#            "code": "success",
#            "message": "order executed"
#        }
#    else:
#        print("order failed")
#        return {
#            "code": "error",
#            "message": "order failed"
#        }

    msg = "\n[" + data['name'] + "]"
    msg += "\n" + "====" + data['ticker'] + "===="
    msg += "\n" + "interval : " + data['interval'] + ""
 #   msg += '\n' + 'recommend :'+ data['strategy']['order_comment']
    msg += '\n' + 'action : '+ side
    msg += '\n' + 'quantity: ' +str(quantity) 
    msg += '\n' + 'price: ' + '{:.5f}'.format(data['strategy']['order_price']) 
 #   print(msg)
    result = sendline(msg , config.LINE_ACCESS_TOKEN ) 
 #   print(result)
    return {
        "code" : "success",
        "message" : msg  
    }

