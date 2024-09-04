import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Función para calcular el CCL
def calcular_ccl(cot_ar, cot_usd, ratio_conversion):
    return (cot_ar * ratio_conversion) / cot_usd

# Configuración de la aplicación Streamlit
st.title('Evolución de Precio Ajustado por CCL (usando el CCL de GGAL) - www.x.com/@iterAR_eco')

# Entradas del usuario
fecha_inicio = st.date_input('Fecha de inicio', value=pd.to_datetime('2023-01-01'))
fecha_fin = st.date_input('Fecha de fin', value=pd.to_datetime('2024-08-31'))
tickers_adicionales = st.multiselect('Tickers a analizar (ej. METR.BA, PAMP.BA)', ['METR.BA'])

# Tickers y ratio de conversión predefinidos
ticker_ar = 'GGAL.BA'  # Ticker en Argentina
ticker_usd = 'GGAL'    # Ticker en NYSE (ADR)
ratio_conversion = 10  # Ratio de conversión para GGAL

# Descargar datos
if st.button('Generar gráfico'):
    data_ar = yf.download(ticker_ar, start=fecha_inicio, end=fecha_fin)
    data_usd = yf.download(ticker_usd, start=fecha_inicio, end=fecha_fin)

    # Alinear las fechas y calcular el CCL
    data_ar = data_ar['Adj Close']
    data_usd = data_usd['Adj Close']

    df_ccl = pd.DataFrame({
        'Cotizacion_AR': data_ar,
        'Cotizacion_USD': data_usd
    })
    df_ccl['CCL'] = calcular_ccl(df_ccl['Cotizacion_AR'], df_ccl['Cotizacion_USD'], ratio_conversion)

    # Alinear las fechas del ticker adicional con el CCL y calcular el precio ajustado por CCL
    df_ccl = df_ccl[['CCL']].dropna()

    fig = go.Figure()

    for ticker in tickers_adicionales:
        data_adicional = yf.download(ticker, start=fecha_inicio, end=fecha_fin)['Adj Close'].dropna()
        df_adicional = pd.DataFrame({'Precio_Original': data_adicional})
        df_adicional = df_adicional.join(df_ccl, how='inner')
        df_adicional['Precio_Ajustado_CCL'] = df_adicional['Precio_Original'] / df_adicional['CCL']

        # Agregar la serie al gráfico interactivo
        fig.add_trace(go.Scatter(x=df_adicional.index, y=df_adicional['Precio_Ajustado_CCL'], mode='lines', name=f'{ticker} Ajustado por CCL'))

    # Configuración del gráfico
    fig.update_layout(
        title='Evolución de Precios Ajustados por CCL',
        xaxis_title='Fecha',
        yaxis_title='Precio Ajustado por CCL',
        template='plotly_dark',
        hovermode='x unified'
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig)
