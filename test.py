#!/usr/bin/python3

from selenium import webdriver
import time

# Chromeのオプション
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Selenium Serverに接続
driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
options=options)

try:
  # 要素の待機時間を最大10秒に設定
  driver.implicitly_wait(10)

  # https://gihyo.jp を開く
  driver.get("https://yoyaku.sports.metro.tokyo.lg.jp/web/")


except:
  import traceback
  traceback.print_exc()

finally:
  # Chromeを終了
  input("何かキーを押すと終了します...")
  driver.quit()