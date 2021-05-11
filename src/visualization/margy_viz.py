import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def report_on_categories(df, category_feature, target_col_name, identifier_column, folder ='../../reports/Margy_investigation/figures/'):

    groupby_train = df.groupby(category_feature).count()[identifier_column]
    groupby_train.to_csv(f'../../reports/Margy_investigation/reports/{target_col_name}_by_{category_feature}_breakdown.csv')

    success_rate_train = df.groupby(category_feature).mean()[target_col_name]

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 16
    fig_size[1] = 16
    plt.rcParams["figure.figsize"] = fig_size

    plt.subplot(211)
    plt.bar(groupby_train.index, groupby_train)
    plt.xticks(groupby_train.index, groupby_train.index, rotation=90)
    plt.title('Volumes by category')

    plt.subplot(212)
    plt.bar(success_rate_train.index, success_rate_train)
    plt.title(f'average_{target_col_name}')
    plt.xticks(success_rate_train.index, success_rate_train.index,rotation=90)

    plt.savefig(f'{folder}{target_col_name}_by_{category_feature}_breakdown.png')
    plt.clf()
    return


# def data_cleaning_per_viz(data):
#     # data = data.set_index(keys='CcLog_id', drop=True)
#     data = data.reset_index(drop=True)
#     data['transaction_approved'] = data['CcStatus_id'].apply(lambda x : 1 if x == 4 else 0) # This column will be the target
#     data = data.drop(columns=['Unnamed: 0', 'CcStatus_id', 'Service_id'])
#     return data
#
#
# def grouping_small_categories_as_other(data, category_feature, identifier_column):
#     groupby_train = data.groupby(category_feature).count()[identifier_column]
#     groupby_train = groupby_train.reset_index()
#     groupby_train = groupby_train.sort_values(by=[identifier_column], ascending=False)
#     total_pop = np.sum(groupby_train[identifier_column])
#     groupby_train = groupby_train[groupby_train[identifier_column] > 0.05 * total_pop]
#     top_categories = list(groupby_train[category_feature])
#     data[category_feature+'_binned'] = data[category_feature].apply(lambda x: x if x in top_categories else 'other')
#     return data


if __name__ == '__main__':
    data_1 = pd.read_csv('../../data/raw/member_data_raw_filtered_margy.csv')
    country_mapping = pd.read_csv('../../data/raw/country_mapping.csv')
    data_1 = data_1.merge(country_mapping, left_on='country_code', right_on='alpha_2', how='left', suffixes=('', '_member'))
    data_1 = data_1.merge(country_mapping, left_on='card_country_code', right_on='alpha_2', how='left', suffixes=('', '_card'))

    data_1['fraud_indicator'] = data_1['new_settlement_36_fraud_30'].apply(lambda x: 1 if float(x) > 0 else 0)
    data_1['cb_indicator'] = data_1['chargebacks'].apply(lambda x: 1 if float(x) > 0 else 0)

    # data_1['local_date_added'].fillna('1970/01/31 00:00:00', inplace=True)
    # data_1['local_date_added'] = pd.to_datetime(data_1['local_date_added'], format= '%Y/%m/%d %H:%M:%S')
    # data_1['hour_of_day'] = data_1['local_date_added'].dt.hour
    # data_1['day_of_month'] = data_1['local_date_added'].dt.day
    # data_1['day_of_week'] = data_1['local_date_added'].dt.dayofweek

    data_1['customer_value'] = data_1['amount_paid'] - data_1['chargeback_amount'] - data_1['chargebacks']*20 - data_1['refund_total']
    print(data_1.head())
    feature_list = ['region', 'sub_region', 'region_card', 'sub_region_card', 'is_trial_member', 'start_date', 'signup_flow', 'device', 'mediatype',
     'product_id', 'browser', 'os', 'card_brand', 'card_subtype', 'card_country', 'card_country_code', 'account_tier']

    targets_list = ['customer_value', 'cb_indicator', 'fraud_indicator', 'num_successful_rebills', 'amount_paid', 'is_refunded_member',
                    'transactions', 'settlements', 'settlement_total', 'refunds', 'refund_total', 'chargebacks', 'chargeback_amount']

    for feature in feature_list:
        for target in targets_list:
            data_1[feature] = data_1[feature].astype(str)
            report_on_categories(data_1, feature, target_col_name=target, identifier_column='member_id')

