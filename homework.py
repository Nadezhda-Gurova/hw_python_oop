import datetime as dt
from typing import Optional


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.datetime.now().date()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        spend_today = sum(record.amount for record in self.records
                          if record.date == self.today)
        return spend_today

    def get_remained(self):
        spend = sum(spend_sum.amount for spend_sum in self.records
                    if spend_sum.date == self.today)
        remain = self.limit - spend
        return remain

    def get_week_stats(self):
        delta = self.today - dt.timedelta(days=7)
        spend_for_seven_days = 0
        for record in self.records:
            if self.today >= record.date > delta:
                spend_for_seven_days += record.amount
        return spend_for_seven_days


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_remained()
        if self.limit > balance > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.45
    EURO_RATE = 89.82
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        currency_data = {'rub': (self.RUB_RATE, 'руб'),
                         'eur': (self.EURO_RATE, 'Euro'),
                         'usd': (self.USD_RATE, 'USD')}
        rate, title = currency_data[currency]
        balance = self.get_remained()
        if balance == 0:
            return 'Денег нет, держись'
        if currency != 'rub':
            account_balance = round(balance / rate, 2)
        else:
            account_balance = balance
        if self.limit > account_balance > 0:
            return f'На сегодня осталось {account_balance} {title}'
        if account_balance < 0:
            account_balance_for_minus = abs(account_balance)
            return (f'Денег нет, держись: твой долг - '
                    f'{account_balance_for_minus} {title}')


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        today = dt.datetime.now().date()
        if date is None:
            self.date = today
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()
