from konlpy.tag import Mecab
import string
import re
import warnings
import pickle
from gensim import corpora, models
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TopicModelingWidget(QWidget):
    dictionary = []
    corpus = []
    tokenized_text = []

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./TopicModeling_UI.ui")
        self.ui.show()
        self.ui.btn_ma.clicked.connect(self.morph_analysis)
        self.ui.btn_tm.clicked.connect(self.topic_modeling)

    def morph_analysis(self):
        docs = read_doc(self.ui.le_file.text())
        cleaned_docs = text_clean(docs)
        self.tokenized_text = text_tokenize(cleaned_docs)
        self.set_ma_table(self.tokenized_text)


    def set_ma_table(self, text):
        row_max = len(text)
        col_max = 0
        for i in range(len(text)):
            for j in range(len(text[i])):
                if len(text[i]) > col_max:
                    col_max = len(text[i])
        self.ui.tbl_ma_result.setColumnCount(col_max)
        self.ui.tbl_ma_result.setRowCount(row_max)
        print("col: {} row: {}".format(col_max, row_max))

        for i in range(len(text)):
            for j in range(len(text[i])):
                self.ui.tbl_ma_result.setItem(i, j, QTableWidgetItem(text[i][j]))
        self.ui.tbl_ma_result.resizeColumnsToContents()
        self.ui.tbl_ma_result.resizeRowsToContents()


    def build_doc_term_mat(self, docs):
        self.dictionary = corpora.Dictionary(docs)
        self.corpus = [self.dictionary.doc2bow(text) for text in docs]


    def topic_modeling(self):
        self.build_doc_term_mat(self.tokenized_text)
        model = models.ldamodel.LdaModel(self.corpus, num_topics=int(self.ui.le_topics.text()),
                                         id2word=self.dictionary, alpha='auto', eta='auto')
        self.set_tm_table(model)


    def set_tm_table(self, model):
        col_max = model.num_topics
        row_max = int(self.ui.le_words.text())
        self.ui.tbl_tm_result.setColumnCount(col_max)
        self.ui.tbl_tm_result.setRowCount(row_max)

        for j in range(model.num_topics):
            topic_word_prob = model.show_topic(j, row_max)
            for i, word_prob in enumerate(topic_word_prob):
                item = "{}({})".format(word_prob[0], word_prob[1])
                print(item)
                self.ui.tbl_tm_result.setItem(i, j, QTableWidgetItem(item))
        self.ui.tbl_tm_result.resizeColumnsToContents()
        self.ui.tbl_tm_result.resizeRowsToContents()


def read_doc(input_file_name):
    corpus = []

    with open(input_file_name, "rb") as f:
        temp_corpus = pickle.load(f)
    for page in temp_corpus:
        corpus += page

    return corpus


def text_clean(docs):
    for doc in docs:
        doc = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힇 ]", "", doc)

    return docs


def define_stopwords(path):
    SW = set()

    for i in string.punctuation:
        SW.add(i)

    with open(path) as f:
        for word in f:
            SW.add(word)

    return SW


def text_tokenize(corpus):
    mecab = Mecab()
    token_corpus = []

    if w.ui.rb_noun.isChecked():
        for n in range(len(corpus)):
            token_text = mecab.nouns(corpus[n])
            token_text = [word for word in token_text if word not in SW]
            token_corpus.append(token_text)

    if w.ui.rb_morphs.isChecked():
        for n in range(len(corpus)):
            token_text = mecab.morphs(corpus[n])
            token_text = [word for word in token_text if word not in SW]
            token_corpus.append(token_text)

    if w.ui.rb_words.isChecked():
        for n in range(len(corpus)):
            token_text = corpus[n].split()
            token_text = [word for word in token_text if word not in SW]
            token_corpus.append(token_text)

    return token_corpus


SW = define_stopwords("./data/stop-word.txt")


if __name__ == "__main__":
    app = QApplication([])
    w = TopicModelingWidget()
    app.exec_()
