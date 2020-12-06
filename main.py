from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox

from exchange import calcExchange, addonExchange


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_widget = Exchange(self)
        self.setCentralWidget(self.form_widget)
        self.resize(300, 250)  # 임시 크기 조정


class Exchange(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("환율 계산기")

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.createStartBox(), 0, 0)
        mainLayout.addWidget(self.createEndBox(), 1, 0)
        self.setLayout(mainLayout)

    # 환전 시작 박스 생성
    def createStartBox(self):

        startBox = QGroupBox('Start')

        # 첫 번째 국가를 선택
        self.startNation = QComboBox()
        self.startNation.addItem('국가 선택')
        self.startNation.addItem('USD')  # 임시 값
        self.startNation.addItem('KRW')
        self.startNation.addItem('DNK')
        self.startNation.addItem('DEU')
        self.startNation.addItem('INR')

        # 환전할 금액을 입력
        self.inputMoney = QLineEdit()
        self.inputMoney.setPlaceholderText('환전할 금액을 입력하세요.')

        startLayout = QGridLayout()
        startLayout.addWidget(self.startNation, 0, 0)
        startLayout.addWidget(self.inputMoney, 1, 1)

        startBox.setLayout(startLayout)

        return startBox

    # 환전 도착 박스 생성
    def createEndBox(self):

        endBox = QGroupBox('End')

        # 두 번째 국가를 선택
        self.endNation = QComboBox()
        self.endNation.addItem('국가 선택')
        self.endNation.addItem('USD')  # 임시 값
        self.endNation.addItem('KRW')
        self.endNation.addItem('DNK')
        self.endNation.addItem('DEU')
        self.endNation.addItem('INR')

        # 환전한 금액을 표시할 LineEdit
        self.displayMoney = QLineEdit()
        self.displayMoney.setReadOnly(True)
        self.displayMoney.setAlignment(Qt.AlignRight)

        # 환전 시작 버튼 생성
        self.startBtn = QPushButton()
        self.startBtn.setText('환전하기')
        self.startBtn.clicked.connect(self.startCalculate)

        endLayout = QGridLayout()
        endLayout.addWidget(self.endNation, 0, 0)
        endLayout.addWidget(self.startBtn, 1, 0)
        endLayout.addWidget(self.displayMoney, 1, 1)

        endBox.setLayout(endLayout)

        return endBox

    # 사용자 입력 정보를 가져옴.
    def getUserInput(self):
        n1 = self.startNation.currentText()
        n2 = self.endNation.currentText()
        money = float(self.inputMoney.text())
        print([n1, n2, money])
        return [n1, n2, money]

    # 환전 시작
    def startCalculate(self):
        user_input = self.getUserInput()
        self.Calculator = calcExchange(user_input[0], user_input[1])
        self.displayMoney.clear()
        result = self.Calculator.calculate(user_input[2])
        self.displayMoney.setText(str(result))
        rate = self.Calculator.getRate()
        print(rate)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = MainWindow()
    calculator.show()
    sys.exit(app.exec_())
