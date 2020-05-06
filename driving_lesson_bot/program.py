moneyTypes = [5000, 1000, 500, 100, 50]

def getMoney(amount):
    if (amount % min(moneyTypes)) == 0:
        d = {}
        for typeofmoney in moneyTypes:
            d.update({f'{typeofmoney}': '0'})

        for typeofmoney in moneyTypes:
            if amount // typeofmoney:
                while amount >= typeofmoney:
                    amount -= typeofmoney
                    edit = int(d[f'{typeofmoney}']) + 1
                    d.update({f'{typeofmoney}': edit})

        for keys, values in d.items():
            print(keys, " : ", values)
    elif amount < min(moneyTypes):
        print(f'Извините, но деньги вернуть невозможно! Cумма должна быть не менее чем {min(moneyTypes)}. Попробуйте ввести другую сумму.')
    else:
        print(f'Извините, но деньги вернуть невозможно! Cумма должна быть кратна {min(moneyTypes)}. Попробуйте ввести другую сумму.')





amount = input('Введите сумму: ')
try:
    getMoney(int(amount))
except:
    print('Ошибка! Вводить можно только целое число')
