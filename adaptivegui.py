import sys
from linker import list_reductions, list_functions, get_function_parameter, find_reduction, find_function
import linker
from functools import partial
import translatereduction
import srcparser
from bfimpl.bfunc import compile
from adaptivenv import CompError


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

definitions = {}


def funcname_all():
    local_functions = list(definitions.keys())
    local_functions.extend(list_functions())
    return local_functions


def get_function_parameter_all(fname, param):
    if fname in definitions.keys():
        return []
    return get_function_parameter(fname, param)


def next_function():
    function = check_function(definitions["main"])
    return function


def check_function(reduction):
    ars = reduction[1]
    for ar in ars:
        if isundefined(ar):
            if ar in definitions.keys():
                res = check_function(definitions[ar])
                if res is not None:
                    return res
            else:
                return ar
    return None


def isundefined(fname):
    if find_function(fname) is not None:
        return False

    return True


class LabeledLinedit(QHBoxLayout):
    def __init__(self, label, parent=None):
        super(QHBoxLayout, self).__init__(parent)
        self.label = QLabel(label)
        self.addWidget(self.label)
        self.ledit = QLineEdit()
        self.addWidget(self.ledit)

    def get_value(self):
        return self.ledit.text()

    def mydelete(self):
        label_item = self.itemAt(0)
        ledit_item = self.itemAt(1)
        label = label_item.widget()
        ledit = ledit_item.widget()
        ledit.hide()
        label.hide()
        self.removeItem(label_item)
        self.removeItem(ledit_item)
        label.deleteLater()
        ledit.deleteLater()
        self.deleteLater()


class FunctionArguments(QVBoxLayout):
    def __init__(self, reduction, parent=None):
        super(QVBoxLayout, self).__init__(parent)
        self.fieldlist = []
        red = find_reduction(reduction)
        ars = red.getFields()
        for ar in ars:
            if ar["count"] == 1:
                freader = FunctionReader(ar["name"])
                self.fieldlist.append(freader)
                self.addLayout(freader)

            if ar["count"] > 1:
                for i in range(0, ar["count"]):
                    freader = FunctionReader(ar["name"] + " " + str(i))
                    self.fieldlist.append(freader)
                    self.addLayout(freader)

            if ar["count"] == -1:
                freader = FunctionReader(ar["name"] + " 0")
                self.addLayout(freader)
                self.fieldlist.append(freader)
                but = QPushButton("Add More")
                but.clicked.connect(partial(self.add_field, but, ar["name"], 1))
                self.addWidget(but)

    @pyqtSlot(QPushButton, str, int)
    def add_field(self, but, name, idx):
        but.disconnect()
        but.clicked.connect(partial(self.add_field, but, name, idx + 1))
        num = self.indexOf(but)
        lay = FunctionReader(name + " " + str(num))
        self.fieldlist.append(lay)
        self.insertLayout(num, lay)

    def get_functions(self):
        funclist = list(map(lambda x: x.get_funcname(), self.fieldlist))
        return funclist

    def mydelete(self):
        co = self.count()
        for i in range(0, co):
            item = self.itemAt(0)
            lay = item.layout()
            wid = item.widget()
            if wid is not None:
                if hasattr(wid, "hide"):
                    wid.hide()
                wid.deleteLater()
            if lay is not None:
                lay.mydelete()
            self.removeItem(item)
        self.deleteLater()

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
            lt.mydelete()
            self.farguments.removeItem(item)

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

    def mydelete(self):
        #Clear faerguments
        while self.farguments.itemAt(0):
            item = self.farguments.itemAt(0)
            lay = item.layout()
            self.farguments.removeItem(item)
            lay.mydelete()

        while self.itemAt(0):
            item = self.itemAt(0)
            widget = item.widget()
            lay = item.layout()
            self.removeItem(item)
            if  lay != None:
                lay.deleteLater()
            if widget != None:
                widget.hide()
                widget.deleteLater()
            self.deleteLater()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedWidth(200)
        self.setMaximumHeight(5)
        layout = QVBoxLayout()

        self.reduce_button = QPushButton("Reduce!")
        self.reduce_button.clicked.connect(self.start_reduction)
        layout.addWidget(self.reduce_button)

        self.composition_button = QPushButton("Open Composition")
        self.composition_button.clicked.connect(self.open_code)
        layout.addWidget(self.composition_button)

        self.setLayout(layout)
        self.setWindowTitle("Adaptive")

    def start_reduction(self):
        reduce_window = ReduceWindow("main")
        reduce_window.show()

    def open_code(self):
        fname = QFileDialog.getOpenFileName(self, "Find Composition Source")[0]
        src = open(fname, "r").read()
        global srcv
        srcv = SourceView(src)
        srcv.show()


class ReduceWindow(QWidget):
    def __init__(self, resolvname, parent=None):
        super(ReduceWindow, self).__init__(parent)
        self.setFixedWidth(400)
        self.setMaximumHeight(5)
        self.resolvname = resolvname
        self.setWindowTitle("Reduce function \"%s\"" % resolvname)

        layout = QVBoxLayout()

        self.label_func = QLabel("Reducing function \"%s\"" % resolvname)
        layout.addWidget(self.label_func)

        reds = list_reductions()
        redbut_layout = QHBoxLayout()
        for red in reds:
            but = QPushButton(red)
            but.clicked.connect(partial(self.selected_reduction, red))
            redbut_layout.addWidget(but)
        layout.addLayout(redbut_layout)
        self.submitButton = QPushButton("Next")
        self.submitButton.clicked.connect(self.accept_reduction)
        layout.addWidget(self.submitButton)
        self.setLayout(layout)
        self.reduction = None

    def clear_functions(self):
        if self.findChild(FunctionArguments, name="fargs"):
            lay = self.layout()
            item = lay.itemAt(2) #Position of arguments
            lay.removeItem(item)
            item.layout().mydelete()

    @pyqtSlot(str)
    def selected_reduction(self, name):
        self.clear_functions()
        self.reduction = name
        self.fargs = FunctionArguments(name)
        self.fargs.setObjectName("fargs")
        self.layout().insertLayout(2, self.fargs)
        self.adjustSize()
        return

    def accept_reduction(self):
        global definitions
        reduction = {self.resolvname: [self.reduction, self.fargs.get_functions()]}
        definitions.update(reduction)
        fname = next_function()
        if fname == None:
            self.hide()
            self.deleteLater()
            src = translatereduction.reduction2ppa(definitions)
            global srcv
            srcv = SourceView(src)
            srcv.show()
            return

        self.resolvname = fname
        self.setWindowTitle("Reduce function \"%s\"" % fname)
        self.label_func.setText("Reducing function \"%s\"" % fname)
        self.clear_functions()
        self.adjustSize()


class CompiledView(QWidget):
    def __init__(self, source, parent=None):
        super(CompiledView, self).__init__(parent)
        self.setWindowTitle("Compiled view")
        self.lay = QVBoxLayout()
        self.code_area = QTextEdit()
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.code_area.setFont(font)
        self.code_area.setText(source)
        self.lay.addWidget(self.code_area)
        self.setLayout(self.lay)
        self.setMinimumWidth(600)


class SourceView(QWidget):
    def __init__(self, source, parent=None):
        super(SourceView, self).__init__(parent)
        self.setWindowTitle("Source view")
        self.lay = QVBoxLayout()
        self.source = source
        self.code_area = QTextEdit()
        self.compile = QPushButton("Compile")
        self.compile.clicked.connect(self.pressed_compile)
        self.code_area.setText(source)
        self.lay.addWidget(self.code_area)
        self.lay.addWidget(self.compile)
        self.setLayout(self.lay)

    def pressed_compile(self):
        global compiled_view
        try:
            srcparser.parse_source(self.code_area.toPlainText())
            resolved = linker.link_functions(srcparser.valueSymList, srcparser.funcSymList, srcparser.compSymList)
            code = compile(resolved)
            compiled_view = CompiledView(code)
            compiled_view.show()
            self.hide()
            self.deleteLater()
        except CompError as err:
            QMessageBox.critical(self, "Compilation to syntax error", str(err))



def start_windowed(argv):
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_windowed(sys.argv)
