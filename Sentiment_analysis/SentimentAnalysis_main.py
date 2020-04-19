from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem

class SAWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.train_data = []
        self.test_data = []
        self.train_path = ""
        self.test_path = ""
        self.ui = uic.loadUi("./SentimentAnalysis_UI.ui")
        self.ui.show()
        self.ui.btn_loading.clicked.connect(self.data_loading)

    def data_loading(self):
        self.train_path = self.ui.le_train_file.text()
        self.test_path = self.ui.le_test_file.text()
        try:
            self.train_data = self.read_documents(self.train_path)
            self.ui.tbl_train_data.clearContents()
            self.set_tbl_train_data(self.train_data)
            self.ui.ln_train_data.display(len(self.train_data))
        except:
            self.ui.tbl_train_data.clearContents()
            self.ui.tbl_train_data.setItem(0, 0, QTableWidgetItem("File Not Found"))
        try:
            self.test_data = self.read_documents(self.test_path)
            self.ui.tbl_test_data.clearContents()
            self.set_tbl_test_data(self.test_data)
            self.ui.ln_test_data.display(len(self.test_data))
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


if __name__ == "__main__":
    app = QApplication([])
    w = SAWidget()
    app.exec_()