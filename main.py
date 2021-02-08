from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QMessageBox
import sys
from ControllerProgram import Ui_Main
from pycode import Macro
from threading import Thread


class App(QtWidgets.QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.ui.btn_AddMouseEvent.clicked.connect(self.add_mouse_event)
        self.ui.btn_save.clicked.connect(self.save_macro)
        self.ui.btn_delete.clicked.connect(self.clear_macro)
        self.ui.btn_preview_macro.clicked.connect(self.preview_macro)
        self.ui.slider_power.valueChanged.connect(self.power_changed)
        self.ui.listWidget_your_macros.itemSelectionChanged.connect(self.item_activated)
        self.macro = Macro()
        self.temp_pattern = []
        self.t1 = Thread(target=lambda: self.macro.mainloop())
        self.startup()

    def add_mouse_event(self):
        temp = self.ui.spinBox_x.text() + ',' + self.ui.spinBox_y.text()
        temp_delay = self.ui.doubleSpinBox_delay_mouse.text()

        self.add_temp_pattern([self.ui.spinBox_x.value(),
                               self.ui.spinBox_y.value(),
                               self.ui.doubleSpinBox_delay_mouse.value()])

        self.ui.listWidget.addItem("➳ mouse event " + temp + "\n● delay " + temp_delay)

        self.ui.spinBox_x.setValue(0)
        self.ui.spinBox_y.setValue(0)
        self.ui.doubleSpinBox_delay_mouse.setValue(0)

    def set_temp_pattern(self, value):
        self.temp_pattern = value

    def add_temp_pattern(self, _pattern):
        self.temp_pattern.append(_pattern)

    def get_temp_pattern(self):
        return self.temp_pattern

    def preview_macro(self):
        self.macro.set_preview_macro(self.get_temp_pattern())

    def save_macro(self):
        text, ok = QInputDialog.getText(self, 'Save Macro - Bisquit', 'Give a name to your macro.')

        if ok and text:
            if self.get_temp_pattern() is not []:
                self.macro.create_macro_pattern(text, self.get_temp_pattern())
                self.ui.listWidget_your_macros.clear()
                self.list_macros()
                self.clear_macro()
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Error - Bisquit')
                msg.setText('There is no macro to be saved.')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ignore)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error - Bisquit')
            msg.setText('Please give a name to your macro.')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ignore)
            msg.exec_()

    def clear_macro(self):
        self.ui.listWidget.clear()
        self.set_temp_pattern([])

    def power_changed(self):
        self.macro.set_macro_power(self.ui.slider_power.value())

    def startup(self):
        self.t1.start()
        self.t1.join(1)
        self.list_macros()

    def list_macros(self):
        try:
            temp = self.macro.get_macro_patterns()
            for name in temp["macros"]:
                self.ui.listWidget_your_macros.addItem(name.get("name"))
        except:
            self.list_macros()

    def item_activated(self):
        self.macro.set_macro_index(self.ui.listWidget_your_macros.currentRow())

    def closeEvent(self, event):
        self.macro.set_program_working(False)
        del self.t1


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = App()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
