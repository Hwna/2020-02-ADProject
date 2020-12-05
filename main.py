from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


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
        self.startNation = QComboBox()
        self.startNation.addItem('1')  # 임시 값
        self.startNation.addItem('2')
        self.startNation.addItem('3')

        # 환전할 금액을 입력
        self.inputMoney = QLineEdit()
        self.inputMoney.setPlaceholderText('환전할 금액을 입력하세요')

        startLayout = QGridLayout()
        startLayout.addWidget(self.startNation, 0, 0)
        startLayout.addWidget(self.inputMoney, 1, 1)

        self.startBox.setLayout(startLayout)

        ###############################

        ########## 두 번째 박스 ##########

        self.endBox = QGroupBox('End')

        # 두 번째 국가를 선택
        self.endNation = QComboBox()
        self.endNation.addItem('1')  # 임시 값
        self.endNation.addItem('2')
        self.endNation.addItem('3')

        # 선택한 국가를 전송
        self.endNation.activated[str].connect(self.showNation)

        # 환전한 금액을 표시
        self.displayMoney = QLineEdit()
        self.displayMoney.setReadOnly(True)
        self.displayMoney.setAlignment(Qt.AlignRight)

        endLayout = QGridLayout()
        endLayout.addWidget(self.endNation, 0, 0)
        endLayout.addWidget(self.displayMoney, 1, 1)

        self.endBox.setLayout(endLayout)

        ###############################

        mainLayout.addWidget(self.startBox, 0, 0)
        mainLayout.addWidget(self.endBox, 1, 0)
        self.setLayout(mainLayout)

    def showNation(self, nation):
        print(self.startNation.currentText())
        print(nation)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = Exchage()
    calculator.show()
    sys.exit(app.exec_())
