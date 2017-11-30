import random
import re
import time

import pickle

import PIL.Image
from pytesseract import pytesseract
from selenium import webdriver
from selenium.webdriver import ActionChains

dir = "C:\\Users\\Masonic\\PycharmProjects\\MasonicBaiduIndex\\output\\"
Monthdict = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30,
             '12': 31}
soapdict = {"三生三世十里桃花"}


def Exist(browser):
    try:
        box = browser.find_element_by_xpath('//div[@id="viewbox"]')
        box = box.get_attribute('style')
        if 'none' in box:
            return False
        else:
            return True
    except:
        return False


def getIndex(name, day, month, driver, i):
    base = driver.find_elements_by_css_selector("#trend rect")[2]
    if i == 0:
        ActionChains(driver).move_to_element_with_offset(base, 3.778877, 10).perform()
    else:
        ActionChains(driver).move_to_element_with_offset(base, 3.778877 * i, 10).perform()
    time.sleep(0.8)
    while (Exist(driver) == False):
        # 1145px / 303days = 3.778877px/day
        off = random.uniform(-0.5, 3.7)
        ActionChains(driver).move_to_element_with_offset(base, 3.778877 * i + off, 10).perform()
        time.sleep(0.1)
        if Exist(driver) == True:
            break
    time.sleep(0.8)
    imgelement = driver.find_element_by_xpath('//div[@id="viewbox"]')
    locations = imgelement.location
    fname = str(month) + "-" + str(day)
    driver.save_screenshot(dir + fname + ".png")
    l = len(name)
    if l > 8:
        l = 8
    rangle = (int(int(locations['x'])) + l * 12 + 32, int(int(locations['y'])) + 28,
              int(int(locations['x'])) + l * 12 + 32 + 80,
              int(int(locations['y'])) + 56)
    img = PIL.Image.open(dir + fname + ".png")
    if locations['x'] != 0.0:
        jpg = img.crop(rangle)
        imgpath = dir + fname + ".png"
        jpg.save(imgpath)
        jpgzoom = PIL.Image.open(str(imgpath))
        (x, y) = jpgzoom.size
        x_s = 60 * 10
        y_s = 20 * 10
        out = jpgzoom.resize((x_s, y_s), PIL.Image.ANTIALIAS)
        out.save(dir + "zoom\\" + fname + ".jpeg", 'jpeg', quality=95)
        image = PIL.Image.open(dir + "zoom\\" + fname + ".jpeg")
        code = pytesseract.image_to_string(image)
        pattern = re.compile("\d+")
        dealcode = code.replace("S", '5').replace(" ", "").replace(",", "").replace("E", "8").replace(".", ""). \
            replace("'", "").replace(u"‘", "").replace("B", "8").replace("\"", "").replace("I", "1").replace(
            "i", "").replace("-", "").replace("$", "8").replace(u"’", "").strip()
        result = pattern.search(dealcode)
        if result:
            return result.group()
        else:
            return 0
            # while result != "None":
            #     result = getIndex(name, day, month, driver, i)


def save_cookies():
    # ~ dcap = dict(DesiredCapabilities.PHANTOMJS)
    # ~ dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    # ~ self.driver=webdriver.PhantomJS(executable_path='/usr/bin/phantomjs', desired_capabilities= dcap)
    driver = webdriver.Chrome()
    # ~ driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
    driver.get('http://index.baidu.com/?tpl=trend&words=%B9%C7%C3%DC%B6%C8%D2%C7')
    time.sleep(1)
    e1 = driver.find_element_by_id("TANGRAM_12__userName")
    e1.send_keys("POPKAP")
    time.sleep(1)
    e2 = driver.find_element_by_id("TANGRAM_12__password")
    e2.send_keys("18353258669x")
    time.sleep(1)
    e3 = driver.find_element_by_id("TANGRAM_12__submit")
    time.sleep(1)
    e3.click()
    cookies = driver.get_cookies()
    driver.quit()
    pickle.dump(cookies, open("C:\\Users\\Masonic\\PycharmProjects\\MasonicBaiduIndex\\cookies\\cookies.pkl", "wb"))


# options = webdriver.ChromeOptions()
# options.add_argument("--user-data-dir=C:\\Users\\Masonic\\PycharmProjects\\MasonicBaiduIndex\\Chrome")
# driver = webdriver.Chrome(chrome_options=options)
def initial():
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get('http://index.baidu.com')
    login = driver.find_element_by_id('schword')
    login.send_keys('三生三世十里桃花')
    time.sleep(0.5)
    submit = driver.find_elements_by_css_selector('input[type=submit]')[0]
    submit.click()
    time.sleep(0.5)
    e1 = driver.find_element_by_id("TANGRAM_12__userName")
    e1.send_keys("POPKAP")
    time.sleep(0.5)
    e2 = driver.find_element_by_id("TANGRAM_12__password")
    e2.send_keys("18353258669x")
    time.sleep(0.5)
    e3 = driver.find_element_by_id("TANGRAM_12__submit").click()

    time.sleep(5)
    driver.find_element_by_xpath("//span[@class='selectA rangeDate']").click()
    driver.find_element_by_xpath("//a[@href='#cust']").click()
    driver.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    driver.find_element_by_xpath(
        "//span[@class='selectA monthA slided']//ul//li//a[@href='#01']").click()
    driver.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    driver.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + '2017' + "']").click()
    driver.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    driver.find_element_by_xpath(
        "//span[@class='selectA monthA slided']//ul//li//a[@href='#10']").click()
    driver.find_element_by_xpath("//input[@value='确定']").click()
    time.sleep(2)
    month, day = 1, 1
    for soap in soapdict:
        for i in range(304):
            wf = open(dir + "final\\" + soap, 'a')
            index = getIndex(soap, day=day, month=month, driver=driver, i=i)
            wf.write(str(month) + "-" + str(day) + "," + str(index))
            if int(day) == Monthdict[str(month)]:
                day = 1
                month = int(month) + 1
            else:
                day = int(day) + 1
            wf.write('\n')
            wf.close()



# imgelement = driver.find_element_by_xpath('//div[@id="viewbox"]')
time.sleep(10)  # cookies = driver.get_cookies()
# driver.quit()
# pickle.dump(cookies, open("cookies/cookies.pkl", "wb"))
if __name__ == '__main__':
    initial()
