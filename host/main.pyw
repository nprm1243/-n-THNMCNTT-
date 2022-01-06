# -*- coding: utf-8 -*-

import sys, os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

import mysql.connector as mysql

import dotenv
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dotenv_file = dotenv.find_dotenv()
load_dotenv()
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

dataInGenre = ['']
dataInSubGenre = ['']
databaseConnection = False

try:
    database = mysql.connect(
        host = HOST,
        user = USER,
        passwd = PASSWORD
    )

    databaseConnection = True

    cursor = database.cursor()
    query = "SELECT * FROM marknice.host_data"
    cursor.execute(query)
    records = cursor.fetchall()

    for record in records:
        if (record[2] not in dataInGenre):
            dataInGenre.append(record[2])
        if (record[3] not in dataInSubGenre):
            dataInSubGenre.append(record[3])
    dataInGenre.sort()
    dataInSubGenre.sort()

    database.close()
except:
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("marknice.ui", self)
        for i, item in enumerate(dataInGenre):
            self.genre.addItem("")
            self.genre.setItemText(i, QtCore.QCoreApplication.translate("MainWindow", str(item)))
        for i, item in enumerate(dataInSubGenre):
            self.subGenre.addItem("")
            self.subGenre.setItemText(i, QtCore.QCoreApplication.translate("MainWindow", str(item)))
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(5,150)

        #event_main
        self.pushButton.clicked.connect(self.process)

        #event_toolbar
        self.menuSetting.triggered.connect(self.toConnectionSetting)
        self.actionT_t_c_s_ch.triggered.connect(self.toAllDataset)
        self.actionMysql_editor.triggered.connect(self.toMySQLEditor)
    
    def process(self):
        try:
            query = "SELECT * FROM marknice.host_data"
            needAnd = False
            if (self.keyWords.text() != ''):
                if (needAnd == False):
                    query += " WHERE"
                query += f" Title LIKE '%{self.keyWords.text()}%'"
                needAnd = True
            if (self.genre.currentText() != ''):
                if (needAnd == False):
                    query += " WHERE"
                if (needAnd):
                    query += ' AND'
                query += f" Genre = '{self.genre.currentText()}'"
                needAnd = True
            if (self.subGenre.currentText() != ''):
                if (needAnd == False):
                    query += " WHERE"
                if (needAnd):
                    query += ' AND'
                query += f" SubGenre = '{self.subGenre.currentText()}'"
                needAnd = True
            if (self.author.text() != ''):
                if (needAnd == False):
                    query += " WHERE"
                if (needAnd):
                    query += ' AND'
                query += f" Author LIKE '%{self.author.text()}%'"
                needAnd = True
            if (self.publisher.text() != ''):
                if (needAnd == False):
                    query += " WHERE"
                if (needAnd):
                    query += ' AND'
                query += f" Publisher LIKE '%{self.publisher.text()}%'"
                needAnd = True
            if (int(self.pages.text()) != 0):
                if (needAnd == False):
                    query += " WHERE"
                if (needAnd):
                    query += ' AND'
                query += f" (Height >= {max(0, int(self.pages.text())) - int(self.delta.text())} AND Height <= {int(self.pages.text()) + int(self.delta.text())})"
                needAnd = True
            print(query)
            database = mysql.connect(
                host = HOST,
                user = USER,
                passwd = PASSWORD
            )
            _cursor = database.cursor()
            _cursor.execute(query)
            _records = _cursor.fetchall()
            database.close()
            result = []
            for record in _records:
                tmp = {}
                tmp['Tựa sách'] = record[0]
                tmp['Thể loại'] = record[2]
                tmp['Thể loại phụ'] = record[3]
                tmp['Tác giả'] = record[1]
                tmp['Số trang'] = record[4]
                tmp['Nhà xuất bản'] = record[5]
                result.append(tmp)
            #print(result)
            row = 0
            self.tableWidget.setRowCount(len(result))
            for item in result:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item["Tựa sách"]))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item["Thể loại"]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(item["Thể loại phụ"]))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item["Tác giả"]))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item["Số trang"])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(item["Nhà xuất bản"]))
                row = row + 1
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Đã xảy ra lỗi!")
            msg.setInformativeText("Bạn chưa kết nối tới bất kỳ Mysql server nào!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def toConnectionSetting(self):
        widget.setCurrentWidget(connectionSetting)

    def toAllDataset(self):
        widget.setCurrentWidget(allDataset)

    def toMySQLEditor(self):
        widget.setCurrentWidget(mysqleditor)

class ConnectionSetting(QMainWindow):
    def __init__(self):
        super(ConnectionSetting, self).__init__()
        loadUi("marknice_setting.ui", self)
        if (databaseConnection):
            self.listWidget.clear()
            self.listWidget.addItem(QtWidgets.QListWidgetItem(f'{HOST} | {USER}'))

        #event_main
        self.pushButton.clicked.connect(self.connectToSQLServer)

        #event_toolbar
        self.actionMain.triggered.connect(self.toMain)
        self.actionT_t_c_s_ch.triggered.connect(self.toAllDataset)

    def connectToSQLServer(self):
        print("ketnoi")
        print(f'{self.lineEdit.text()} {self.lineEdit_2.text()} {self.lineEdit_3.text()}')
        global database 
        try:
            database = mysql.connect(
                host = self.lineEdit.text(),
                user = self.lineEdit_2.text(),
                passwd = self.lineEdit_3.text()
            )

            os.environ["HOST"] = self.lineEdit.text()
            os.environ["USER"] = self.lineEdit_2.text()
            os.environ["PASSWORD"] = self.lineEdit_3.text()
            dotenv.set_key(dotenv_file, "HOST", os.environ["HOST"])
            dotenv.set_key(dotenv_file, "USER", os.environ["USER"])
            dotenv.set_key(dotenv_file, "PASSWORD", os.environ["PASSWORD"])
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Đã kết nối đến Mysql server thành công!")
            msg.setInformativeText("Bạn vui lòng restart lại phần mềm để cập nhật những nội dung mới.")
            msg.setWindowTitle("Message")
            msg.exec_()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Đã xảy ra lỗi!")
            msg.setInformativeText("Không thể kết nối đến Mysql server!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def toMain(self):
        widget.setCurrentWidget(mainwindow)
    
    def toAllDataset(self):
        widget.setCurrentWidget(allDataset)

class AllDataset(QMainWindow):
    def __init__(self):
        super(AllDataset, self).__init__()
        loadUi("all_book.ui", self)
        self.bookTable.setColumnWidth(0,250)
        self.bookTable.setColumnWidth(5,150)
        self.window_1 = plotting()

        #event main
        self.pushButton.clicked.connect(self.process)
 
        #event toolbar
        self.actionTra_c_u_s_ch.triggered.connect(self.toMain)
        self.actionConnection.triggered.connect(self.toConnectionSetting)

    def process(self):
        database = mysql.connect(
            host = HOST,
            user = USER,
            passwd = PASSWORD
        )
        query = "SELECT * FROM marknice.host_data"
        needAnd = False
        #try:
        if (self.comboBox_2.currentText() == 'Có'):
            if (needAnd == False):
                query += " WHERE"
            if (needAnd):
                query += ' AND'
            needAnd = True
            query += " Author NOT LIKE ''"
        if (self.comboBox_2.currentText() == 'Không'):
            if (needAnd == False):
                query += " WHERE"
            if (needAnd):
                query += ' AND'
            needAnd = True
            query += " Author LIKE ''"
        if (self.comboBox_3.currentText() == 'Có'):
            if (needAnd == False):
                query += " WHERE"
            if (needAnd):
                query += ' AND'
            needAnd = True
            query += " Publisher NOT LIKE ''"
        if (self.comboBox_3.currentText() == 'Không'):
            if (needAnd == False):
                query += " WHERE"
            if (needAnd):
                query += ' AND'
            needAnd = True
            query += " Publisher LIKE ''"
        _cursor = database.cursor()
        _cursor.execute(query)
        _records = _cursor.fetchall()
        database.close()
        result = []
        listToDF = {'Tựa sách' : [], 'Thể loại' : [], 'Thể loại phụ' : [], 'Tác giả' : [], 'Số trang' : [], 'Nhà xuất bản' : []}
        for record in _records:
            listToDF["Tựa sách"].append(record[0])
            listToDF["Thể loại"].append(record[2])
            listToDF["Thể loại phụ"].append(record[3])
            listToDF["Tác giả"].append(record[1])
            listToDF["Số trang"].append(record[4])
            listToDF["Nhà xuất bản"].append(record[5])
        df = pd.DataFrame(listToDF)
        if self.checkBox.isChecked():
            df = df.sort_values(by = str(self.comboBox.currentText()), ascending = False)
        else:
            df = df.sort_values(by = str(self.comboBox.currentText()))
        self.bookTable.setRowCount(len(listToDF["Tựa sách"]))
        for row, item in enumerate(listToDF["Tựa sách"]):
            self.bookTable.setItem(row, 0, QtWidgets.QTableWidgetItem(df.iloc[row][0]))
            self.bookTable.setItem(row, 1, QtWidgets.QTableWidgetItem(df.iloc[row][1]))
            self.bookTable.setItem(row, 2, QtWidgets.QTableWidgetItem(df.iloc[row][2]))
            self.bookTable.setItem(row, 3, QtWidgets.QTableWidgetItem(df.iloc[row][3]))
            self.bookTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(df.iloc[row][4])))
            self.bookTable.setItem(row, 5, QtWidgets.QTableWidgetItem(df.iloc[row][5]))
        if (self.checkBox_2.isChecked()):
            self.window_1.show()
            visualization_data.barChart(df)
            visualization_data.pieChart(df)
            visualization_data.scatterPlot(df)
            pixmap = QtGui.QPixmap('bar.png')
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.window_1.plotView.setScene(scene)
        #except:
        #    msg = QtWidgets.QMessageBox()
        #    msg.setIcon(QtWidgets.QMessageBox.Information)
        #    msg.setText("Đã xảy ra lỗi!")
        #    msg.setInformativeText("Bạn chưa kết nối tới bất kỳ Mysql server nào!")
        #    msg.setWindowTitle("Error")
        #    msg.exec_()

    def toMain(self):
        widget.setCurrentWidget(mainwindow)
    
    def toConnectionSetting(self):
        widget.setCurrentWidget(connectionSetting)
        
class plotting(QMainWindow):
    def __init__(self):
        super(plotting, self).__init__()
        loadUi("plot.ui", self)

        #event main
        self.plotComboBox.currentIndexChanged.connect(self.process)
    
    def process(self):
        if (self.plotComboBox.currentText() == 'Biểu đồ cột'):
            pixmap = QtGui.QPixmap('bar.png')
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.plotView.setScene(scene)
        elif (self.plotComboBox.currentText() == 'Biểu đồ tròn'):
            pixmap = QtGui.QPixmap('pie.png')
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.plotView.setScene(scene)
        else:
            pixmap = QtGui.QPixmap('scatter.png')
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.plotView.setScene(scene)

class visualization_data():
    def __init__(self):
        pass

    def barChart(df):
        genre = df["Thể loại"]
        labels = ['tech','science','nonfiction','fiction','philosophy']
        fig = plt.figure(figsize=(8, 5))
        plt.hist(genre)
        fig.figure.savefig("bar.png",dpi=100)
        pass

    def pieChart(df):
        genre = df["Thể loại"]
        dem = []
        labels = []
        for item in genre:
            if (item not in labels):
                labels.append(item)
                dem.append(1)
            else:
                dem[labels.index(item)] += 1
        fig = plt.figure(figsize=(8, 5))
        plt.pie(dem, labels = labels, autopct= '%1.1f%% \n')
        fig.figure.savefig("pie.png",dpi=100)
        pass

    def scatterPlot(df):
        pair = []
        dem = []
        Genre = df["Thể loại"]
        SubGenre = df["Thể loại phụ"]
        for i in range(len(Genre)):
            tmp = [Genre[i], SubGenre[i]]
            if (tmp in pair):
                dem[pair.index(tmp)] += 1
            else:
                pair.append(tmp)
                dem.append(1)
        Genre = []
        SubGenre = []
        for item in pair:
            Genre.append(item[0])
            SubGenre.append(item[1])
        df = pd.DataFrame({"Genre" : Genre, "SubGenre" : SubGenre, "Count" : dem})
        sns.set_style("whitegrid")
        plt.figure(figsize = (8, 6))
        sns_plot = sns.scatterplot(data = df, x = 'Genre', y = 'SubGenre', size = 'Count', sizes = (20, 200))
        sns_plot.figure.savefig("scatter.png", dpi = 100)
        pass

class mySQLEditor(QMainWindow):
    def __init__(self):
        super(mySQLEditor, self).__init__()
        loadUi("mysqleditor.ui", self)

        #event main
        self.runButton.clicked.connect(self.execute)
        self.actiontracuu.triggered.connect(self.toMain)

    def toMain(self):
        widget.setCurrentWidget(mainwindow)

    def execute(self):
        database = mysql.connect(
            host = HOST,
            user = USER,
            passwd = PASSWORD
        )
        query = self.code.toPlainText()
        _cursor = database.cursor()
        _cursor.execute(query)
        _records = _cursor.fetchall()
        database.close()
        print(_records)
        if (len(_records) > 0):
            columns = len(_records[0])
            self.result.setColumnCount(columns)
            self.result.setRowCount(len(_records))
            for row, record in enumerate(_records):
                for i in range(columns):
                    self.result.setItem(row, i, QtWidgets.QTableWidgetItem(str(record[i])))
        pass

app = QApplication(sys.argv)

mainwindow = MainWindow()
connectionSetting = ConnectionSetting()
allDataset = AllDataset()
plottingScreen = plotting()
mysqleditor = mySQLEditor()
widget = QtWidgets.QStackedWidget()

widget.addWidget(mainwindow)
widget.addWidget(connectionSetting)
widget.addWidget(allDataset)
widget.addWidget(plottingScreen)
widget.addWidget(mysqleditor)

widget.setFixedHeight(500)
widget.setFixedWidth(880)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")