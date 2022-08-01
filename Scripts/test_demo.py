# coding=utf-8
import xlrd2
import xlwt
from appium import webdriver
import time
import yaml
import os
from selenium.webdriver.common.by import By
from tomorrow import threads
from Basic.base import Base

data =xlrd2.open_workbook(r'/Users/zhao/Downloads/data_all.xls')
cols= data.sheet_by_name("Sheet1").col_values(0)
# add_list = cols
add_list =["https://vimeo.com/731378604?autoplay=1",
           "https://www.dailymotion.com/video/x8539b3",
            "https://www.aparat.com/v/JkF83"]
#移除表头
# cols.remove(cols[0])
#结果地址
data_result = xlwt.Workbook('encoding=unf-8')
result_sheet = data_result.add_sheet('result-failed',cell_overwrite_ok=True)
#切换到appium的main.js所在路径
# os.chdir(r'/usr/local/lib/node_modules/appium/build/lib')

def start_appium(port=4723,udid=""):
    a = os.popen('netstat -anv | grep "%s" '% port)
    time.sleep(2)
    t1 = a.read()
    if "LISTEN" in t1:
        print("appium服务已经启动：%s" % t1)
        # s = t1.split(" ")
        # s1 = [i for i in s if i != '']
        # pip = s1[-1].replace("n", "")
    else:
        # 启动appium服务
        # appium -a 127.0.0.1 -p 4740 -U emulator-5554 127.0.0.1:62001 --no-reset
        # print('\n'.join(sys.path))
        # sys.path.append("/path/to/usr/local/lib/node_modules/appium/")
        os.system("appium -a 127.0.0.1 -p %s -U %s --no-reset " % (port, udid))
        # os.chdir(r'/usr/local/lib/node_modules/appium/build/lib')
        # # port = 4723
        # appium_log_path = r'./appium_log{}.log'.format(port)
        # subprocess.Popen('node main.js -p {} -g {}'.format(port, appium_log_path),
        #                  stdout=subprocess.STDOUT,
        #                  stderr=subprocess.PIPE,shell=True).communicate()

def get_desired_caps(devicesName='c7c8ca7e'):
    '''
    从yaml读取desired_caps配置信息
    参数name:设备名称,如：夜神/雷电
    :return: desired_caps字典格式
    '''
    curpath = os.path.dirname(os.path.realpath(__file__))
    yamlpath = os.path.join(curpath, "phone.yaml")
    print("配置地址：%s" % yamlpath)
    f = open(yamlpath, "r", encoding="utf-8")
    a = f.read()
    f.close()
    # 把yaml文件转字典
    d = yaml.safe_load(a)
    for i in d:
        if devicesName in i["desc"]:
            print(i)
            # 启动服务
            devicesName = i['desired_caps']['udid']
            print(devicesName)
            start_appium(port=i['port'],udid=devicesName)
            return (i['desired_caps'], i['port'])

@threads(2)
def run_app(devicesName):
    # 配置参数
    desired_caps = get_desired_caps(devicesName)
    # 执行测试脚本
    driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % desired_caps[1], desired_caps[0])
    time.sleep(3)
    try:
        base_obj = Base(driver)
        base_obj.find_element((By.ID,"free.video.downloader.converter.music:id/tvContinue")).click()
        base_obj.find_element((By.ID,"free.video.downloader.converter.music:id/tvSearch")).click()

        # 清空后 输入网站链接
        # driver.find_element_by_id("free.video.downloader.converter.music:id/tvSearch").click()
        search_input = driver.find_element_by_id("free.video.downloader.converter.music:id/etInput")
        row = 0
        # 批量链接
        for link in add_list:
            search_input.clear()
            search_input.send_keys(link)
            # try:
            # search_input.send_keys("http://vimeo.com/watch")
            driver.find_element_by_id("free.video.downloader.converter.music:id/test_confirm_search_view").click()
            # 点击开始解析按钮
            download_bt = base_obj.find_element((By.ID,"free.video.downloader.converter.music:id/normalView"))
            download_bt.click()
            #查看解析完成按钮
            result = base_obj.find_element((By.ID,"free.video.downloader.converter.music:id/remindCountView"))
            if result:
                print("%s解析成功 可正常下载"%link)
            else:
                print("%s解析失败 或下载失败！ "%link)
                result_sheet.write(row + 1, 0, link)
                row = row + 1
            base_obj.find_element((By.ID, "free.video.downloader.converter.music:id/tvSearch")).click()
            driver.find_element_by_id("free.video.downloader.converter.music:id/ivDeleteAll").click()
    except:
        driver.get_screenshot_as_file('/Users/zhao/Desktop/download_errorphoto/' + 'result.png')
    driver.quit()
if __name__ == "__main__":
    # 作者：上海-悠悠 QQ交流群：330467341
    devices = ["Samxing"]
    for i in devices:
        run_app(devicesName=i)
