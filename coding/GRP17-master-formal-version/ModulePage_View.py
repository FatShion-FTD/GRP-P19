from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from ModuleFrame1_View import moduleFrame1_view
from ModuleFrame1_Model import moduleFrame1_Model
from ModuleFrame_Delegate import moduleFrame_Deletagte
from upcomingEvent_View import upcomingEvent_view
from upcomingEvent_Model import upcomingEvent_Model
from CommonHelper import CommonHelper
# jump by creating new window
from ModulePage_Ctr import ModulePage_ctr
import dbController
import Login_View

import sys


class modulePage_view(QMainWindow):

    # jumping signal to controller - TBC
    # moduleModel = None
    moduleList = []
    moduleModel = moduleFrame1_Model()
    enterSessionPage_Signal = pyqtSignal()

    def __init__(self):
        super(modulePage_view, self).__init__()
        self.window = None


    def show(self):
       self.window.show()

    # TBC
    def hide(self):
        self.window.hide()

    def setMainWindow(self, mainWindow, logCtr):
        self.window = mainWindow
        #In order to get View in class logCtr
        self.logCtr = logCtr

        self.setupMyUI()

    def setupMyUI(self):
        # connect with Ctr
        self.modulePageCtr = ModulePage_ctr()
        self.modulePageCtr.setCtr(self, self.window)

        # build view, model, delegate
        self.Frame1 = moduleFrame1_view()
        #self.Frame1.listView.setAlternatingRowColors(True)
        #moduleModel = moduleFrame1_Model()
        moduleDelegate = moduleFrame_Deletagte()

        # connect signal of frame to this page
        self.Frame1.enterSessionPage_SignalToPage.connect(self.goSession)

        self.upcomingFrame = upcomingEvent_view()
        upcomingModel = upcomingEvent_Model()

        # set model and delegate for views
        
        self.Frame1.setupUi(self.window.moduleFrame1)
        #self.Frame1.listView.setModel(moduleModel)
        self.Frame1.listView.setItemDelegate(moduleDelegate)
        self.Frame1.refresh()
        #self.window.stackedWidget.addWidget(self.Frame1)
        self.upcomingFrame.setupUi(self.window.moduleFrame2)
        self.upcomingFrame.listView.setModel(upcomingModel)
        self.upcomingFrame.connectToRecord(self.window)
        self.window.stackedWidget.setCurrentIndex(0)

    def setupModel(self):
        # print(Login_View.userId)
        moduleName = dbController.GetTeacherInfo(Login_View.userId)
        # print(moduleName)
        for r in moduleName:
            self.moduleModel.listItemData.append(r[2])
            self.moduleList.append(r[2])
        #print(moduleModel.listItemData)
        self.Frame1.listView.setModel(self.moduleModel)
        return self.moduleModel.listItemData

    def goSession(self):
        # TODO: jump to the page
        self.enterSessionPage_Signal.emit()

# test code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = modulePage_view()
    mainWindow.show()
    CommonHelper.readQSS("resources/qss/mainwindow.qss",app)
    sys.exit(app.exec_())