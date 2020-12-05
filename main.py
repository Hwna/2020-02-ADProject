from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QLayout, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QPushButton, QGroupBox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_widget = Exchage(self)
        self.setCentralWidget(self.form_widget)
        self.statusBar().showMessage('환율: ')


class Exchage(QWidget):
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
        self.startNation.addItem('1')  # 임시 값
        self.startNation.addItem('2')
        self.startNation.addItem('3')

        # 환전할 금액을 입력
        self.inputMoney = QLineEdit()
        self.inputMoney.setPlaceholderText('환전할 금액을 입력하세요')

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
        self.endNation.addItem('1')  # 임시 값
        self.endNation.addItem('2')
        self.endNation.addItem('3')

        # 두 번째 국가를 전송하면 메소드를 실행
        self.endNation.activated[str].connect(self.getNation)

        # 환전한 금액을 표시
        self.displayMoney = QLineEdit()
        self.displayMoney.setReadOnly(True)
        self.displayMoney.setAlignment(Qt.AlignRight)

        endLayout = QGridLayout()
        endLayout.addWidget(self.endNation, 0, 0)
        endLayout.addWidget(self.displayMoney, 1, 1)

        endBox.setLayout(endLayout)

        return endBox

    # 사용자가 입력한 두 국가를 가져옴.

    def getNation(self, nation):
        n1 = self.startNation.currentText()
        n2 = nation
        print(n1, n2)
        return (n1, n2)

    # 사용자가 입력한 금액을 가져욤.
    def getInputMoney(self):
        print(self.inputMoney.text())
        return self.inputMoney.text()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = MainWindow()
    calculator.show()
    sys.exit(app.exec_())
