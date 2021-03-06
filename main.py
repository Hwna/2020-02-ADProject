from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox, QMessageBox

from exchange import calcExchange, addonExchange
from nationList import nationList, leadingContries


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_widget = Exchange(self)
        self.setCentralWidget(self.form_widget)
        self.resize(350, 500)
        self.statusBar().showMessage('')
        self.setWindowTitle("환율 계산기")


class Exchange(QWidget):
    def __init__(self, parent):
        super(Exchange, self).__init__(parent)
        self.parent = parent
        self.selected1 = False
        self.selected2 = False
        self.initUI()

    def initUI(self):

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

        # 국가를 선택하면 아이콘을 표시
        self.startNation.activated[str].connect(
            self.startIcon)

        # 국가가 선택되었는지를 판단
        self.startNation.activated[str].connect(
            self.checkSelect1)

        # 환전할 금액을 입력
        self.inputMoney = QLineEdit()
        self.inputMoney.setPlaceholderText('환전할 금액을 입력하세요.')
        self.inputMoney.setAlignment(Qt.AlignRight)

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
        for nation in list(nationList.keys()):
            self.endNation.addItem(nation)

        # 국가를 선택하면 아이콘을 표시
        self.endNation.activated[str].connect(
            self.endIcon)

        # 국가가 선택되었는지 판단
        self.endNation.activated[str].connect(
            self.checkSelect2)

        # 환전한 금액을 표시할 LineEdit
        self.displayMoney = QLineEdit()
        self.displayMoney.setReadOnly(True)
        self.displayMoney.setAlignment(Qt.AlignRight)

        # 환전 시작 버튼 생성
        self.startBtn = QPushButton()
        self.startBtn.setText('환전하기')
        self.startBtn.clicked.connect(self.getUserInput)
        self.startBtn.setEnabled(False)

        endLayout = QGridLayout()
        endLayout.addWidget(self.endNation, 0, 0)
        endLayout.addWidget(self.startBtn, 1, 0)
        endLayout.addWidget(self.displayMoney, 1, 1)

        endBox.setLayout(endLayout)

        return endBox

    # 시작 국가의 화폐 기호를 가져옴
    def startIcon(self, nation):
        try:
            nation = nationList[nation]
            addon = addonExchange(nation)
            self.startIcon = addon.getIcon()
            self.inputMoney.setText(self.startIcon + " ")
        except KeyError:
            self.inputMoney.clear()

    # 도착 국가의 화폐 기호를 가져옴
    def endIcon(self, nation):
        try:
            nation = nationList[nation]
            addon = addonExchange(nation)
            self.endIcon = addon.getIcon()
            self.displayMoney.setText(self.endIcon)
        except KeyError:
            self.displayMoney.clear()

    # 사용자 입력 정보를 가져옴.
    def getUserInput(self):
        n1 = self.startNation.currentText()
        n1 = nationList[n1]
        n2 = self.endNation.currentText()
        n2 = nationList[n2]
        try:
            money = self.inputMoney.text()
            money = float(money.split(self.startIcon)[-1])

        # 입력이 숫자가 아닌 상황에 대한 예외 처리
        except ValueError:
            self.alert = QMessageBox.critical(
                self, '경고!', '형식이 올바르지 않습니다.', QMessageBox.Ok)
            self.inputMoney.setText(self.startIcon + " ")
            return
        self.startCalculate([n1, n2, money])

    # 시작 국가가 선택되었는지 확인
    def checkSelect1(self):
        self.selected1 = True
        if(self.selected2 == True):
            self.startBtn.setEnabled(True)

    # 도착 국가가 선택되었는지 확인
    def checkSelect2(self):
        self.selected2 = True
        if(self.selected1 == True):
            self.startBtn.setEnabled(True)

    # 환전 시작
    def startCalculate(self, user_input):
        self.Calculator = calcExchange(user_input[0], user_input[1])
        result = self.Calculator.calculate(user_input[2])
        self.displayMoney.setText(self.endIcon + " " + str(result))
        rate = self.Calculator.getRate()
        self.parent.statusBar().showMessage("환율: " + str(rate))

    # 주요 국가의 환율 변동 추이 (표)
    def show_leading_contries(self):
        rateBox = QGroupBox("주요 국가 환율 변동 추이")
        rateChart = QGridLayout()

        lbl1 = QLabel("통화")
        lbl2 = QLabel("매매기준율")
        lbl3 = QLabel("전일대비")
        lbl4 = QLabel("등락률")

        rateChart.addWidget(lbl1, 0, 0)
        rateChart.addWidget(lbl2, 0, 1)
        rateChart.addWidget(lbl3, 0, 2)
        rateChart.addWidget(lbl4, 0, 3)

        for idx, lc in enumerate(leadingContries):
            for i, info in enumerate(addonExchange(lc).getChange()):
                lc_lbl = QLabel(info)
                if i == 2:
                    if '▲' in info:
                        lc_lbl.setStyleSheet("color: #FB6868;")
                    elif '▼' in info:
                        lc_lbl.setStyleSheet("color: #5CB5FF;")
                elif i == 3:
                    if '-' in info:
                        lc_lbl.setStyleSheet("color: #5CB5FF;")
                    else:
                        lc_lbl.setStyleSheet("color: #FB6868;")

                lc_lbl.setAlignment(Qt.AlignLeft)
                rateChart.addWidget(lc_lbl, idx + 1, i)

        rateBox.setLayout(rateChart)
        return rateBox


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = MainWindow()
    calculator.show()
    sys.exit(app.exec_())
