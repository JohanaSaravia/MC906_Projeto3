import sys
import math

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import date
from datetime import datetime
import visuals_and_graphics as vag
from process import process


# Esse programa tenta predizer o valor de fechamento da ação na data fornecida, baseando-se na data e os valores de abertura anteriores e previstos
# através de uma regressão linear múltipla

data, dates_deltaToPredict, datesToPredict = process()

x_v = data[['Date_delta', 'Open']]
y_v = data[['Close']]

print("Correlation between Date and Closing values:")
print(data[['Date_delta', 'Open', 'Close']].corr())

model = LinearRegression()
model.fit(x_v, y_v)

print("model score:")
print(round(model.score(x_v, y_v), 5))

# Previsão do valor de fechamento para as datas após o último dia dos dados disponíveis,
# para valor de abertura do primeiro dia da previsão utiliza-se o valor de fechamento do último dia dos dados disponíveis
# para valor de abertura dos demais dias após isso utiliza-se o valor previsto de fechamento do dia anterior
openValue = data.loc[len(data['Open'])-1, 'Open']
i = 0
df2 = pd.DataFrame(columns=['Date', 'Close'])
while i < len(dates_deltaToPredict):

    dd = dates_deltaToPredict[i]
    closingValue = model.predict([[dd, openValue]])[0][0]
    date = datesToPredict[i]
    df2 = df2.append({'Date': date, 'Close': closingValue}, ignore_index=True)

    # Valor de abertura do dia seguinte é sempre o valor de fechamento do dia anterior
    openValue = closingValue
    i = i + 1

# Graph correlating the Open and Close stock values
vag.fig_sct_open_close(data)

# Generating a comparative graph between the prices we have and future prices our model predicted
vag.fig_real_predicted_values(data, df2, 'Regressao Linear Multipla usando Date e Open')