from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from PIL import Image
import StringIO
import base64
import tesseract_ocr

from copy import deepcopy

class Amazon_API(object):
    state = "start"
    max_wait=5
    ret ={"old_balance":'','status_msg':'','new_balance':'',}
    base_redeem_url = "https://www.amazon.com/gc/redeem"

    def __init__(self,width=1151,height=629):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ( "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0 WebKit" )
        #self.br = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ssl-protocol=any','--ignore-ssl-errors=true'])
        self.br=webdriver.Firefox()
        self.br.set_window_size(width,height)

    def set_credentials(self,username,password):
        self.username = username
        self.password = password

    def navigate_to_login(self):
        br =  self.br
        br.save_screenshot("ss.png")
        self.br.get("https://www.amazon.com/")
        href = br.find_element_by_xpath("//div[@id='nav-flyout-ya-signin']/a").get_attribute("href")
        br.get(href)

    def wait_for_element(self,elem):
        br=self.br
        try:
            WebDriverWait(br,self.max_wait).\
                until(EC.presence_of_element_located(elem))
        except:
            pass

    def login(self):
        br = self.br
        br.save_screenshot("ss.png")
        captcha = br.find_elements_by_id("auth-captcha-guess")
        if captcha:
            self.solve_captcha_login()

        br.find_element_by_id("ap_email").send_keys(self.username)
        br.find_element_by_id("ap_password").send_keys(self.password)
        br.find_element_by_id("signInSubmit").click()
        self.wait_for_element(br.find_element_by_partial_link_text("Gift Cards"))

    def navigate_to_code_reedem(self):
        self.state="loggedin"
        br = self.br
        br.find_element_by_partial_link_text("Gift Cards").click()
        redeem = [(i,i.get_attribute("alt")) for i in self.br.find_elements_by_xpath("//div[@id='merchandised-content']//map/area[@alt]") if i.get_attribute("alt")=='Redeem an Amazon.com gift card']
        if redeem:
            self.wait_for_element(redeem[0][0])
            redeem[0][0].click()
        self.state = 'enter_code'

    def set_code(self,code):
        self.code = code

    def solve_captcha_login(self):
        br = self.br
        element = br.find_element_by_id('auth-captcha-image') # find part of the page you want image of
        location = element.location
        size = element.size
        im = Image.open(StringIO.StringIO(base64.decodestring(br.get_screenshot_as_base64())))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save("captcha.jpg")
        text = tesseract_ocr.text_for_filename("captcha.jpg")
        br.find_element_by_id("auth-captcha-guess").send_keys(text)

    def solve_captcha_reedeem(self):
        br = self.br
        element = br.find_element_by_class_name("gc-captcha-image")
        location = element.location
        size = element.size
        im = Image.open(StringIO.StringIO(base64.decodestring(br.get_screenshot_as_base64())))
        left,top,right,bottom = location['x'],location['y'],location['x']+size['width'],location['y']+size['height']
        im = im.crop((left,top,right,bottom))
        im.save("captcha_reedem.jpg")
        text = tesseract_ocr.text_for_filename("captcha_reedem.jpg")
        br.find_element_by_xpath("//input[@name='captchaInput']").send_keys(text)

    def enter_code(self):
        code = self.code
        br = self.br
        captcha = br.find_elements_by_class_name("gc-captcha-image")
        if captcha:
            self.solve_captcha_reedeem()
        old_balance_elem = br.find_element_by_id("gc-current-balance")
        old_balance =  old_balance_elem.text
        self.ret['old_balance'] = old_balance if old_balance else "0"
        br.find_element_by_id("gc-redemption-input").send_keys(self.code)
        br.find_elements_by_class_name("a-button-input")[0].click()
        try:
            self.wait_for_element(br.find_element_by_class_name("a-alert-heading"))
            status_elem = br.find_element_by_class_name("a-alert-heading")
            status = status_elem.text
        except:
            status = br.find_element_by_class_name("a-alert-content").text

        self.ret['status_msg'] = status if status else "unknown"
        self.ret['status'] = "valid" if "has been added to your" in status else "invalid"
        new_balance = br.find_element_by_id("gc-current-balance").text
        self.ret['new_balance'] = new_balance
        br.get(self.base_redeem_url)
        return self.ret

browser = Amazon_API()
