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

@app.route("/action",methods=['POST'])
def request_accept():
    try:
        pd = ujson.loads(request.get_data())
        if br.state !='enter_code':
            br.navigate_to_login()
            br.login(pd['username'],pd['password'])
            br.navigate_to_code_reedem()

        ret = br.enter_code(pd['code'])
        return ujson.dumps(ret),200
    except:
        import traceback
        traceback.print_exc()
        return "ERROR",400

if __name__=='__main__':
    app.run(port=5000,host="0.0.0.0")