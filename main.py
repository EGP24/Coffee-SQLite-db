import sys

from PyQt5 import uic
from addCoffeeForm import Ui_Dialog as addCoffeeForm
from editCoffeeForm import Ui_Dialog as editCoffeeForm
from mainForm import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
import sqlite3


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.updateTableWidget()
        self.pushButton1.clicked.connect(self.onClicked)
        self.pushButton2.clicked.connect(self.onClicked)

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

    def onClicked(self):
        if self.sender().text() == 'Добавить':
            self.addCoffeeDialog = AddCoffeeDialog(self.tableWidget, self.updateTableWidget)
            self.addCoffeeDialog.exec()

        if self.sender().text() == 'Редактировать':
            try:
                selected = [self.tableWidget.
                                item(list(self.tableWidget.selectionModel().
                                          selectedRows())[-1].row(), j).text() for j in range(7)]
                self.editCoffeeDialog = EditCoffeeDialog(self.tableWidget, self.updateTableWidget, *selected)
                self.editCoffeeDialog.exec()
            except IndexError:
                QMessageBox.critical(None, 'Ошибка', 'Выберите кофе', QMessageBox.Ok)
            except Exception as e:
                print(e)
                QMessageBox.critical(None, 'Ошибка', 'Что-то пошло не так', QMessageBox.Ok)


class AddCoffeeDialog(QDialog, addCoffeeForm):
    def __init__(self, tableWidget, updateTableWidget):
        super().__init__()
        self.setupUi(self)

        self.tableWidget = tableWidget
        self.updateTableWidget = updateTableWidget
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.pushButton.clicked.connect(self.onClicked)

    def onClicked(self):
        title = self.lineEdit.text()
        degree = self.cur.execute(f'SELECT ID FROM Degrees '
                                  f'WHERE title="{self.comboBox1.currentText()}"').fetchall()[0][0]
        groudOrBean = self.cur.execute(f'SELECT ID FROM GroudOrBean '
                                       f'WHERE title="{self.comboBox2.currentText()}"').fetchall()[0][0]
        price = self.spinBox1.value()
        size = self.spinBox2.value()
        description = self.plainTextEdit.toPlainText()
        try:
            assert title and price and size and description

            self.cur.execute(f'INSERT INTO Coffee(title,degree,groudOrBean,price,size,description) '
                             f'VALUES("{title}",{degree},{groudOrBean},{price},{size},"{description}")')
            self.con.commit()
            self.updateTableWidget()
            self.close()
        except AssertionError:
            QMessageBox.critical(None, 'Ошибка', 'Заполните все поля', QMessageBox.Ok)
        except:
            QMessageBox.critical(None, 'Ошибка', 'Что-то пошло не так', QMessageBox.Ok)


class EditCoffeeDialog(QDialog, editCoffeeForm):
    def __init__(self, tableWidget, updateTableWidget, ID, title, degree, groudOrBean, description, price, size):
        super().__init__()
        self.setupUi(self)

        self.ID = ID
        self.tableWidget = tableWidget
        self.updateTableWidget = updateTableWidget
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.pushButton.clicked.connect(self.onClicked)
        self.lineEdit.setText(title)
        self.comboBox1.setCurrentText(degree)
        self.comboBox2.setCurrentText(groudOrBean)
        self.spinBox1.setValue(int(price))
        self.spinBox2.setValue(int(size))
        self.plainTextEdit.setPlainText(description)

    def onClicked(self):
        title = self.lineEdit.text()
        degree = self.cur.execute(f'SELECT ID FROM Degrees '
                                  f'WHERE title="{self.comboBox1.currentText()}"').fetchall()[0][0]
        groudOrBean = self.cur.execute(f'SELECT ID FROM GroudOrBean '
                                       f'WHERE title="{self.comboBox2.currentText()}"').fetchall()[0][0]
        price = self.spinBox1.value()
        size = self.spinBox2.value()
        description = self.plainTextEdit.toPlainText()
        try:
            assert title and price and size and description

            self.cur.execute(f'UPDATE Coffee SET title="{title}", degree={degree}, '
                             f'groudOrBean={groudOrBean}, price={price}, size={size}, description="{description}" '
                             f'WHERE ID={self.ID}')
            self.con.commit()
            self.updateTableWidget()
            self.close()
        except AssertionError:
            QMessageBox.critical(None, 'Ошибка', 'Заполните все поля', QMessageBox.Ok)
        except:
            QMessageBox.critical(None, 'Ошибка', 'Что-то пошло не так', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())