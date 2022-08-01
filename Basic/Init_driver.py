from selenium import webdriver

def init_driver():
    desired_caps  ={}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion']= '11'
    desired_caps['deviceName'] = ''
    # app包名和启动名
    desired_caps['appPackage'] = 'free.video.downloader.converter.music'
        # 'video.downloader.videodownloader.tube'
    desired_caps['appActivity'] = 'free.video.downloader.converter.music.view.activity.StartupActivity'

    desired_caps['chromedriverExecutbleDir'] = '/usr/local/lib/node_modules/appium/node_modules/appium-chromedriver/chromedriver/mac'
    desired_caps['chromedriverChromeMappingFile'] = '/usr/local/lib/node_modules/appium/node_modules/appium-chromedriver/chromedriver/chromedriver_support.json'
    desired_caps['npReset']=True
    # 手机驱动对象
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    return driver # 返回driver对象


