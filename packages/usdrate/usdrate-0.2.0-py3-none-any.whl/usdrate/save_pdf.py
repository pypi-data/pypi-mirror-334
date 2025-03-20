import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def save_as_pdf(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 必要に応じてウィンドウサイズの指定も追加可能
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    # ページが完全にレンダリングされるのを待つ場合は time.sleep() や明示的な待機を利用してください

    # DevToolsプロトコルを使ってPDF出力
    pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
    pdf_data = base64.b64decode(pdf['data'])
    
    with open(output_path, 'wb') as f:
        f.write(pdf_data)

    driver.quit()
    print(f"PDFが保存されました: {output_path}")

if __name__ == "__main__":
    target_url = "https://www.77bank.co.jp/kawase/usd2024.html"
    save_as_pdf(target_url, "page.pdf")
