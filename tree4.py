import os, sys, json
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from PyQt5 import QtCore
from urllib.error import HTTPError
import webbrowser

class MyWindow(QMainWindow):
    def __init__(self, txt):
        super().__init__()
        self.setGeometry(300,300,800,400)

        self.text = QPlainTextEdit(self)
        self.text.move(10,10)
        self.text.resize(800, 400)

        self.text.appendPlainText(txt)

class MyApp(QWidget):

    def __init__(self, url):
        super().__init__()
        self.initUI(url)

    def initUI(self, url):

        self.table = QTableWidget()

        self.table.setRowCount(0)
        self.table.setColumnCount(1)

        self.table.setColumnWidth(0, 800)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.openMenu)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table, 1)

        self.setLayout(vbox)

        try:
            headers = {'User-Agent': 'Chrome/66.0.3359.181'}
            req = Request(url, headers=headers)
            with urlopen(req) as f:
                bsObj = BeautifulSoup(f.read(), 'html.parser')
                self.extract(bsObj)
        except (Exception) as e:
            print(e)

        self.setWindowTitle('QTextEdit')
        self.setGeometry(300, 300, 800, 800)
        self.show()

    def extract(self, bsObj):
        nameList = bsObj.findAll("a")
        for name in nameList:
            if 'href' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("img")
        for name in nameList:
            if 'src' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("form")
        for name in nameList:
            if 'action' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("script")
        for name in nameList:
            if 'src' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("iframe")
        for name in nameList:
            if 'src' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("div")
        for name in nameList:
            if 'src' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("frame")
        for name in nameList:
            if 'src' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

        nameList = bsObj.findAll("embed")
        for name in nameList:
            if 'src' in name.attrs:
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(name.prettify()))

    def openMenu(self, position):
        mdlIdx = self.table.indexAt(position)
        if not mdlIdx.isValid():
            return
        item = self.table.itemFromIndex(mdlIdx)

        right_click_menu = QMenu()

        act_add = right_click_menu.addAction(self.tr("크롤링"))
        act_add.triggered.connect(partial(self.large, item.text()))

        right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def large(self, text):
        self.mywindow = MyWindow(text)
        self.mywindow.show()

class view(QMainWindow):

    def __init__(self):
        super(view, self).__init__()
        self.InitTree()
        self.InitMenu()
        self.InitEdit()
        self.InitSaved()

        self.model.setRowCount(0)

    def InitTree(self):
        self.tree = QTreeView()
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Url', 'Status'])

        self.tree.header().setDefaultSectionSize(180)

        self.tree.setModel(self.model)

        self.tree.setColumnWidth(0, 600)
        self.tree.setColumnWidth(1, 50)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.layout = QVBoxLayout(centralWidget)
        self.layout.addWidget(self.tree)

        self.sublayout1 = QHBoxLayout()
        self.layout.addLayout(self.sublayout1)

        self.sublayout2 = QHBoxLayout()
        self.layout.addLayout(self.sublayout2)

    def InitMenu(self):

        clearAction = QAction('clear', self)
        clearAction.setShortcut('Ctrl+C')
        clearAction.setStatusTip('clear')
        clearAction.triggered.connect(self.action3_fun)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(clearAction)

    def InitEdit(self):
        self.lbl = QLabel('Url:')
        self.sublayout1.addWidget(self.lbl)

        self.qle = QLineEdit(self)
        self.sublayout1.addWidget(self.qle)

        self.btn = QPushButton('&Crawl', self)
        self.btn.setCheckable(True)
        self.btn.toggle()
        self.sublayout1.addWidget(self.btn)

        self.btn.clicked.connect(self.action4_fun)

    def InitSaved(self):
        self.lbl2 = QLabel('Saved File:')
        self.sublayout2.addWidget(self.lbl2)

        self.qle2 = QLineEdit(self)
        self.sublayout2.addWidget(self.qle2)

        self.btn2 = QPushButton('&Update', self)
        self.btn2.setCheckable(True)
        self.btn2.toggle()
        self.sublayout2.addWidget(self.btn2)

        self.btn2.clicked.connect(self.action5_fun)

    def openMenu(self, position):
        mdlIdx = self.tree.indexAt(position)
        if not mdlIdx.isValid():
            return
        item = self.model.itemFromIndex(mdlIdx)

        right_click_menu = QMenu()

        act_add = right_click_menu.addAction(self.tr("크롤링"))
        act_add.triggered.connect(partial(self.action1_fun, mdlIdx))

        act_add = right_click_menu.addAction(self.tr("브라우저"))
        act_add.triggered.connect(partial(self.action2_fun, mdlIdx))

        act_add = right_click_menu.addAction(self.tr("입력 요소"))
        act_add.triggered.connect(partial(self.action6_fun, mdlIdx))

        right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def extract(self, bsObj):
        with open(self.saved, 'a', encoding='utf-8') as a:
            nameList = bsObj.findAll("a")
            for name in nameList:
                if 'href' in name.attrs:
                    a.write(str(name.attrs['href']) + ' xxx' + '\n')

            nameList = bsObj.findAll("img")
            for name in nameList:
                if 'src' in name.attrs:
                    a.write(str(name.attrs['src']) + ' xxx' + '\n')

            nameList = bsObj.findAll("form")
            for name in nameList:
                if 'action' in name.attrs:
                    a.write(str(name.attrs['action']) + ' xxx' + '\n')

            nameList = bsObj.findAll("script")
            for name in nameList:
                if 'src' in name.attrs:
                    a.write(str(name.attrs['src']) + ' xxx' + '\n')

            nameList = bsObj.findAll("iframe")
            for name in nameList:
                if 'src' in name.attrs:
                    a.write(str(name.attrs['src']) + ' xxx' + '\n')

            nameList = bsObj.findAll("div")
            for name in nameList:
                if 'src' in name.attrs:
                    a.write(str(name.attrs['src']) + ' xxx' + '\n')

            nameList = bsObj.findAll("frame")
            for name in nameList:
                if 'src' in name.attrs:
                    a.write(str(name.attrs['src']) + ' xxx' + '\n')

            nameList = bsObj.findAll("embed")
            for name in nameList:
                if 'src' in name.attrs:
                    a.write(str(name.attrs['src']) + ' xxx' + '\n')

    def crawlurl(self, url):
        headers = {'User-Agent':'Chrome/66.0.3359.181'}
        req = Request(url, headers=headers)
        try:
            with urlopen(req) as f:
                bsObj = BeautifulSoup(f.read(), 'html.parser')
        except (Exception) as e:
            raise e

        try:
            self.extract(bsObj)
            self.saved_to_tree(self.saved)
        except (Exception) as e:
            print(e)
            return

    def saved_to_tree(self, file):
        q = re.compile('^/')
        try:
            with open(file, 'r', encoding='utf-8') as a:
                list = a.readlines()
                for line in list:
                    if q.match(line):
                        line = self.domain + line
                    self.appendurl(line)
            self.tree.expandAll()
        except (Exception) as e:
            print(e)
            return

    def appendurl(self, url):

        crawled = url.split()[-1]

        url = url[:-4]

        url = url.strip()

        self.discovery = 1

        store = url

        p = re.compile('^https?://$')

        q = re.compile('^https?://')

        root = self.model.invisibleRootItem()

        parent = root

        if not q.match(url):
            row = -1
            if parent.rowCount() == 0:
                parent.appendRow([
                    QStandardItem(url),
                    QStandardItem(crawled)
                ])
                if crawled == '200':
                    parent.child(row, 0).setBackground(QColor(225, 225, 225))
                elif crawled == 'xxx':
                    pass
                else:
                    parent.child(row, 0).setBackground(QColor(225, 0, 0))
                return

            for row in range(0, parent.rowCount()):
                if parent.child(row, 0).text() == url:
                    break

            if row == parent.rowCount() - 1 and parent.child(row, 0).text != url:
                parent.appendRow([
                    QStandardItem(url),
                    QStandardItem(crawled)
                ])
                if crawled == '200':
                    parent.child(row, 0).setBackground(QColor(225, 225, 225))
                elif crawled == 'xxx':
                    pass
                else:
                    parent.child(row, 0).setBackground(QColor(225, 0, 0))
            return

        list = self.spliturl(url)

        while parent.hasChildren() and list:

            line = list.pop()

            temp = parent.rowCount()

            row = -1
            oldparent = parent

            for row in range(0, temp):
                child = parent.child(row, 0)
                oldparent = parent
                if line == child.text():
                    parent = parent.child(row, 0)
                    break
            if row == temp - 1 and oldparent == parent:
                list = self.spliturl(store)
                if parent.text() not in list:
                    self.puturl(parent, list, crawled)
                else:
                    self.puturl(parent, list[:list.index(parent.text())], crawled)
                break

        if not parent.hasChildren() and list:
            list = self.spliturl(store)

            if parent.text() not in list:
                self.puturl(parent, list, crawled)
            else:
                self.puturl(parent, list[:list.index(parent.text())], crawled)

    def spliturl(self, url):
        p = re.compile('^https?://$')

        list = []

        while True:
            list.append(url)
            end = url.rfind('/')
            if p.match(url[:end+1]):
                break
            else:
                url = url[:url.rfind('/')]
        return list

    def puturl(self, parent, list, crawled):
        while True:
            if len(list):
                parent.appendRow([
                    QStandardItem(list.pop()),
                    QStandardItem(crawled)
                ])
                parent = parent.child(parent.rowCount() - 1)

                if crawled == '200':
                    parent.setBackground(QColor(225, 225, 225))
                elif crawled == 'xxx':
                    pass
                else:
                    parent.setBackground(QColor(225, 0, 0))
            else:
                break
        self.discovery = 0

    def iterItems(self, root):
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        yield child
                        if child.hasChildren():
                            stack.append(child)

    def transverse_tree(self):
        item_list = []
        root = self.model.invisibleRootItem()
        for item in self.iterItems(root):
            item_list.append(item.text())

        return item_list

    def closeEvent(self, event):

        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Sure?",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:

            tree_list = self.transverse_tree()

            with open(self.saved, 'w', encoding='utf-8') as f:
                for i in range(0, len(tree_list), 2):
                    f.write(tree_list[i] + ' ' + tree_list[i+1] + '\n')

            event.accept()

        else:
            event.ignore()

    def action1_fun(self, mdlIdx):
        item = self.model.itemFromIndex(mdlIdx)
        item.setBackground(QColor(225, 225, 225))

        try:
            with open(self.saved, 'a', encoding='utf-8') as a:
                a.write(item.text() + ' xxx' + '\n')
        except (Exception) as e:
            print(e)
            return

        try:
            self.crawlurl(item.text())
        except (HTTPError) as e1:
            row = item.row()
            parent = item.parent()
            parent.child(row, 1).setText(str(e1.code))
            item.setBackground(QColor(225, 0, 0))
        except (Exception) as e2:
            item.setBackground(QColor(225, 0, 0))
        else:
            row = item.row()
            parent = item.parent()

            if parent == None:
                parent = self.model.invisibleRootItem()

            parent.child(row, 1).setText('200')

    def action2_fun(self, mdlIdx):
        item = self.model.itemFromIndex(mdlIdx)

        try:
            webbrowser.open(item.text())
        except(Exception) as e:
            return

    def action3_fun(self):
        self.model.setRowCount(0)

    def action4_fun(self):
        self.model.setRowCount(0)

        text = self.qle.displayText()

        r = re.compile('^https?://.+\.((com)|(net)|(org))')

        self.domain = r.search(text).group()

        self.crawlurl(text)

    def action5_fun(self):
        self.model.setRowCount(0)
        self.saved = self.qle2.displayText()
        if os.path.isfile(self.saved):
            self.saved_to_tree(self.saved)
        self.statusBar().showMessage(self.saved)

    def action6_fun(self, mdlIdx):
        item = self.model.itemFromIndex(mdlIdx)
        self.ex = MyApp(item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = view()

    view.setGeometry(300, 100, 800, 800)
    view.setWindowTitle('My site-mapping tool')
    view.show()
    sys.exit(app.exec_())

