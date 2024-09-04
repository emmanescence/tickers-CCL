import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Función para calcular el CCL
def calcular_ccl(cot_ar, cot_usd, ratio_conversion):
    return (cot_ar * ratio_conversion) / cot_usd

# Configuración de la aplicación Streamlit
st.title('Evolución de Precio Ajustado por CCL (usando el CCL de GGAL) - www.x.com/@iterAR_eco')

# Entradas del usuario
fecha_inicio = st.date_input('Fecha de inicio', value=pd.to_datetime('2023-01-01'))
fecha_fin = st.date_input('Fecha de fin', value=pd.to_datetime('2024-08-31'))
ticker_adicional = st.text_input('Ticker a analizar (ej. METR.BA)', 'METR.BA')

# Tickers y ratio de conversión predefinidos
ticker_ar = 'GGAL.BA'  # Ticker en Argentina
ticker_usd = 'GGAL'    # Ticker en NYSE (ADR)
ratio_conversion = 10  # Ratio de conversión para GGAL

# Descargar datos
if st.button('Generar gráfico'):
    data_ar = yf.download(ticker_ar, start=fecha_inicio, end=fecha_fin)
    data_usd = yf.download(ticker_usd, start=fecha_inicio, end=fecha_fin)
    data_adicional = yf.download(ticker_adicional, start=fecha_inicio, end=fecha_fin)

    # Alinear las fechas y calcular el CCL
    data_ar = data_ar['Adj Close']
    data_usd = data_usd['Adj Close']
    data_adicional = data_adicional['Adj Close']

    df_ccl = pd.DataFrame({
        'Cotizacion_AR': data_ar,
        'Cotizacion_USD': data_usd
    })
    df_ccl['CCL'] = calcular_ccl(df_ccl['Cotizacion_AR'], df_ccl['Cotizacion_USD'], ratio_conversion)

    # Alinear las fechas del ticker adicional con el CCL y calcular el precio ajustado por CCL
    df_ccl = df_ccl[['CCL']].dropna()
    df_adicional = pd.DataFrame({
        'Precio_Original': data_adicional
    })
    df_adicional = df_adicional.dropna()
    df_adicional = df_adicional.join(df_ccl, how='inner')
    df_adicional['Precio_Ajustado_CCL'] = df_adicional['Precio_Original'] / df_adicional['CCL']

    # Aplicar un estilo oscuro
    plt.style.use('dark_background')

    # Graficar la evolución del precio ajustado por CCL
    plt.figure(figsize=(10, 6))
    plt.plot(df_adicional.index, df_adicional['Precio_Ajustado_CCL'], label=f'{ticker_adicional} Ajustado por CCL', color='cyan')
    plt.title(f'Evolución de {ticker_adicional} Ajustado por CCL')
    plt.xlabel('Fecha')
    plt.ylabel('Precio Ajustado por CCL')
    plt.legend()
    plt.grid(True, color='gray')

    # Mostrar gráfico en Streamlit
    st.pyplot(plt)
