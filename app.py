from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QTimer
from interface.Ui_main import Ui_MainWindow
import sys

class MatrixCalculator(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Instances
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        validator = QDoubleValidator()

        self.matrix = tuple()

        self.alert_timer = QTimer()
        self.alert_timer.setInterval(1000)
        self.c = 0

        # Itinialization
        self.ui.x1.setValidator(validator)
        self.ui.x2.setValidator(validator)
        self.ui.x3.setValidator(validator)
        self.ui.y1.setValidator(validator)
        self.ui.y2.setValidator(validator)
        self.ui.y3.setValidator(validator)
        self.ui.z1.setValidator(validator)
        self.ui.z2.setValidator(validator)
        self.ui.z3.setValidator(validator)
        self.ui.i1.setValidator(validator)
        self.ui.i2.setValidator(validator)
        self.ui.i3.setValidator(validator)
        
        self.ui.alert.clear()

        # Buttons controls
        self.ui.btn_calculate.clicked.connect(self.captureData)

        # Other signals
        self.alert_timer.timeout.connect(self.stopAlert)
        
        self.ui.x1.textEdited.connect(self.processInput)
        self.ui.x2.textEdited.connect(self.processInput)
        self.ui.x3.textEdited.connect(self.processInput)
        self.ui.y1.textEdited.connect(self.processInput)
        self.ui.y2.textEdited.connect(self.processInput)
        self.ui.y3.textEdited.connect(self.processInput)
        self.ui.z1.textEdited.connect(self.processInput)
        self.ui.z2.textEdited.connect(self.processInput)
        self.ui.z3.textEdited.connect(self.processInput)
        self.ui.i1.textEdited.connect(self.processInput)
        self.ui.i2.textEdited.connect(self.processInput)
        self.ui.i3.textEdited.connect(self.processInput)

    def captureData(self):
        try:
            # Capturando datos de la matriz
            self.matrix = (
                [
                    float(self.ui.x1.text()),
                    float(self.ui.y1.text()),
                    float(self.ui.z1.text()),
                    float(self.ui.i1.text())
                ],
                [
                    float(self.ui.x2.text()),
                    float(self.ui.y2.text()),
                    float(self.ui.z2.text()),
                    float(self.ui.i2.text())
                ],
                [
                    float(self.ui.x3.text()),
                    float(self.ui.y3.text()),
                    float(self.ui.z3.text()),
                    float(self.ui.i3.text())
                ]
            )        
            # for row in matrix:
            #     print(row)
            self.calculateXYZ()

        except ValueError:
            self.showHideAlert('¡Ingrese todos los datos de la matriz!')

    def calculateXYZ(self):
        for i in range(0, len(self.matrix), 1):      # Fila intacta
            for x in range(0, len(self.matrix), 1):  # Filas mutadas
                if x != i:
                    c1 = self.matrix[x][i]
                    c2 = self.matrix[i][i]

                    self.matrix[x][0] = c1 * self.matrix[i][0] - c2 * self.matrix[x][0]
                    self.matrix[x][1] = c1 * self.matrix[i][1] - c2 * self.matrix[x][1]
                    self.matrix[x][2] = c1 * self.matrix[i][2] - c2 * self.matrix[x][2]
                    self.matrix[x][3] = c1 * self.matrix[i][3] - c2 * self.matrix[x][3]

        for j in range(0, len(self.matrix), 1):
            num = self.matrix[j][j]
            self.matrix[j][j] /= num
            last_num = self.matrix[j][3] / num
            
            self.matrix[j][3] = int(last_num) if last_num.is_integer() else round(last_num, 2)

        # for row in self.matrix:
        #     print(row)

        self.ui.x_result.setText(str(self.matrix[0][3]))
        self.ui.y_result.setText(str(self.matrix[1][3]))
        self.ui.z_result.setText(str(self.matrix[2][3]))

    # ========== Secondaries Functions ============

    def showHideAlert(self, alert:str):
        self.ui.alert.setText(f"{alert}")
        self.alert_timer.start()

    def stopAlert(self):
        if self.c < 2:
            self.c+= 1
        else:
            self.c = 0
            self.ui.alert.clear()
            self.alert_timer.stop()

    def processInput(self, value:str):
        if "." in value:
            point = value.find(".")
            if len(value) > point + 3:
                self.sender().setText(value[:point + 3])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = MatrixCalculator()
    mc.show()
    sys.exit(app.exec_())