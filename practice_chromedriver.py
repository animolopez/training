#for Google Chrome
#Chrome Driver と Google chrome のバージョンを対応させる必要アリ
#Chrome Driver ver.90 に path を通し済み
#参考：https://qiita.com/memakura/items/20a02161fa7e18d8a693

import time
from selenium import webdriver

driver = webdriver.Chrome() # ()内に各ブラウザ対応のwebdriverが存在するパスを指定。空欄ならPATHが指定される。
url = 'https://www.google.com/'
driver.get(url)
time.sleep(2) # 処理の一時停止(パッチ処理)
search_box = driver.find_element_by_name("q")
search_box.send_keys('ミスタードーナツ　カロリー')
search_box.submit()
time.sleep(5)
driver.quit()
