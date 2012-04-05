#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui,QtWebKit
import pytos.util.NescApp as NescApp
import pytos.util.ParseArgs as ParseArgs
import math
import random

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.app = NescApp.NescApp("./build/telosb/","sf@localhost:9002", tosbase=False, localCommOnly=True)
        self.gwidget=GraphWidget(self)
        self.setCentralWidget(self.gwidget)       
        self.printer = QtGui.QPrinter()
        self.currentNodeID=1
        self.createActions()
        self.createMenus()
        self.createDockWindows()
		
	self.flag=0#if you have not open the map or draw node it is 0.every node you draw, it will ++ 
        self.setWindowTitle("VisualControl")
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.resize(1000, 600)
    def setCurrentNodeID(self):
    	strID=self.app.Globals.TOS_NODE_ID.peek()
    	strID_=str(strID)
    	strID__=strID_.split(":")[-1]
    	strID___=strID__.split("\n")[0]
    	strID____=strID___.strip()
    	intID=int(strID____)
    	self.currentNodeID=intID
    def print_(self):
    	dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)
    
    def about(self):
        QtGui.QMessageBox.about(self, "About Dock Widgets",
                "The <b>Dock Widgets</b> example demonstrates how to use "
                "Qt's dock widgets. You can enter your own text, click a "
                "customer to add a customer name and address, and click "
                "standard paragraphs to add them.")
############################
    def updateActions(self):
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.addNodeAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.addLineAct.setEnabled(not self.fitToWindowAct.isChecked())
    def normalSize(self):
        #self.imageLabel.adjustSize()
        self.gwidget.adjustSize()
        self.scaleFactor = 1.0
    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
        if fileName:
            self.image = QtGui.QImage(fileName)
            if self.image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            self.gwidget.drawMyBackground(self.image)
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.gwidget.adjustSize()
    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))
    def addNode(self):
        i, ok = QtGui.QInputDialog.getInteger(self,
                "AddNode", "the number you wanna add to map:", 25, 0, 100, 1)
        if ok:
            self.gwidget.drawMyNode(i,self.image)
    def addLine(self):
        self.linebox=LineMagicBox(self)
        self.linebox.show()
########################################
    def createActions(self):
    	self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)
        
        self.printAct = QtGui.QAction(QtGui.QIcon(':/images/print.png'),
                "&Print...", self, shortcut=QtGui.QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.print_)

        self.quitAct = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)
        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)
                
        self.normalSizeAct = QtGui.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.addNodeAct = QtGui.QAction("&AddNode", self, shortcut="Ctrl+N",
        	enabled=False,triggered=self.addNode)
        self.addLineAct = QtGui.QAction("&AddLine", self, shortcut="Ctrl+L",
        	enabled=False,triggered=self.addLine)
	self.showDocAct =QtGui.QAction("&Docs", self, shortcut="Ctrl+D",
        	enabled=True,triggered=self.showDoc)
    def showDoc(self):
    	self.docview=QtWebKit.QWebView()
    	self.docview.load(QtCore.QUrl.fromLocalFile ("/opt/tinyos-2.1.1/doc/nesdoc/telosb/index.html"))
    	self.docview.show()
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)      
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)
	
	self.setMenu = self.menuBar().addMenu("&Set")
	self.setMenu.addAction(self.addNodeAct)
	self.setMenu.addAction(self.addLineAct)
        self.menuBar().addSeparator()
        
        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addAction(self.showDocAct)
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        
    def operationBox(self):
    	#print item.data(0,0)
    	self.selectList=self.ramTreeWidget.selectedItems()
    	vNameStr=self.selectList[0].data(0,0).toString()
    	self.rpcMBox=RPCMagicBox(vNameStr,self.app,self)
    	self.rpcMBox.show()
    def exeCommand(self):
    	self.exeList=self.rpcList.selectedItems()
    	fNameStr=self.exeList[0].data(0).toString()
    	self.rsMBox=RSMagicBox(fNameStr,self.app,self)
    	self.rsMBox.show()
    	#print fNameStr	
    def createDockWindows(self):
    	rpcstr=[]
    	str1=self.app.rpc
	str2=str(str1)
	str3=str2.split("\n")
	for x in range(len(str3)):
		if not str3[x]=='':
			tmp=str3[x].strip()
			rpcstr.append(tmp)
        dock = QtGui.QDockWidget("Rpc", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.rpcList = QtGui.QListWidget(dock)
        for i in range(len(rpcstr)):
            qlwitem=QtGui.QListWidgetItem(rpcstr[i])
            qlwitem.setToolTip("double click to execute")
            self.rpcList.addItem(qlwitem)

        dock.setWidget(self.rpcList)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        self.rpcList.itemDoubleClicked.connect(self.exeCommand)
##############################################
        dock = QtGui.QDockWidget("RamSymbols", self)
        headerLabels = ("vName", "vType")
        self.ramTreeWidget = QtGui.QTreeWidget()
        self.ramTreeWidget.setHeaderLabels(headerLabels)
        self.ramTreeWidget.setColumnCount(2)        
        ramstr=[]
    	ramtype=[]
    	ramname=[]
    	str11=self.app.ramSymbols
	str22=str(str11)
	str33=str22.split("\n")
	for x in range(len(str33)):
		if not str33[x]=='':
			tmp=str33[x].strip()
			ramstr.append(tmp)
	for x in range(len(ramstr)):
		ramtype.append(ramstr[x].split(":")[0])
		ramname.append(ramstr[x].split(":")[1])
    		item = QtGui.QTreeWidgetItem(self.ramTreeWidget)
        	item.setText(0, ramname[x])
        	item.setText(1, ramtype[x])
        self.ramTreeWidget.itemDoubleClicked.connect(self.operationBox)
        dock.setWidget(self.ramTreeWidget)
        
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
#####################################################################
class LineMagicBox(QtGui.QDialog):
    def __init__(self,parent=None):
        super(LineMagicBox,self).__init__(parent)
        self.setWindowTitle("ShowLine")
        self.parent=parent
        self.sourceLabel = QtGui.QLabel("Source Node:")
        self.destinationLabel =QtGui.QLabel("Destination Node:")
        
        self.sourceComboBox = QtGui.QComboBox()
        self.destinationGroupBox = QtGui.QGroupBox()
        
        layout1 = QtGui.QVBoxLayout()
        self.checkbox=[]
        for x in range(len(self.parent.gwidget.myNodeList)):
            self.sourceComboBox.addItem("Node"+str(x))
            self.checkbox.append(QtGui.QCheckBox("Node"+str(x)))
            layout1.addWidget(self.checkbox[x])
        for x in range(len(self.parent.gwidget.myNodeList)):
            self.checkbox[x].setChecked(False)
        i=self.sourceComboBox.currentIndex()
        destNodeList=[]
        for x in range(len(self.parent.gwidget.myNodeList[i].edgeList)):
            destnode=self.parent.gwidget.myNodeList[i].edgeList[x].destNode()
            index=destnode.Index()
            self.checkbox[index].setChecked(True)                
        self.destinationGroupBox.setLayout(layout1)
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        self.scrollArea.setWidget(self.destinationGroupBox)
        
        self.sourceComboBox.currentIndexChanged.connect(self.refresh)
        
        addButton =QtGui.QPushButton("&Add")
        addButton.clicked.connect(self.showLineOnMap)
        closeButton = QtGui.QPushButton("&Close")
        closeButton.clicked.connect(self.close)

        bottomLayout = QtGui.QHBoxLayout()
        bottomLayout.addStretch()
        bottomLayout.addWidget(closeButton)
        bottomLayout.addWidget(addButton)
        layout2 = QtGui.QVBoxLayout()
    	layout2.addWidget(self.sourceLabel)
    	layout2.addWidget(self.sourceComboBox)
    	layout2.addWidget(self.destinationLabel)
    	layout2.addWidget(self.scrollArea)
    	layout2.addLayout(bottomLayout)

    	self.setLayout(layout2)
    def refresh(self):
        for x in range(len(self.parent.gwidget.myNodeList)):
            self.checkbox[x].setChecked(False)
        i=self.sourceComboBox.currentIndex()
        for x in range(len(self.parent.gwidget.myNodeList[i].edgeList)):
            destnode=self.parent.gwidget.myNodeList[i].edgeList[x].destNode()
            index=destnode.Index()
            self.checkbox[index].setChecked(True)
    def showLineOnMap(self):
    	for x in range(len(self.checkbox)):
    	    if self.checkbox[x].isChecked():
    	    	i=self.sourceComboBox.currentIndex()
    	        self.parent.gwidget.scene.addItem(Edge(self.parent.gwidget.myNodeList[i], self.parent.gwidget.myNodeList[x])) 
    	#print "waiting remove"
    	#self.parent.gwidget.scene.removeItem(self.parent.gwidget.myNodeList[0].edgeList[0])
class RSMagicBox(QtGui.QDialog):
    def __init__(self, fName,app,parent=None): 
    	super(RSMagicBox, self).__init__(parent)
    	self.setWindowTitle("ExecuteCommand")
    	self.funNamestr=fName
    	self.parent=parent
    	self.argstr=self.funNamestr.split("(")[-1]
    	self.argstr_=str(self.argstr.split(")")[0].strip())
    	self.typestr=str(self.funNamestr.split(" ")[0].strip())
    	self.namestr=self.funNamestr.split("(")[0]
    	self.namestr_=str(self.namestr.split(" ")[-1].strip())
    	self.app=app
    	self.rtntypeLabel = QtGui.QLabel("Return Type:")
    	self.funnameLabel = QtGui.QLabel("Function Name:")
    	self.argsLabel = QtGui.QLabel("Please input the argumens value if it has:\nlike this("+self.argstr_+")")
    	self.rtntypeEdit = QtGui.QLineEdit()
    	self.rtntypeEdit.setReadOnly(True)
    	self.funnameEdit = QtGui.QLineEdit()
    	self.funnameEdit.setReadOnly(True)
    	self.argsEdit = QtGui.QLineEdit()
    	
    	self.rtntypeEdit.setText(self.typestr)
    	self.funnameEdit.setText(self.namestr_)
    	self.argsEdit.setText("")
    	#self.buttonBox = QtGui.QDialogButtonBox()
    	
    	self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Close)
    	self.buttonBox.addButton("&Execute",QtGui.QDialogButtonBox.AcceptRole)
    	
    	self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)
        
    	layout = QtGui.QVBoxLayout()
    	layout.addWidget(self.funnameLabel)
    	layout.addWidget(self.funnameEdit)
    	layout.addWidget(self.rtntypeLabel)
    	layout.addWidget(self.rtntypeEdit)
    	layout.addWidget(self.argsLabel)
    	layout.addWidget(self.argsEdit)
    	layout.addWidget(self.buttonBox)
    	self.setLayout(layout)
    def accept(self):
    	argsstr=str(self.argsEdit.text())
    	exestr="self.app."+self.namestr_+"("+argsstr+")"
    	exec exestr
    	self.parent.setCurrentNodeID()
    	if not self.parent.flag==0:
    	    self.parent.gwidget.myNodeList[0].updateToolTip(self.app)
    	qmessbox=QtGui.QMessageBox(self)
    	qmessbox.setText("the command has executed!")
    	qmessbox.show()
class RPCMagicBox(QtGui.QDialog):  
    def __init__(self, vName,app,parent=None): 
    	super(RPCMagicBox, self).__init__(parent)
    	self.setWindowTitle("OperationBox")
    	self.valName=vName
    	self.parent=parent
    	self.app=app
    	self.nameLabel = QtGui.QLabel("Variable Name:")
    	self.nameEdit = QtGui.QLineEdit(self.valName)
    	self.valueLabel = QtGui.QLabel("Variable Value:")
    	self.valueEdit = QtGui.QLineEdit()
    	self.displayCheckBox = QtGui.QCheckBox("To display the value on the map")
    	self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)
    	self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)
              
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameEdit)
        layout.addWidget(self.valueLabel)
        layout.addWidget(self.valueEdit)
        layout.addWidget(self.displayCheckBox)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        vNameStr2="soso=self.app."+self.valName.strip()+".peek()"
    	exec vNameStr2
	result_=str(soso)
	result__=result_.split(":")[-1]
	result___=result__.split("\n")[0]
	result____=result___.strip()
	result=int(result____)
    	self.valueEdit.setText(str(result))
    def accept(self):
    	if self.valueEdit.isModified():
    	     tmpval=self.valueEdit.text().strip()   	     
    	     vNameStr3="self.app."+self.valName.strip()+".poke("+tmpval+")"
    	     exec vNameStr3
    	     self.parent.setCurrentNodeID()
    	     if not self.parent.flag==0:
    	         self.parent.gwidget.myNodeList[0].updateToolTip(self.app)
    	     #print "nihao"
    	     vNameStr2="soso=self.app."+self.valName.strip()+".peek()"
    	     exec vNameStr2
    	     #print vNameStr2
	     result_=str(soso)
	     result__=result_.split(":")[-1]
	     result___=result__.split("\n")[0]
	     result____=result___.strip()
	     result=int(result____)
	     self.valueEdit.setText(str(result))
	else:
	     pass
	if self.displayCheckBox.isChecked():
	    if self.parent.flag==0:
    	    	qmessbox=QtGui.QMessageBox(self)
    		qmessbox.setText("you have not open the map or\n add the node on the map")
    		qmessbox.show()
    	    elif self.parent.gwidget.myNodeList[0].tooltip.find(self.valName.strip())==-1:
    	        #print "set"
    	    	val=self.valueEdit.text()
    	    	node=self.parent.gwidget.myNodeList[0]
    	    	node.tooltip=node.tooltip+self.valName+"="+val+"\n"
    	    	node.setToolTip(node.tooltip)
    	    else:
    	    	#print "update"
    	    	self.parent.gwidget.myNodeList[0].updateToolTip(self.app)
    	    	
    	    	
    	    	
    	    	
    	
###########################################################
class Edge(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()

        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()

        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()
    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()

    def adjust(self):
        
        if not self.source or not self.dest:
            return

        line = QtCore.QLineF(self.mapFromItem(self.source, 0, 0),
                self.mapFromItem(self.dest, 0, 0))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length,
                (line.dy() * 10) / length)

        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def boundingRect(self):
        if not self.source or not self.dest:
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)
	if line.length() == 0.0:
            return
	
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(QtCore.Qt.black)

        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))


class Node(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType + 1
    def __init__(self, graphWidget,nodeindex,nodecolor=0):
        super(Node, self).__init__()
        self.index=nodeindex
	self.thread=Worker()
	QtCore.QObject.connect(self.thread, QtCore.SIGNAL("start()"), self.linesAdjust)
	self.NodeID=0
	self.tooltip=''
        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QtCore.QPointF()
	self.nodeColor=nodecolor
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)
    def linesAdjust(self):
        for edge in self.edgeList:
            edge.adjust()
    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()
    def Index(self):
        return self.index
    def updateToolTip(self,app):
    	tmptooltip=self.tooltip.strip()
    	if not tmptooltip=='':
    	    vnames=tmptooltip.split("\n")
    	    self.tooltip=''
    	    #print len(vnames)
    	    for i in range(len(vnames)):
    	    	vname=vnames[i].split("=")[0]
    	    	vNameStr="soso=app."+vname+".peek()"
    	     	exec vNameStr
    	     	val_=str(soso)
	     	val__=val_.split(":")[-1]
	     	val___=val__.split("\n")[0]
	     	val=val___.strip()
   		self.tooltip=self.tooltip+vname+"="+val+"\n"
   	    #print self.tooltip	
   	    self.setToolTip(self.tooltip)
   		 	
    def setNodeID(self,ID):
    	self.NodeID=ID
    def getNodeID(self):
    	return self.NodeID
    def type(self):
        return Node.Type

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10 - adjust, 23 + adjust,
                23 + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)
        gradient = QtGui.QRadialGradient(-3, -3, 10)
         
        if option.state & QtGui.QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            if not self.nodeColor:
            	gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
            	gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
            else:
            	gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.red).light(120))
            	gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkRed).light(120))
        else:
            if not self.nodeColor:
            	gradient.setColorAt(0, QtCore.Qt.yellow)
            	gradient.setColorAt(1, QtCore.Qt.darkYellow)
            else:
            	gradient.setColorAt(0, QtCore.Qt.red)
            	gradient.setColorAt(1, QtCore.Qt.darkRed)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)
        textRect = QtCore.QRectF(-7, -7, 20, 20)
        message = str(self.index)

        font = painter.font()
        font.setBold(True)
        font.setPointSize(7)
        painter.setFont(font)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(textRect, message)
    def itemChange(self, change, value):
  	
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            
	    #self.thread.render()
            #for edge in self.edgeList:
             #   edge.adjust()
            self.graph.itemMoved()

        return super(Node, self).itemChange(change, value)
    def calculateForces(self):
        if not self.scene() or self.scene().mouseGrabberItem() is self:
            self.newPos = self.pos()
            return
    
        # Sum up all forces pushing this item away.
        xvel = 0.0
        yvel = 0.0
        for item in self.scene().items():
            if not isinstance(item, Node):
                continue

            line = QtCore.QLineF(self.mapFromItem(item, 0, 0),
                    QtCore.QPointF(0, 0))
            dx = line.dx()
            dy = line.dy()
            l = 2.0 * (dx * dx + dy * dy)
            if l > 0:
                xvel += (dx * 150.0) / l
                yvel += (dy * 150.0) / l

        # Now subtract all forces pulling items together.
        weight = (len(self.edgeList) + 1) * 10.0
        for edge in self.edgeList:
            if edge.sourceNode() is self:
                pos = self.mapFromItem(edge.destNode(), 0, 0)
            else:
                pos = self.mapFromItem(edge.sourceNode(), 0, 0)
            xvel += pos.x() / weight
            yvel += pos.y() / weight
    
        if QtCore.qAbs(xvel) < 0.1 and QtCore.qAbs(yvel) < 0.1:
            xvel = yvel = 0.0

        sceneRect = self.scene().sceneRect()
        self.newPos = self.pos() + QtCore.QPointF(xvel, yvel)
        self.newPos.setX(min(max(self.newPos.x(), sceneRect.left() + 10), sceneRect.right() - 10))
        self.newPos.setY(min(max(self.newPos.y(), sceneRect.top() + 10), sceneRect.bottom() - 10))

    def mousePressEvent(self, event):
    	self.update()
    	self.thread.render()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        self.thread.render()
        super(Node, self).mouseReleaseEvent(event)
class Worker(QtCore.QThread):
    def __init__(self, parent = None):
	QtCore.QThread.__init__(self, parent)
	self.exiting = False
    def __del__(self):
	self.exiting = True
	self.wait()
    def render(self):
	self.start()
    def run(self):
	self.emit(QtCore.SIGNAL("start()"))
		#time.sleep(2)
		#self.emit(QtCore.SIGNAL("log(QString)"),u'text')
		#time.sleep(2)
		#self.emit(QtCore.SIGNAL("terminated()"))

class GraphWidget(QtGui.QGraphicsView):
    def __init__(self,parent=None):
        super(GraphWidget, self).__init__()
        self.setMouseTracking(True)
        self.itemInMotion = None
        self.myNodeList=[]
        self.parent=parent
        
    def drawMyBackground(self,image):    	
        self.timerId = 0
        self.setBackgroundBrush(QtGui.QBrush(image))
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene.setSceneRect(0, 0, image.width(), image.height())
        self.setScene(self.scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.scale(2, 2)
        
    def drawMyNode(self,num,image):
    	
    	nodeNum=len(self.myNodeList)+num
    	curNodeID=self.parent.currentNodeID
    	#print curNodeID
    	for i in range(nodeNum-num,nodeNum):
    	    self.parent.flag=self.parent.flag+1
    	    #if curNodeID==i:
    	    if i==0:
    	    	nodecolor=1
    	    	self.myNodeList.append(Node(self,i,nodecolor))
    	    	self.myNodeList[i].setNodeID(curNodeID)
    	    	self.scene.addItem(self.myNodeList[i])
    	    else:
    	    	nodecolor=0	
            	self.myNodeList.append(Node(self,i,nodecolor))
    	    	self.scene.addItem(self.myNodeList[i])

    	    x=random.randint(0,image.width())	
    	    y=random.randint(0,image.height())
    	    self.myNodeList[i].setPos(x,y) 
    	    #self.myNodeList[i].setToolTip('NodeID='+str(i)+'\nhello weixin')
 	   	    
    def itemMoved(self):
        #print "moving"
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def timerEvent(self, event):
        nodes = [item for item in self.scene().items() if isinstance(item, Node)]

        for node in nodes:
            node.calculateForces()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 1.01 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)


if __name__ == '__main__':

    import sys

    qapp = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(qapp.exec_())
    #sys.exit()
