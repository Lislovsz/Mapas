import pandas as pd
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import traceback
app = Flask(__name__)
CORS(app)
PLANILHA_CARD = "PDV Grupocard_Mar_2026 1.xlsx"
PLANILHA_PIU = "PDVs_PIU_Mar_2026 1.xlsx"
def tratar_coordenadas(df):
    df.columns = df.columns.str.strip()
    df['Latitude'] = pd.to_numeric(
        df['Latitude'].astype(str).str.replace(',', '.'),
        errors='coerce'
    )
    df['Longitude'] = pd.to_numeric(
        df['Longitude'].astype(str).str.replace(',', '.'),
        errors='coerce'
    )
    return df.dropna(subset=['Latitude', 'Longitude'])
def carregar_card():
    try:
        df = pd.read_excel(PLANILHA_CARD)
        df = tratar_coordenadas(df)
        lista = []
        for _, linha in df.iterrows():
            bairro = str(linha['Bairro']).strip().upper()
            lista.append({
                "coords": [linha['Latitude'], linha['Longitude']],
                "popup": f"<b>{linha['Nome Fantasia']}</b><br>Bairro: {linha['Bairro']}<br>Terminal: {linha['Modelo Terminal']}",
                "bairro": bairro,
                "tipo": "CARD"
            })
        return lista
    except Exception:
        traceback.print_exc()
        return []





def carregar_piu():

    try:

        df = pd.read_excel(PLANILHA_PIU)

        df = tratar_coordenadas(df)



        lista = []



        for _, linha in df.iterrows():

            bairro = str(linha['Bairro']).strip().upper()



            lista.append({

                "coords": [linha['Latitude'], linha['Longitude']],

                "popup": f"<b>{linha['PDV']}</b><br>{linha['Logradouro']}, {linha['Numero']}<br>{linha['Bairro']} - {linha['Cidade']}",

                "bairro": bairro,

                "tipo": "PIU"

            })



        return lista



    except Exception:

        traceback.print_exc()

        return []





@app.route('/dados-pdv')

def obter_dados():

    dados = carregar_card() + carregar_piu()

    print(f"🔥 TOTAL: {len(dados)} pontos")

    return jsonify(dados)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':

    print("🚀 🚀 http://192.168.4.157:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)