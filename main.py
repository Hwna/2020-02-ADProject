from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox


class MainWindow(QMainWindow):
    def __init__(self):
        pass


class Exchage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("환율 계산기")

        mainLayout = QGridLayout()

        ########## 첫 번째 박스 ##########

        self.startBox = QGroupBox('Start')

        # 첫 번째 국가를 선택
        self.firstNation = QComboBox()

        # 환전할 금액을 입력
        self.inputMoney = QLineEdit()
        self.inputMoney.setPlaceholderText('환전할 금액을 입력하세요')

        startLayout = QGridLayout()
        startLayout.addWidget(self.firstNation, 0, 0)
        startLayout.addWidget(self.inputMoney, 1, 1)

        self.startBox.setLayout(startLayout)

        ###############################

        ########## 두 번째 박스 ##########

        self.endBox = QGroupBox('End')

        # 두 번째 국가를 선택
        self.secondNation = QComboBox()

        # 환전한 금액을 표시
        self.displayMoney = QLineEdit()
        self.displayMoney.setReadOnly(True)
        self.displayMoney.setAlignment(Qt.AlignRight)

        endLayout = QGridLayout()
        endLayout.addWidget(self.secondNation, 0, 0)
        endLayout.addWidget(self.displayMoney, 1, 1)

        self.endBox.setLayout(endLayout)

        ###############################

        mainLayout.addWidget(self.startBox, 0, 0)
        mainLayout.addWidget(self.endBox, 1, 0)
        self.setLayout(mainLayout)

        self.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = Exchage()
    calculator.show()
    sys.exit(app.exec_())
