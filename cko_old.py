from csv import reader
from csv import DictReader

indicator = []

with open('/Users/valerijus.kracius/PycharmProjects/pythonProject/venv/24-05-20-24-05-26-DisputeReport-TransferGoLtd (1).csv', 'r') as disputas:
    dispute = DictReader(disputas, delimiter=",")
    for chargeback in dispute:
        indicator.append(chargeback['Dispute Indicator'])

def kiek():
    kiekis = {}
    for x in indicator:
        if x not in kiekis:
            kiekis[x] = 1
        else:
            kiekis[x] +=1
    return kiekis

print(kiek())