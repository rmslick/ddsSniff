from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import sys
import threading
import time

getTopic = 1
def getTopics():
    global getTopic
    while getTopic == 1:
    	print("running")

topicThread = threading.Thread(target=getTopics)
topicThread.start()
topics = []
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        global topics
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('GenericLayout.ui', self) # Load the .ui file
        self.graphLayout = self.findChild(QtWidgets.QVBoxLayout, 'graphLayout')
        self.topicCombo = self.findChild(QtWidgets.QComboBox, 'topicComboBox')
        self.topicCombo.addItem("All")
        self.topics = topics
        self.FillTopics()
        print("Current value of topc combo box is : " + self.topicCombo.currentText())
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        self.graphLayout.addWidget(self.graphWidget)
        self.show() # Show the GUI
        
    def FillTopics(self):
        global topics
        for topic in topics:
            self.topicCombo.addItem(topic)
            
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
getTopic = 0
topicThread.join()
print ("Exiting Main Thread")
