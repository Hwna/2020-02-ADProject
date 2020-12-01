#exchange
from forex_python.converter import CurrencyRates, CurrencyCodes


class calcExchange:
    def __init__(self):
        self.c = CurrencyRates()
        self.s = CurrencyCodes()

    def getRate(self, nation1, nation2):        #환율 추출
        self.rate = (self.c).get_rate(nation1, nation2)
        return self.rate

    def calculate(self, beforeCalc):        #입력받은 값 환전
        self.afterCalc = round((self.rate * beforeCalc),2)
        return self.afterCalc

    def getIcon(self, nation):      #화폐 기호 가져오기
        self.icon = (self.s).get_symbol(nation)
        return self.icon

if __name__ == '__main__':
    cal1 = calcExchange()
    s1 = 'USD'
    s2 = 'EUR'
    print(cal1.getRate(s1,s2))
    print(cal1.calculate(10.45))
    print(cal1.getIcon(s2))
