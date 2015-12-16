from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from copy import deepcopy

class Amazon_API(object):
    state = "start"
    function_states = {
        'init':'navigate_to_login',
        'login':'login',
        'navigate_to_redeem_url':'navigate_to_reedem_url',
        'enter_code':'enter_code',
    }
    ret ={"old_balance":'','status_msg':'','new_balance':'',}
    base_redeem_url = "https://www.amazon.com/gc/redeem"
    def next_action(self,**kwargs):
        func = getattr(self,self.function_states[self.state])
        func(self)

    def __init__(self,width=1151,height=629):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ( "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0 WebKit" )
        self.br = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ssl-protocol=any','--ignore-ssl-errors=true'])
        self.br.set_window_size(width,height)
        self.state = "init"

    def set_credentials(self,username,password):
        self.username = username
        self.password = password

    def navigate_to_login(self):

        br =  self.br
        br.save_screenshot("ss.png")
        self.br.get("https://www.amazon.com/")
        href = br.find_element_by_xpath("//div[@id='nav-flyout-ya-signin']/a").get_attribute("href")
        br.get(href)
        self.state = 'login'

    def login(self):
        br = self.br
        br.save_screenshot("ss.png")
        br.find_element_by_id("ap_email").send_keys(self.username)
        br.find_element_by_id("ap_password").send_keys(self.password)
        br.find_element_by_id("signInSubmit").click()
        return self.br.page_source

    def navigate_to_code_reedem(self):
        br = self.br
        br.save_screenshot("ss.png")
        br.find_element_by_partial_link_text("Gift Cards").click()
        redeem = [(i,i.get_attribute("alt")) for i in self.br.find_elements_by_xpath("//div[@id='merchandised-content']//map/area[@alt]") if i.get_attribute("alt")=='Redeem an Amazon.com gift card']
        if redeem:
            redeem[0][0].click()

    def set_code(self,code):
        self.code = code

    def enter_code(self):
        import ipdb;ipdb.set_trace()
        code = self.code
        br = self.br
        br.save_screenshot("ss.png")
        old_balance = br.find_element_by_id("gc-current-balance").text
        self.ret['old_balance'] = old_balance if old_balance else "0"

        br.find_element_by_id("gc-redemption-input").send_keys(self.code)
        br.find_elements_by_class_name("a-button-input")[0].click()
        page_source = deepcopy(br.page_source)
        status = br.find_element_by_class_name("a-alert-heading").text

        self.ret['status_msg'] = status if status else "unknown"
        self.ret['status'] = "valid" if "has been added to your" in status else "invalid"
        new_balance = br.find_element_by_id("gc-current-balance").text
        self.ret['new_balance'] = new_balance
        br.get(self.base_redeem_url)
        br.save_screenshot("ss.png")

        return self.ret



browser = Amazon_API()
