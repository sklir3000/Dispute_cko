#importing library to read csv files
from csv import DictReader

#creating variables and giving them file path in directory.
# since we have two reports - we have two variables
cko = '/Users/valerijus.kracius/Downloads/24-11-11-24-11-18-disputes.csv'
cko_nas = '/Users/valerijus.kracius/Downloads/24-11-11-24-11-18-disputes.csv'

#creating first list where will keep all needed NAMES(indicators) from report
indicator_old = []

#opening first file and adding needed items ('Dispute Indicator') to the list
with open(cko, 'r') as disputas:
    dispute = DictReader(disputas, delimiter=",")
    for chargeback in dispute:
        indicator_old.append(chargeback['Dispute Indicator'])


#As we need to count them - creating function to do that
def kiek_old():
    kiekis = {}
    for x in indicator_old:
        if x not in kiekis:
            kiekis[x] = 1
        else:
            kiekis[x] +=1
    return kiekis

###########################################################

#new report, new list
indicator_nas = []

#another file, adding items to new list
with open(cko_nas, 'r') as disputas:
    dispute = DictReader(disputas, delimiter=",")
    for chargeback in dispute:
        indicator_nas.append(chargeback['Dispute Indicator'])


#counting them
def kiek_nas():
    kiekis = {}
    for x in indicator_nas:
        if x not in kiekis:
            kiekis[x] = 1
        else:
            kiekis[x] +=1
    return kiekis

#Printing, just to see them
print(f'CKO_old: {kiek_old()}')
print(f'CKO_nas: {kiek_nas()}')


#creating dictionary to have them in one place and count
bendrai = {}

#adding items from the first list
for pavadinimas, kiekis in kiek_old().items():
    if pavadinimas in bendrai:
        bendrai[pavadinimas] += kiekis
    else:
        bendrai[pavadinimas] = kiekis

#adding items from the second list
for pavadinimas, kiekis in kiek_nas().items():
    if pavadinimas in bendrai:
        bendrai[pavadinimas] += kiekis
    else:
        bendrai[pavadinimas] = kiekis


#could skip this step and just print(bendrai),
# but want to have info easy to copy and to paste in our file
# so printing keys and counted values
with open('/Users/valerijus.kracius/Downloads/statistika.txt','w') as file:
    for vienas, du in bendrai.items():
        file.write(f'Is viso: {vienas} {du}\n')
        print(f'Is viso: {vienas} {du}')


