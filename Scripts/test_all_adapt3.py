#coding:utf-8
import time
import unittest
import xlrd2
import xlwt
from Basic.Init_driver import   init_driver

#源文件地址
data =xlrd2.open_workbook(r'/Users/zhao/Downloads/data_all.xls')
cols= data.sheet_by_name("Sheet1").col_values(0)
add_list = cols
#移除表头
# cols.remove(cols[0])

#结果地址
data_result = xlwt.Workbook('encoding=unf-8')
result_sheet = data_result.add_sheet('result-failed',cell_overwrite_ok=True)

class Testcase(unittest.TestCase):
    def setUp(self) :
        self.driver = init_driver()

    def test_all(self):
        u"""
        用例说明：用户下载适配网站文件
        用例步骤：
        1. 用户进入首页
        2. 输入网站链接
        3，点击下载按钮
        4，用户退出
        :return:
        """
        #启动进入首页
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/tvContinue").click()
        #清空后 输入网站链接
        self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/tvSearch").click()
        search_input = self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/etInput")
        row = 0
        #批量链接
        for link in add_list:
            search_input.clear()
            search_input.send_keys(link)
            # try:
            # search_input.send_keys("http://vimeo.com/watch")
            self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/test_confirm_search_view").click()
            # time.sleep(8)

            # self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/tvGotIt").click()
            # self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/tvGotIt").click()
            #点击watch now按钮
            # self.driver.find_element_by_xpath(
            #     "//android.view.View[@content-desc='Watch now']/android.widget.TextView[2]").click()

            #点击开始解析按钮
            download_bt = \
                self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/normalView")
            download_bt.click()
            result = self.driver.find_element_by_id("video.downloader.videodownloader.tube:id/remindCountView")
            if  result :
                print ("解析成功 可正常下载")
            else:
                print("解析失败 或下载失败！ ")
                result_sheet.write(row+1,0,link)
                row=row+1
            # except:
            self.driver.get_screenshot_as_file('/Users/zhao/Desktop/download_errorphoto/'+'result.png')
    data_result.save("data_result.xls")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()