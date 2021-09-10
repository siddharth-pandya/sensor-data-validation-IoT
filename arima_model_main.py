from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
import statistics
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas import DataFrame60
from pandas import read_csv
from sklearn import metrics
import statsmodels as sm
//2.
series1 = read_csv('temp.csv', index_col=0, parse_dates=True, squeeze=True)
print(series1.head())
print(series1.tail())
print(series1.shape)
series1.plot()
pyplot.show()
series_diff1 = series1.diff().fillna(series)
series_diff1.plot()
pyplot.show()
series_diff2 = series_diff1.diff().fillna(series_diff1)
series_diff2.plot()
pyplot.show()
//3.
plot_acf(series_diff1)
pyplot.show()
plot_pacf(series_diff1)
pyplot.show()
//4.
A1series = ARIMA(series, order=(1,1,1)).fit(transparams=False)
print(A1series.summary())
//5.
residuals1 = DataFrame(A1series.resid)
residuals1.plot()
pyplot.show()
residuals1.plot(kind='kde')
pyplot.show()
print(residuals1.describe())
//6.
X = series1.values61
size1 = int(len(X) * 0.66)
train, test = X[0:size1], X[size1:len(X)]
hist = [x for x in train]
arr=np.zeros((len(test), 2))
prediction = list()
for k in range(len(test)):
model = ARIMA(hist, order=(5,1,0))
model_fit = model.fit(disp=0)
output = model_fit.forecast()
yhat = output[0]
prediction.append(yhat)
obs = test[k]
hist.append(obs)
print('predicted=%f, expected=%f' % (yhat, obs))
arr[k][0]=yhat
arr[k][1]=obs
clean_arr=[[item for item in row] for row in arr]
df_pred=pd.DataFrame(clean_arr, columns=['Predicted','Expected'])
print(df_pred)
error_mse = metrics.mean_squared_error(test, prediction)
error_mae = metrics.mean_absolute_error(test,prediction)
error_r2=metrics.r2_score(test,prediction)
print('Test MSE: %.3f' % error_mse)
print('Test MAE: %.3f' % error_mae)
print('Test Coefficient of Determination: %.3f' % error_r2)# plot
pyplot.plot(test)
pyplot.plot(prediction, color='red')
pyplot.show()
//7.
pyplot.plot(test)
pyplot.show()
pyplot.plot(prediction, color='red')
pyplot.show()
