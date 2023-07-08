# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
#import cmdstanpy
#cmdstanpy.install_cmdstan(compiler=True)
class SPP:
    def s_pred(self):
        #cmdstanpy.install_cmdstan()
        #cmdstanpy.install_cmdstan(compiler=True)
        #START = "2015-01-01"
        START = "2018-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")
        st.write(TODAY)
        
        st.title('Stock Forecast App')

        stocks = ('2330.TW','2303.TW','8069.TW','2454.TW','2317.TW','^TWII','TSLA','GOOG', 'AAPL', 'MSFT', 'GME')
        selected_stock = st.selectbox('Select dataset for prediction', stocks)

        n_years = st.slider('Days of prediction:', 1, 60)
        #period = n_years * 365
        period = n_years

        @st.cache
        def load_data(ticker):
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data


        data_load_state = st.text('Loading data...')
        data = load_data(selected_stock)
        #data = load_data('GOOG')
        data_load_state.text('Loading data... done!')


        st.subheader('Major Holders')
        selected_stock = yf.Ticker(selected_stock)
        
        st.write(selected_stock.major_holders)
        
        st.subheader('Raw data')
        data = selected_stock.history(start = START, end = TODAY)
    
        st.write(data)
        st.write(data.tail())


        # Plot raw data
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open", fillcolor="red"))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
            fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)


        plot_raw_data()

        # Predict forecast with Prophet.
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Show and plot forecast
        st.subheader('Forecast data')
        st.write(forecast.tail())

        st.write(f'Forecast plot for {n_years} days')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
