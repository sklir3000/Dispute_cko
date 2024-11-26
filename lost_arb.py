from docxtpl import DocxTemplate
import pandas as pd
import csv
import chardet
from csv import DictReader

admin_file = "Sheet 1_data"
cko_file = "24-11-18-24-11-25-disputes"

doc = DocxTemplate('/Users/valerijus.kracius/Documents/new_arb.docx')

with open(f"/Users/valerijus.kracius/Downloads/{admin_file}.csv", "rb") as file:
    result = chardet.detect(file.read(10000))  # Read a portion of the file to detect encoding
    encoding = result['encoding']

df1 = pd.read_csv(f"/Users/valerijus.kracius/Downloads/{admin_file}.csv", encoding=encoding, delimiter="\t")
df2 = pd.read_csv(f"/Users/valerijus.kracius/Downloads/{cko_file}.csv")

print(type(df1))

merged_df = pd.merge(df1, df2, left_on='purchase_id', right_on='Reference')

merged_df.to_csv('/Users/valerijus.kracius/Downloads/new_report.csv', index=False)

data = pd.DataFrame(merged_df)

for index, row in data.iterrows():
    if 'RPDL' == row['Dispute Indicator']:

        booking_date = row['booking_date'][:10]
        sent_date = row['sent_date'][:10]

        outgoing = row['outgoing_bank_account_code']
        if outgoing == 'ua_globus_uah':
            token = row['payout_token']
        else:
            token = row["partner_token"]

        acc = row["outgoing_bank_account_code"]
        acc = acc.split('_')
        if 'checkout' in acc:
            outgoing_acc = acc[1:3]
            outgoing_acc = ' '.join(outgoing_acc).title()
        elif 'bo' in acc:
            outgoing_acc = "Birlesik Odeme"
        elif 'sepa' in acc:
            outgoing_acc = "LHV"
        elif 'No Value' in acc:
            outgoing_acc = "-"
        else:
            outgoing_acc = acc[1].title()

        first_amount = str(row['payment_amount']).replace(",", "")
        second_amount = str(row['receiver_gets']).replace(",", "")
        send_amount = "{:.2f}".format(float(first_amount))
        receive_amount = "{:.2f}".format(float(second_amount))

        dispute_id = str(row["reason_number"])
        keturi = dispute_id[0]
        if keturi == '4':
            dispute = dispute_id[:4]
        else:
            dispute = dispute_id

        from_currency = row['from_currency_code']
        to_currency = row['to_currency_code']
        if from_currency == to_currency and send_amount != receive_amount:
            to_currency_fee = " Delivery fees were applied and our customer agreed to them when creating a payment. "
        else:
            to_currency_fee = " "

        if from_currency == to_currency:
            converted = 'The'
        else:
            converted = "The converted"

        if dispute_id == '13.1' or dispute_id == '4855':
            dispute_r = 'Product/Service not received'
        elif dispute_id == '4853':
            dispute_r = 'General'
        elif dispute_id == '12.5':
            dispute_r = 'Incorrect amount'
        elif dispute_id == '12.6.1' or dispute_id == '4834':
            dispute_r = 'Duplicate'
        elif dispute_id == '13.5' or dispute_id == '13.3':
            dispute_r = 'Not as described'
        elif dispute_id == '13.7' or dispute_id == '12.6.2' or dispute_id == '13.6':
            dispute_r = 'Credit not issued'
        else:
            dispute_r = ''

        info = {
            'reference': row['purchase_id'],
            'booking': row['transaction_key'],
            'dsp': row['action_key'],
            'cx_name': row['customer_name'],
            'rx_name': row['receiver_name'],
            'first_day': booking_date,
            'second_day': sent_date,
            's_amount': send_amount,
            's_currency': from_currency,
            'r_amount': receive_amount,
            'r_currency': to_currency,
            'reason_nr': dispute,
            'trx_id': token,
            'partner': outgoing_acc,
            'arn': row["Acquirer Reference Number"],
            'eur_eur_fee': to_currency_fee,
            'converted': converted,
            'reason': dispute_r
        }

        doc.render(info)
        doc.save(f"/Users/valerijus.kracius/Downloads/{row['purchase_id']}_Dispute_id_{row['action_key']}.docx")

    else:
        pass


privat_fil = data[((data['outgoing_bank_account_code'] == "ua_privatbank_usd") |
                  (data['outgoing_bank_account_code'] == "ua_privatbank_eur") |
             (data['outgoing_bank_account_code'] == "ua_privatbank_uah")) & (data['breakdown_type'] == "Chargeback (ADJM)")]
privat_bank = privat_fil[['payout_token', 'partner_token', 'sent_date', 'Dispute Indicator']]

with open('/Users/valerijus.kracius/Downloads/privat_bank.txt','w') as file:
    file.write(f"Hello team, please provide proofs of payments for: \n")
    for index1, row1 in privat_bank.iterrows():
        if 'RPDL' == row1['Dispute Indicator']:
            file.write(f"{row1['payout_token']}, {row1['partner_token']}, {row1['sent_date']}\n")
    file.write(f'Thank you in advance!\n')