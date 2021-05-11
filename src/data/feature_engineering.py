import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    df = pd.read_csv('../../data/raw/member_data_raw_filtered.csv')
    country_mapping = pd.read_csv('../../data/raw/country_mapping.csv')
    df = df.merge(country_mapping, left_on='country_code', right_on='alpha_2', how='left', suffixes=('', '_member'))
    df = df.merge(country_mapping, left_on='card_country_code', right_on='alpha_2', how='left', suffixes=('', '_card'))

    df['fraud_indicator'] = df['fraud_120'].apply(lambda x: 1 if float(x) > 0 else 0)
    df['customer_value'] = df['amount_paid'] - df['chargeback_amount'] - df['chargebacks'] * 20 - df['refund_total']
    feature_list = ['region', 'sub_region', 'region_card', 'sub_region_card', 'is_trial_member', 'device', 'mediatype',
     'browser', 'os', 'card_brand', 'card_subtype', 'account_tier']
    # feature_list = ['sub_region', 'sub_region_card', 'is_trial_member', 'mediatype',
    #  'browser', 'os', 'card_brand', 'account_tier']
    targets_list = ['customer_value', 'fraud_indicator', 'chargebacks', 'amount_paid']
        # , 'num_successful_rebills', 'amount_paid', 'is_refunded_member',
        #             'transactions', 'settlements', 'settlement_total', 'refunds', 'refund_total', 'chargeback_amount']

    df = df[feature_list+targets_list]
    features_for_OHE = ['region', 'sub_region', 'region_card', 'sub_region_card', 'device', 'mediatype',
     'browser', 'os', 'card_brand', 'card_subtype', 'account_tier']
    # features_for_OHE = ['sub_region', 'sub_region_card', 'mediatype',
    #  'browser', 'os', 'card_brand', 'account_tier']

    for categorical_var in tqdm(features_for_OHE):
        enc = OneHotEncoder(handle_unknown='ignore')
        list_of_regions = np.unique(df[categorical_var].astype(str)).reshape(-1, 1)
        enc.fit(list_of_regions)
        OneHE_array = enc.transform(df[[categorical_var]]).toarray()
        OneHE_df = pd.DataFrame(OneHE_array, columns=enc.categories_)
        df = df.join(OneHE_df, rsuffix='_'+categorical_var)
    df = df.drop(columns=features_for_OHE)
    df.to_csv('../../data/interim/post_encoding.csv')