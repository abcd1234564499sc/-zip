#!/usr/bin/env python
# coding=utf-8
import time
import zipfile

from PyQt5.QtCore import QThread, pyqtSignal


class PassBrup(QThread):
    signal_log = pyqtSignal(str)
    signal_over = pyqtSignal(str)

    def __init__(self, zipFilePath="", passDicPath="", parent=None):
        super(PassBrup, self).__init__(parent)
        self.zipFilePath = zipFilePath
        self.passDicPath = passDicPath

    def run(self):
        # 读取字典
        with open(self.passDicPath, "r") as fr:
            passList = [p.replace("\r\n", "\n").replace("\n", "") for p in fr.readlines()]
        zFile = zipfile.ZipFile(self.zipFilePath, "r")
        ifFindFlag = False
        for index, passStr in enumerate(passList):
            if index % 500 == 0 and index != 0:
                echoStr = "<font color='#0000FF' size='4'>前{0}个密码未爆破成功</font>".format(index)
                self.signal_log.emit(echoStr)
                # time.sleep(2)
                pass
            else:
                pass
            try:
                zFile.extractall(path="./", pwd=passStr.encode())
            except RuntimeError:
                # echoStr = "<font color='#0000FF' size='4'>（{1}/{2}）</font><font color='#0000FF' size='4'>测试密码：{0}</font>".format(
                #     passStr, index + 1, len(passList))
                pass
            except Exception as ex:
                # echoStr = "<font color='#0000FF' size='4'>（{1}/{2}）</font><font color='#FF0000' size='4'>异常密码：{0}，异常为{3}</font>".format(
                #     passStr, index + 1, len(passList), str(ex))
                # self.signal_log.emit(echoStr)
                pass
            else:
                echoStr = "<font color='#0000FF' size='4'>（{1}/{2}）</font><font color='#17C37B' size='4'>找到密码：{0}</font>".format(
                    passStr, index + 1, len(passList))
                self.signal_log.emit(echoStr)
                ifFindFlag = True
                break
        if not ifFindFlag:
            echoStr = "<font color='#0000FF' size='4'>已遍历所有 {0} 个密码，未爆破成功</font>".format(len(passList))
        else:
            echoStr = "<font color='#0000FF' size='4'>爆破成功</font>".format(len(passList))
        self.signal_over.emit(echoStr)
