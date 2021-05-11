import pandas as pd

raw_member_df = pd.read_csv('../../data/raw/member_data_raw.csv')


raw_member_df = raw_member_df[raw_member_df['start_date'] > '2021-03-15']
print(raw_member_df.head())
raw_member_df = raw_member_df[raw_member_df['amount_paid'] > 0]
raw_member_df = raw_member_df[raw_member_df['affiliate_id'] == 129304]
print(raw_member_df.head())
raw_member_df.to_csv('../../data/raw/v.csv')
