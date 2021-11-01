#!/usr/bin/env python
# coding=utf-8

import sys
import time

from PyQt5.QtCore import QDir
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.mainUi import Ui_MainWindow
from PassBrup import PassBrup


class ZipExtrator(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ZipExtrator, self).__init__()
        self.setupUi(self)
        self.passBrup = PassBrup(zipFilePath="", passDicPath="")
        self.passBrup.signal_log.connect(self.writeLog)
        self.passBrup.signal_over.connect(self.endBrup)

    # 绑定选择zip文件事件
    def zipFileOpen(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取zip文件", QDir.currentPath(), "ZIP Files (*.zip)")
        self.lineEdit.setText(fileName)

    # 绑定选择字典文件事件
    def passDictFileOpen(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取字典文件", QDir.currentPath(), "Text Files (*.txt)")
        self.lineEdit_2.setText(fileName)

    def startBrup(self):
        self.textEdit.setText("")
        zipFilePath = self.lineEdit.text()
        dictFilePath = self.lineEdit_2.text()
        if zipFilePath == "" or dictFilePath == "":
            self.textEdit.insertHtml("<font color='#FF0000' size='4'>提示：请选择文件</font>")
            return
        else:
            self.writeLog("<font color='#0000FF' size='4'>开始爆破（开始时间为：{0}）</font>".format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            self.pushButton.setEnabled(False)
            self.passBrup.passDicPath = dictFilePath
            self.passBrup.zipFilePath = zipFilePath
            self.passBrup.start()

    def endBrup(self, log):
        self.writeLog(log)
        self.pushButton.setEnabled(True)

    def writeLog(self, log):
        log = log + "<br>"
        self.textEdit.insertHtml(log)
        self.textEdit.moveCursor(QTextCursor.End)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ZipExtrator()
    form.show()
    sys.exit(app.exec_())
