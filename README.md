# sensor-data-validation-IoT

- A temperature sensor phyiscally reads temperature in real-time, using an arduino connected to it. ( In terms of smart city, deploying number of IoT tempearture sensors).

- This read data , is displayed on a localhost server ( cloud based dashboard in terms of smart city scaling).

- Parallely on local host , or cloud a ARIMA model is trained with past 10 years data of temperature of that city. And a model is ready for predictions.

- Now, data collected in real-time from sensor is brought , a prediction is made by the ML model for that day, both are compared on localhost (cloud for larger scale).

- If the real-time data recieved by physical sensor is in a predictive limit decided by the ML model, it is correct, else the average of the correct predicted limit by the ML model is displayed on a web-based dashboard ( this web-based dashboard can be used by meterological department in the smart city, or by individual citizens by fetching details from cloud-based server, which will perform all collection, processing of data in real-time and comparing with model results and displaying on a web-based service)
