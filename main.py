import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.updateTableWidget()

    def updateTableWidget(self):
        result = self.cur.execute('SELECT * FROM Coffee, Degrees, GroudOrBean '
                                  'WHERE Coffee.degree = Degrees.ID AND GroudOrBean.ID = Coffee.groudOrBean').fetchall()
        result = [[i[0], i[1], i[8], i[10], i[4], i[5], i[6]] for i in result]

        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название', 'Степень обжарки', 'В зёрнах/Молотый',
                                                    'Описание', 'Цена', 'Объём(мл)'])
        self.tableWidget.setRowCount(0)

        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())