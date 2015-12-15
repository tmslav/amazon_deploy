from flask import Flask,request
app = Flask(__name__)
from webdriver import Amazon_API
import ujson

br=Amazon_API()

@app.route("/post_code",methods=['POST'])
def request_accept():
    try:
        pd = ujson.loads(request.get_data())
        br.set_code(pd['code'])
        ret = br.enter_code()
        return ret,200
    except:
        return "ERROR",400

@app.route("/login_to_amazon",methods=['POST'])
def login_to_amazon():
    try:
        pd=ujson.loads(request.get_data())
        br.set_credentials(pd['username'],pd['password'])
        br.navigate_to_login()
        br.login()
        br.navigate_to_code_reedem()
        return 'OK',200
    except:
        return "ERROR",400




if __name__=='__main__':
    app.run(port=5000)