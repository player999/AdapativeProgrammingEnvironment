import sys
from linker import list_reductions, list_functions, get_function_parameter, find_reduction
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

program = "main"


def funcname_all():
    return list_functions()


def get_function_parameter_all(fname, param):
    return get_function_parameter(fname, param)


class LabeledLinedit(QHBoxLayout):
    def __init__(self, label, parent=None):
        super(QHBoxLayout, self).__init__(parent)
        self.label = QLabel(label)
        self.addWidget(self.label)
        self.ledit = QLineEdit()
        self.addWidget(self.ledit)

    def get_value(self):
        return self.ledit.text()

    def __del__(self):
        self.removeItem(self.itemAt(0))
        self.removeItem(self.itemAt(0))
        self.ledit.hide()
        self.label.hide()
        del self.ledit
        del self.label


class FunctionReader(QVBoxLayout):
    def __init__(self, name, parent=None):
        super(QVBoxLayout, self).__init__(parent)
        self.name = name

        self.addWidget(QLabel(name))

        self.selector = QComboBox()
        funcs = ["", "Custom"]
        funcs.extend(funcname_all())
        self.selector.addItems(funcs)
        self.selector.currentIndexChanged.connect(self.selected_function)
        self.addWidget(self.selector)

        self.farguments = QVBoxLayout()
        self.addLayout(self.farguments)

    def selected_function(self):
        #Clear Layout
        item_count = self.farguments.count()
        for i in range(0, item_count):
            item = self.farguments.itemAt(0)
            lt = item.layout()
            self.farguments.removeItem(item)
            del lt

        #Add arguments
        if self.selector.currentText() == "":
            return

        if self.selector.currentText() == "Custom":
            self.farguments.addLayout(LabeledLinedit("Function name"))
        else:
            ars = get_function_parameter_all(self.selector.currentText(), "args")
            for ar in ars:
                self.farguments.addLayout(LabeledLinedit(ar))

    def get_funcname(self):
        if self.selector.currentText() == "":
            return None

        if self.selector.currentText() == "Custom":
            return self.farguments.itemAt(0).layout().get_value()

        if self.farguments.count() == 0:
            return self.selector.currentText()
        else:
            count = self.farguments.count()
            ars = []
            for i in range(0, count):
                lay = self.farguments.itemAt(i).layout()
                val = int(lay.get_value())
                ars.append(val)
            pat = get_function_parameter_all(self.selector.currentText(), "genpattern")
            funcname = pat % tuple(ars)
            return funcname

    def __del__(self):
        item = self.itemAt(0)
        widget = item.widget()
        self.removeItem(item)
        widget.hide()
        del widget

        item = self.itemAt(0)
        widget = item.widget()
        self.removeItem(item)
        widget.hide()
        del widget

        item = self.itemAt(0)
        lay = item.layout()
        self.removeItem(item)
        del lay


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedWidth(200)
        self.setMaximumHeight(5)
        layout = QVBoxLayout()
        self.submitButton = QPushButton("Reduce!")
        layout.addWidget(self.submitButton)
        self.setLayout(layout)
        self.setWindowTitle("Adaptive")


class ReduceWindow(QWidget):
    def __init__(self, resolvname, parent=None):
        super(ReduceWindow, self).__init__(parent)
        self.setFixedWidth(400)
        self.setMaximumHeight(5)

        self.setWindowTitle("Reduce function \"%s\"" % resolvname)

        layout = QVBoxLayout()

        label_func = QLabel("Reducing function \"%s\"" % resolvname)
        layout.addWidget(label_func)

        reds = list_reductions()
        redbut_layout = QHBoxLayout()
        for red in reds:
            but = QPushButton(red)
            but.clicked.connect(partial(self.selected_reduction, red))
            redbut_layout.addWidget(but)
        layout.addLayout(redbut_layout)

        self.functions = QVBoxLayout()

        layout.addLayout(self.functions)

        self.submitButton = QPushButton("Submit")
        layout.addWidget(self.submitButton)
        self.setLayout(layout)

    @pyqtSlot(str)
    def selected_reduction(self, name):
        #Clear Layout
        lo = self.functions
        co = lo.count()
        for i in range(0, co):
            item = lo.itemAt(0)
            wid = item.widget()
            lay = item.layout()
            lo.removeItem(item)
            if wid != None:
                wid.hide()
                del wid
            if lay != None:
                del lay

        #Resize window
        self.setMaximumHeight(5)
        self.update()

        red = find_reduction(name)
        ars = red.getFields()
        for ar in ars:
            if ar["count"] == 1:
                self.functions.addLayout(FunctionReader(ar["name"]))

            if ar["count"] > 1:
                for i in range(0, ar["count"]):
                    self.functions.addLayout(FunctionReader(ar["name"] + " " + str(i)))

            if ar["count"] == -1:
                self.functions.addLayout(FunctionReader(ar["name"] + " 0"))
                but = QPushButton("Add More")
                but.clicked.connect(partial(self.add_field, but, ar["name"], 1))
                self.functions.addWidget(but)

    @pyqtSlot(QPushButton, str, int)
    def add_field(self, but, name, idx):
        but.disconnect()
        but.clicked.connect(partial(self.add_field, but, name, idx + 1))
        num = self.functions.indexOf(but)
        lay = FunctionReader(name + " " + str(num))
        self.functions.insertLayout(num, lay)


def start_windowed(argv):
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    reduce_window = ReduceWindow("main")
    reduce_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_windowed(sys.argv)
