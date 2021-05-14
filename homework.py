import datetime as dt
from typing import Optional


class Calculator:
    today = dt.datetime.now().date()

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        spend_today = 0
        for record in self.records:
            if record.today == record.date:
                spend_today += int(record.amount)
        return spend_today

    def get_remained(self):
        spend = 0
        for spend_sum in self.records:
            if spend_sum.date == self.today:
                spend += spend_sum.amount
        remain = self.limit - spend
        return remain

    def get_week_stats(self):
        delta = self.today - dt.timedelta(days=7)
        spend_for_seven_days = 0
        for record in self.records:
            if (record.date > delta) and (record.date <= self.today):
                spend_for_seven_days += record.amount
        return spend_for_seven_days


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_remained()
        if (balance < self.limit) and (balance > 0):
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        else:
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
        account_balance = round(balance / rate, 2)
        if (account_balance < self.limit) and (account_balance > 0):
            return f'На сегодня осталось {account_balance} {title}'
        if account_balance == 0:
            return 'Денег нет, держись'
        if account_balance < 0:
            account_balance_for_minus = abs(account_balance)
            return (f'Денег нет, держись: твой долг - '
                    f'{account_balance_for_minus} {title}')


class Record:
    date_format = '%d.%m.%Y'
    today = dt.datetime.now().date()

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = self.today
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()
