import  unittest
import datetime
import  os
from BeautifulReport import BeautifulReport

#测试用例路径
case_path = os.path.join(os.getcwd(),"Scripts")
#自动化报告存放路径
report_path = os.path.join(os.getcwd(),"Report")
def all_case():
    #discover()方法能够批量执行测试用例
    discover = unittest.defaultTestLoader.discover(case_path,pattern='test_all_adapt3.py',top_level_dir=None)
    return discover

if __name__ == '__main__':
    # 建立自动化测试报告
    #测试报告名称
    now = datetime.datetime.now().strftime('%Y_%m%d_%H%M%S')
    filename = '自动化测试报告'+str(now)
    #用例名称
    description = '功能自动化测试'
    report_dir = report_path
    result = BeautifulReport(all_case())
    result.report(filename=filename,description=description,report_dir=report_path)
