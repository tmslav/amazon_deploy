from flask import Flask,request,send_file
app = Flask(__name__)
from webdriver import Amazon_API
import ujson

br=Amazon_API()
@app.route("/",methods=['GET'])
def r():
    return "Hi"

@app.route("/image")
def image():
        return send_file("ss.png",mimetype='image/gif')

@app.route("/post_code",methods=['POST'])
def request_accept():
    try:
        pd = ujson.loads(request.get_data())
        br.set_code(pd['code'])
        ret = br.enter_code()
        return "OK",200
    except:
        return "ERROR",400

@app.route("/login_to_amazon",methods=['POST'])
def login_to_amazon():
    try:
        import ipdb;ipdb.set_trace()
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