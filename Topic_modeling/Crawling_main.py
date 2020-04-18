from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
import urllib.request
import requests
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import Chrome, ChromeOptions
import pickle
import ast, warnings
from bs4 import BeautifulSoup
import urllib, time

warnings.filterwarnings("ignore", category=DeprecationWarning)


class CrawlingWidget(QWidget):

    news_data = []
    page_count = 0
    client_id = ""
    client_secret = ""
    doc_count = 0
    # client_id = "85EE1wzHs7GTndgtN2vP"
    # client_secret = "54aVonJzf1"

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./Crawling_UI.ui")
        self.ui.show()
        self.ui.btn_crawling.clicked.connect(self.crawling_naver_news)

    def crawling_naver_news(self):
        links = self.link_downloading()
        titles, contents = self.crawling(links)

        with open("./data/naver_news_title.pk", 'wb') as f:
            pickle.dump(titles, f)
        with open("./data/naver_news_contents.pk", 'wb') as f:
            pickle.dump(contents, f)
        self.ui.ln_doccount.display(self.doc_count)
        self.pop_message("수집 완료!!")


    def link_downloading(self):
        keyword = self.ui.le_keyword.text()
        encText = urllib.parse.quote(keyword)
        self.client_id = self.ui.le_clientId.text()
        self.client_secret = self.ui.le_clientSecret.text()
        self.page_count = int(self.ui.le_pagecount.text())

        for idx in range(self.page_count):
            url = "https://openapi.naver.com/v1/search/news?query=" + encText + \
                "&start=" + str(idx * 10 + 1)
            print(url)
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if(rescode == 200):
                result = requests.get(response.geturl(),
                                      headers={"X-Naver-Client-Id": self.client_id,
                                               "X-Naver-Client-Secret": self.client_secret})
                self.news_data.append(result.json())
            else:
                print("Error Code: " + rescode)

        naver_news_link = []

        for page in self.news_data:
            page_news_link = []

            for item in page['items']:
                link = item['link']
                if "naver" in link:
                    page_news_link.append(link)

            naver_news_link.append(page_news_link)

        print(len(naver_news_link))

        for page in naver_news_link:
            for link in page:
                print(link)

        return naver_news_link


    def crawling(self, links):
        options = ChromeOptions()
        options.add_argument('-headless')
        driver = Chrome(options=options)

        naver_news_title = []
        naver_news_content = []

        for n in range(len(links)):
            news_page_title = []
            news_page_content = []

            for idx in range(len(links[n])):
                try:
                    driver.get(links[n][idx])
                    print(links[n][idx])
                except:
                    print("TimeOut!!")
                    continue

                try:
                    response = driver.page_source
                except UnexpectedAlertPresentException:
                    driver.switch_to_alert().accept()
                    print("게시글이 삭제되었습니다.")
                    continue

                soup = BeautifulSoup(response, "html.parser")

                title = None

                try:
                    item = soup.find('div', class_="article_info")
                    title = item.find('h3', class_="tts_head").get_text()
                except:
                    title = "OUTLINK"
                    print(title)

                news_page_title.append(title)

                doc = None
                text = ""

                data = soup.find_all("div", {"class":"_article_body_contents"})
                if data:
                    for item in data:
                        text = text + str(item.find_all(text=True)).strip()
                        text = ast.literal_eval(text)
                        doc = ' '.join(text)
                    self.doc_count += 1
                else:
                    doc = "OUTLINK"

                news_page_content.append(doc.replace('\n', ' '))

            naver_news_title.append(news_page_title)
            naver_news_content.append(news_page_content)

            time.sleep(2)

        # print(naver_news_title[0])
        # print(naver_news_content[0])

        return naver_news_title, naver_news_content


    def pop_message(self, message):
        QMessageBox.information(self, "", message, QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication([])
    w = CrawlingWidget()
    app.exec_()