from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import sys
import threading
import time
import os
import pyshark

getTopic = 1
def getTopics():
    global getTopic
    while getTopic == 1:
    	pass

topicThread = threading.Thread(target=getTopics)
topicThread.start()
topics = []
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        global topics
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('GenericLayout.ui', self) # Load the .ui file
        self.graphLayout = self.findChild(QtWidgets.QVBoxLayout, 'graphLayout')
        #self.topicCombo = self.findChild(QtWidgets.QComboBox, 'topicComboBox')
        #self.topicCombo.addItem("All")
        #self.topics = topics
        #self.FillTopics()
        
        self.pushButton = self.findChild(QtWidgets.QPushButton, "pushButton") 
        self.pushButton.clicked.connect(self.changelabeltext)

        
        #print("Current value of topc combo box is : " + self.topicCombo.currentText())
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        self.graphLayout.addWidget(self.graphWidget)
        self.show() # Show the GUI
        
    def FillTopics(self):
        global topics
        for topic in topics:
            self.topicCombo.addItem(topic)
    def changelabeltext(self): 
        self.hourTextEdit = self.findChild(QtWidgets.QTextEdit, 'hourTextEdit')
        try:
            hourInput = int(self.hourTextEdit.toPlainText())
        except:
            hourInput = 0
        self.minTextEdit = self.findChild(QtWidgets.QTextEdit, 'minTextEdit')
        try:
            minInput = int(self.minTextEdit.toPlainText())
        except:
            minInput = 0
        self.secTextEdit = self.findChild(QtWidgets.QTextEdit, 'secTextEdit')
        try:
            secInput = int(self.secTextEdit.toPlainText())
        except:
            secInput = 0
        secs = 60*60*hourInput + 60*minInput + secInput

        self.topicName = self.findChild(QtWidgets.QLineEdit, 'topicLineEdit')
        
        topic = 1
        if self.topicName.text() == "All":
            topic = 0
            
        #rtps.param.topicName == " "
        print("Running for : " + str(secs) + " seconds.")
        print("Beginning capture!\n")
        os.system("touch test.pcap")
        os.system("sudo chmod o=rw test.pcap")
        command  = 'sudo tshark -ni any -w test.pcap -a duration:' + str(secs)
        os.system(command)
        if topic == 1:
            f ='rtps.param.topicName == ' + self.topicName.text()
            cap = pyshark.FileCapture('test.pcap', display_filter=f)
            print("Capturing topic: " + f)
        else:
            print("Capturing topic: All")
            cap = pyshark.FileCapture('test.pcap')
        out_file = open("Eavesdrop_Data.txt", "w")
        for pkt in cap:
            out_file.write(str(pkt))

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
getTopic = 0
topicThread.join()
print ("Exiting Main Thread")
