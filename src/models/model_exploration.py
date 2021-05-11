import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score
from datetime import datetime
from sklearn.svm import SVR

def print_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

print_now()
targets_list = ['customer_value', 'fraud_indicator', 'chargebacks', 'amount_paid']
y = pd.read_csv('../../data/interim/post_encoding.csv').drop(columns='Unnamed: 0')
print(y.columns)
y = y.head(100000)
X = y.drop(columns = targets_list)
y = y[['chargebacks']]

print_now()
reg = LinearRegression().fit(X, y)
y_hat = reg.predict(X)
print(r2_score(y,y_hat))
print_now()

svr = SVR().fit(X, y)
y_hat = svr.predict(X)
print(r2_score(y,y_hat))
print_now()

y = y['chargebacks'].values
sgd = SGDRegressor(random_state=0, max_iter=1000, tol=0.000001, warm_start=True)
sgd.fit(X, y)
y_hat= sgd.predict(X)
print(r2_score(y,y_hat))
for i in range(100):
    sgd.fit(X, y)
    y_hat = sgd.predict(X)
    print(r2_score(y,y_hat))

print_now()