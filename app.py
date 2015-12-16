__author__="tmslav"
from flask import Flask,request,send_file
app = Flask(__name__)
from webdriver import browser as br
import ujson


@app.route("/",methods=['GET'])
def r():
    return "Hi"

@app.route("/state")
def state():
    return br.state,200

@app.route("/send_code",methods=['POST'])
def request_accept():
    try:
        pd = ujson.loads(request.get_data())
        br.set_code(pd['code'])
        ret = br.enter_code()
        return ujson.dumps(ret),200
    except:
        import traceback
        traceback.print_exc()
        return "ERROR",400

@app.route("/login",methods=['POST'])
def login_to_amazon():
    try:
        pd=ujson.loads(request.get_data())
        br.set_credentials(pd['username'],pd['password'])
        br.navigate_to_login()
        br.login()
        br.navigate_to_code_reedem()
        return 'OK',200
    except:
        return "ERROR:{}".format(request.get_data()),400




if __name__=='__main__':
    app.run(port=5000,host="0.0.0.0")