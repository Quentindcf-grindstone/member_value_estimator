from pydomo import Domo
import pandas as pd
from dotenv import dotenv_values
config = dotenv_values("../../.env")

domo = Domo(config['domo_client_id'], config['domo_secret'], api_host='api.domo.com')

member_data = domo.ds_get('82b72ffd-008e-460e-ae34-fe69d988197e')
member_data.to_csv('../../data/raw/member_data_raw.csv')
print('Data going from',min(member_data['start_date']), ' to', max(member_data['start_date']))

