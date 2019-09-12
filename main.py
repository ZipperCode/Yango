from selenium import webdriver
import random
import time
username = "账号" # 此处填账号
password = "密码" # 此处填密码
# url = "http://27.151.115.58:8082/"


class Yango:

    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.set_window_size(550, 450)
        self.all_link = []
        self.assess_flag = False
        pass

    def open(self,url = "http://27.151.115.58:8082/"):
        self.driver.get(url)
        time.sleep(2)
        assert "阳光学院教务部" in self.driver.title

    def login(self):
        uname = self.driver.find_element_by_name("muser")
        uname.clear()
        uname.send_keys(username)
        pswd = self.driver.find_element_by_name("passwd")
        pswd.clear()
        pswd.send_keys(password)
        code = self.driver.find_element_by_name("captchacode")
        # capt_img = self.driver.find_element_by_id("imgCaptcha")
        c = input("请输入验证码=>")
        while c == None or c == "":
            c = input("请输入验证码=>")
        print('您输入的验证码为=>', c)
        code.send_keys(c)
        submit = self.driver.find_element_by_name("dl")
        submit.click()
        time.sleep(1)

    def judge_login(self):
        while self.is_alert():
            self.login()
        print("登陆成功！！")

    def is_alert(self):
        try:
            self.driver.switch_to.alert.accept()
            return True
        except:
            return False

    def is_main_page(self):
        return self.driver.title == "网络办公系统"

    def show_cur_page(self):
        print("当前界面 title=>",self.driver.title)

    def open_score_page(self, url="http://27.151.115.58:8082/xszy/wdcj/cjyl/teach_list.asp?menu_no=1901"):
        self.driver.get(url)
        try:
            table = self.driver.find_element_by_xpath('//table[@class="linking"]/tbody')
        except:
            print('none table')
            table = None
        print('table==>', table)
        if table:
            print('operate table')
            links = table.find_elements_by_link_text("开始评议")
            for link in links:
                self.all_link.append(link.get_attribute('href'))
            self.assess_flag = True
        else:
            print('cancel table operator')

    def assess(self):
        if self.assess_flag:
            for index in range(0,len(self.all_link)):
                self.driver.get(self.all_link[index])
                self.full_score()
                while self.is_alert():
                    time.sleep(1)
                    self.driver.get(self.all_link[index])
                    time.sleep(2)
                    self.full_score()
                print('评价第'+str(index)+'个老师成功')
        else:
            print('似乎没有评价！')
        self.driver.close()
        pass

    def full_score(self):
        form = self.driver.find_element_by_name('cpform')
        try:
            form_table = form.find_element_by_xpath('//table[@width="1000"]')
            trList = form_table.find_elements_by_tag_name('tr')
            print('list length =>', len(trList))
            for index in range(1, len(trList)):
                inp = trList[index].find_element_by_tag_name('input')
                if inp:
                    inp.send_keys(random.randint(85, 100))
        except Exception as e:
            print('assess table operator error')
            raise e
        form.find_element_by_id('bt1').click()
        pass

if __name__ == "__main__":
    yg = Yango()
    yg.open()#打开登陆页面
    yg.login()#登陆
    yg.judge_login() #判断是否登录
    yg.show_cur_page() #展示当前页面title
    yg.open_score_page()#打开成绩页面
    yg.assess()#评价老师


