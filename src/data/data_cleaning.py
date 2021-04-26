import pandas as pd

raw_member_df = pd.read_csv('../../data/raw/member_data_raw.csv')
raw_member_df = raw_member_df[['is_trial_member', 'start_date', 'country_code', 'signup_flow', 'device', 'mediatype',
                               'site_id', 'product_id', 'browser', 'os', 'card_brand', 'card_subtype', 'card_country',
                               'card_country_code', 'account_tier', 'local_date_added',

                                'num_successful_rebills', 'amount_paid', 'is_refunded_member', 'chargeback_date', 'transactions',
                               'settlements', 'settlement_total', 'refunds', 'refund_total', 'chargebacks', 'chargeback_amount']]

raw_member_df = raw_member_df[raw_member_df['amount_paid'] > 0]
print(raw_member_df.columns)

raw_member_df.to_csv('../../data/raw/member_data_raw_filtered.csv')