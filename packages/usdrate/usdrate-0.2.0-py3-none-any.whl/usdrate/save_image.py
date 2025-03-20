from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def capture_screenshot(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')  # ページ全体が収まるようウィンドウサイズを指定
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    driver.save_screenshot(output_path)
    driver.quit()
    print(f"スクリーンショットが保存されました: {output_path}")

if __name__ == "__main__":
    target_url = "https://www.77bank.co.jp/kawase/usd2024.html"
    capture_screenshot(target_url, "screenshot.png")
