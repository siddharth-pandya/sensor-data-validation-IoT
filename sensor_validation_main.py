import numpy as np
import serial
import time
import streamlit as st
import pandas as pd
from pandas import read_csv
from pandas import DataFrame
import statsmodels as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults64
import statistics
from sklearn import metrics
from datetime import datetime,date
//1.
@st.cache(suppress_st_warning=True)
def model_arima():
series2 = read_csv('temp.csv', index_col=0, parse_dates=True, squeeze=True)
X = series2.values
size2 = int(len(X) * 0.66)
train, test = X[0:size2], X[size2:len(X)]
hist = [x for x in train]
arr=np.zeros((len(test), 2))
preds = list()
for m in range(len(test)):
model = ARIMA(hist, order=(5,1,0))
model_fit = model.fit(disp=0)
output = model_fit.forecast()
yp = output[0]
preds.append(yp)
ob = test[m]
hist.append(ob)
print('predicted=%f, expected=%f' % (yp, ob))
arr[m][0]=yp
arr[m][1]=ob
clean_arr=[[item for item in row] for row in arr]
df_pred=pd.DataFrame(clean_arr, columns=['Predicted','Expected'])
error_mse = metrics.mean_squared_error(test, preds)
error_mae = metrics.mean_absolute_error(test,preds)
error_r2=metrics.r2_score(test,preds)
print('Test MSE: %.3f' % error_mse)
print('Test MAE: %.3f' % error_mae)
print('Test Coefficient of Determination: %.3f' % error_r2)65
plt.plot(test, color='blue')
plt.show()
plt.plot(preds, color='red')
plt.show()
return model_fit,df_pred
//2.
@st.cache(suppress_st_warning=True)
def real_time():
ser1 = serial.Serial('com6',115200)
time.sleep(2)
dat=[]
l_date=[]
l_temp=[]
today = str(date.today())
for i in range(0,10):
incoming = str (ser1.readline())
tem=float(incoming[2:7])
today = str(date.today())
l_date.append(today)
l_temp.append(tem)
print(today)
print(tem)
dat.append(today)
zippedList = list(zip(l_date,l_temp))
dfr = pd.DataFrame(zippedList, columns = ['Date' , 'Temperature'])
s=0.0
for item in l_temp:
s=s+item
te=(s/len(l_temp))
return dfr,te
//3.
def main():66
st.title('Temperature Machine')
st.header('Real-Time Temperature Readings')
df,temp_iot=real_time()
st.dataframe(df)
df.plot(x ='Date', y='Temperature', kind = 'line',title='Real-time plot')
plt.show()
st.pyplot()
st.subheader('Conclusions from Real-Time temperature table and plot')
st.markdown('The real-time average temperture from the IoT sensor records **%.4f degree
Celcius**'%temp_iot)
st.header('Model Predictions')
st.subheader('The following are the forecasted predictions and actual readings:')
mod_fit,df0=model_arima()
st.dataframe(df0)
final_pred=mod_fit.forecast()[0]
error_calc=mod_fit.forecast()[1]
conf_int=mod_fit.forecast()[2]
mini=conf_int[0][0]
maxi=conf_int[0][1]
st.markdown('The predicted temperature by model is **%.4f degree
Celcius**'%final_pred[0])
st.markdown('The model-predicted range in which the temperature from IoT sensor can lie
is between _%.4f degree Celcius_ and _%.4f degree Celcius_'%(mini,maxi))
st.subheader('Data Validation for IoT Sensor')
if(temp_iot<maxi and temp_iot>mini):
st.markdown('The real-time value from sensor which is **%f degree Celcius** lies
well within the model predicted range i.e. Between **_%f degree Celcius_** and **_%f degree
Celcius_**'%(temp_iot,mini,maxi))
st.write('Hence the sensor is working correctly.')67
st.markdown('And the correct present temperature is ** %.4f degree Celcius** as
recorded by the IoT sensor.'%temp_iot)
else:
st.write('The real time value from sensor may be incorrect, as it is out of model
predicted range')
st.write('Hence the sensor is not working correctly')
st.markdown('So the correct present temperature should be ** %.4f degree Celcius**
and not the temperature recorded by IoT sensor (i.e. _%.4f degree Celcius_)
'%(final_pred[0],temp_iot))
if __name__ == "__main__":
main()
