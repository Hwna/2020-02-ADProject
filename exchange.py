# exchange
from forex_python.converter import CurrencyRates, CurrencyCodes
from datetime import datetime, timedelta


class calcExchange:
    def __init__(self, nation1, nation2):
        self.c = CurrencyRates()
        self.nation1 = nation1
        self.nation2 = nation2

    def getRate(self):  # 환율 추출
        self.rate = (self.c).get_rate(self.nation1, self.nation2)
        return self.rate

    def calculate(self, beforeCalc):  # 입력받은 값 환전
        self.beforeCalc = beforeCalc
        self.afterCalc = (self.c).convert(
            self.nation1, self.nation2, beforeCalc)
        return round(self.afterCalc, 2)


class addonExchange:
    def __init__(self, nation):
        self.c = CurrencyRates()
        self.s = CurrencyCodes()
        self.nation = nation

    def getIcon(self):  # 화폐 기호 가져오기
        self.icon = (self.s).get_symbol(self.nation)
        return self.icon

    def getChange(self):  # 전일 대비 변화율 구하기, The rates are updated daily 3PM CET.
        self.yesterday = datetime.today() - timedelta(2)
        self.todayTsr = (self.c).convert(self.nation, 'KRW', 1)
        self.yesterdayTsr = (self.c).convert(
            self.nation, 'KRW', 1, self.yesterday)
        self.tsrChange = self.todayTsr - self.yesterdayTsr
        self.changeRate = 100 - (self.yesterdayTsr)/(self.todayTsr) * 100
        self.tsrChange = round((self.tsrChange), 2)
        self.changeRate = round((self.changeRate), 2)
        if(self.tsrChange > 0):
            self.code = '▲'
        elif(self.tsrChange < 0):
            self.code = '▼'
        else:
            self.code = '-'
        self.changeChart = [self.nation, str(round(self.todayTsr, 2)), (
            self.code + " " + str(self.tsrChange)), (str(self.changeRate) + "%")]
        return self.changeChart

    def getChangeList(self):
        self.graphList = []
        for i in range(1, 4):
            self.day = datetime.today() - timedelta(i)
            self.tradingStandardRate = round(
                (self.c).convert(self.nation, 'KRW', 1, self.day), 2)
            self.graphList.append(self.tradingStandardRate)
        return self.graphList


if __name__ == '__main__':
    s1 = 'USD'
    s2 = 'KRW'
    cal1 = calcExchange(s1, s2)
    cal2 = addonExchange('USD')
    print(cal1.getRate())
    print(cal1.calculate(1))
    print(cal2.getChange())
    print(cal2.getChangeList())
