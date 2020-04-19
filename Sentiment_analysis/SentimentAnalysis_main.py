from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem
import re
from konlpy.tag import Mecab
import os, json


class SAWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.train_docs = []
        self.test_docs = []
        self.train_data = []
        self.test_data = []
        self.train_path = ""
        self.test_path = ""
        self.ui = uic.loadUi("./SentimentAnalysis_UI.ui")
        self.ui.show()
        self.ui.btn_loading.clicked.connect(self.data_loading)
        self.ui.btn_tokenizing.clicked.connect(self.making_data)

    def data_loading(self):
        self.train_path = self.ui.le_train_file.text()
        self.test_path = self.ui.le_test_file.text()
        try:
            self.train_docs = self.read_documents(self.train_path)
            self.ui.tbl_train_data.clearContents()
            self.set_tbl_train_data(self.train_docs)
            self.ui.ln_train_data.display(len(self.train_docs))
        except:
            self.ui.tbl_train_data.clearContents()
            self.ui.tbl_train_data.setItem(0, 0, QTableWidgetItem("File Not Found"))
        try:
            self.test_docs = self.read_documents(self.test_path)
            self.ui.tbl_test_data.clearContents()
            self.set_tbl_test_data(self.test_docs)
            self.ui.ln_test_data.display(len(self.test_docs))
        except:
            self.ui.tbl_test_data.clearContents()
            self.ui.tbl_test_data.setItem(0, 0, QTableWidgetItem("File Not Found"))

    def read_documents(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            docs = [line.split('\t') for line in f.read().splitlines()]
            docs = docs[1:]      # header 제거
        return docs

    def set_tbl_train_data(self, data):
        row_max = 10
        col_max = 3
        for i in range(row_max):
            for j in range(col_max):
                self.ui.tbl_train_data.setItem(i, j, QTableWidgetItem(data[i][j]))

    def set_tbl_test_data(self, data):
        row_max = 10
        col_max = 3
        for i in range(row_max):
            for j in range(col_max):
                self.ui.tbl_test_data.setItem(i, j, QTableWidgetItem(data[i][j]))

    def text_cleaning(self, doc):
        doc = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힇 ]", "", doc)
        return doc

    def define_stopwords(self, path):
        SW = set()
        with open(path) as f:
            for word in f:
                SW.add(word)
        return SW

    def making_data(self):
        if os.path.exists("data/train_docs.json"):
            with open("data/train_docs.json", encoding="utf-8") as f:
                self.train_data = json.load(f)
        else:
            self.train_data = [(self.text_tokenizing(self.text_cleaning(line[1])), line[2])
                               for line in self.train_docs if self.text_tokenizing(line[1])]
            with open("data/train_docs.json", "w", encoding="utf-8") as f:
                json.dump(self.train_data, f, ensure_ascii=False, indent="\t")

        if os.path.exists("data/test_docs.json"):
            with open("data/test_docs.json", encoding="utf-8") as f:
                self.test_data = json.load(f)
        else:
            self.test_data = [(self.text_tokenizing(self.text_cleaning(line[1])), line[2])
                              for line in self.test_docs if self.text_tokenizing(line[1])]
            with open("data/test_docs.json", "w", encoding="utf-8") as f:
                json.dump(self.test_data, f, ensure_ascii=False, indent="\t")

        self.set_tbl_train_token(self.train_data)
        self.set_tbl_test_token(self.test_data)

    def text_tokenizing(self, doc):
        mecab = Mecab()
        SW = self.define_stopwords("./data/stopwords-ko.txt")

        if self.ui.rb_noun.isChecked():
            return [word for word in mecab.nouns(doc) if word not in SW and len(word) > 1]
        elif self.ui.rb_morphs.isChecked():
            return [word for word in mecab.morphs(doc) if word not in SW and len(word) > 1]
        elif self.ui.rb_words.isChecked():
            return [word for word in mecab.words(doc) if word not in SW and len(word) > 1]

    def set_tbl_train_token(self, data):
        row_max = 10
        for i in range(row_max):
            self.ui.tbl_train_token.setItem(i, 0, QTableWidgetItem(", ".join(data[i][0])))
            self.ui.tbl_train_token.setItem(i, 1, QTableWidgetItem(data[i][1]))

    def set_tbl_test_token(self, data):
        row_max = 10
        for i in range(row_max):
            self.ui.tbl_test_token.setItem(i, 0, QTableWidgetItem(", ".join(data[i][0])))
            self.ui.tbl_test_token.setItem(i, 1, QTableWidgetItem(data[i][1]))


if __name__ == "__main__":
    app = QApplication([])
    w = SAWidget()
    app.exec_()