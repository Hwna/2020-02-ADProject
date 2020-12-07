from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox

from exchange import calcExchange, addonExchange
from nationList import nationList, leadingContries


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_widget = Exchange(self)
        self.setCentralWidget(self.form_widget)
        self.resize(350, 500)  # 임시 크기 조정
        self.statusBar().showMessage('')


class Exchange(QWidget):
    def __init__(self, parent):
        super(Exchange, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("환율 계산기")

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.createStartBox(), 0, 0)
        mainLayout.addWidget(self.createEndBox(), 1, 0)
        mainLayout.addWidget(self.show_leading_contries(), 2, 0)
        self.setLayout(mainLayout)

    # 환전 시작 박스 생성
    def createStartBox(self):

        startBox = QGroupBox('Start')

        # 첫 번째 국가를 선택
        self.startNation = QComboBox()
        self.startNation.addItem('국가 선택')
        for nation in list(nationList.keys()):
            self.startNation.addItem(nation)

        self.inputLbl = QLabel("", self)
        self.inputLbl.setAlignment(Qt.AlignCenter)

        # 국가를 선택하면 아이콘을 표시
        self.startNation.activated[str].connect(
            self.startIcon)

        # 환전할 금액을 입력
        self.inputMoney = QLineEdit()
        self.inputMoney.setPlaceholderText('환전할 금액을 입력하세요.')
        self.inputMoney.setAlignment(Qt.AlignRight)

        startLayout = QGridLayout()
        startLayout.addWidget(self.startNation, 0, 0)
        #startLayout.addWidget(self.inputLbl, 1, 0)
        startLayout.addWidget(self.inputMoney, 1, 1)

        startBox.setLayout(startLayout)

        return startBox

    # 환전 도착 박스 생성
    def createEndBox(self):

        endBox = QGroupBox('End')

        # 두 번째 국가를 선택
        self.endNation = QComboBox()
        self.endNation.addItem('국가 선택')
        for nation in list(nationList.keys()):
            self.endNation.addItem(nation)

        # 국가를 선택하면 아이콘을 표시
        self.endNation.activated[str].connect(
            self.endIcon)

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

    # 시작 국가의 화폐 기호를 가져옴
    def startIcon(self, nation):
        nation = nationList[nation]
        addon = addonExchange(nation)
        self.icon = addon.getIcon()
        # self.inputMoney.setText(self.icon)

    # 도착 국가의 화폐 기호를 가져옴
    def endIcon(self, nation):
        nation = nationList[nation]
        addon = addonExchange(nation)
        self.icon = addon.getIcon()
        self.displayMoney.clear()
        self.displayMoney.setText(self.icon)

    # 사용자 입력 정보를 가져옴.
    def getUserInput(self):
        n1 = self.startNation.currentText()
        n1 = nationList[n1]
        n2 = self.endNation.currentText()
        n2 = nationList[n2]
        money = float(self.inputMoney.text())
        print([n1, n2, money])
        return [n1, n2, money]

    # 환전 시작
    def startCalculate(self):
        user_input = self.getUserInput()
        self.Calculator = calcExchange(user_input[0], user_input[1])
        result = self.Calculator.calculate(user_input[2])
        self.displayMoney.setText(self.displayMoney.text() + " " + str(result))
        rate = self.Calculator.getRate()
        self.parent.statusBar().showMessage("환율: " + str(rate))

    # 주요 국가의 환율 변동 추이
    def show_leading_contries(self):
        rateBox = QGroupBox("주요 국가 환율 변동 추이")
        rateChart = QGridLayout()
        for idx, lc in enumerate(leadingContries):
            print(lc)
            print(idx)
            lc_lbl = QLabel(lc + "\t" + addonExchange(lc).getChange())
            lc_lbl.setAlignment(Qt.AlignLeft)
            rateChart.addWidget(lc_lbl, idx, 0)
        rateBox.setLayout(rateChart)
        return rateBox


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = MainWindow()
    calculator.show()
    sys.exit(app.exec_())
