import pandas as pd
import json

PLANILHA_CARD = "PDV Grupocard_Mar_2026 1.xlsx"
PLANILHA_PIU  = "PDVs_PIU_Mar_2026 1.xlsx"

def tratar(df):
    df.columns = df.columns.str.strip()
    df['Latitude']  = pd.to_numeric(df['Latitude'].astype(str).str.replace(',', '.'), errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'].astype(str).str.replace(',', '.'), errors='coerce')
    return df.dropna(subset=['Latitude', 'Longitude'])

lista = []

df = tratar(pd.read_excel(PLANILHA_CARD))
for _, r in df.iterrows():
    lista.append({
        "coords": [r['Latitude'], r['Longitude']],
        "popup":  f"<b>{r['Nome Fantasia']}</b><br>Bairro: {r['Bairro']}<br>Terminal: {r['Modelo Terminal']}",
        "bairro": str(r['Bairro']).strip().upper(),
        "tipo":   "CARD"
    })

df = tratar(pd.read_excel(PLANILHA_PIU))
for _, r in df.iterrows():
    lista.append({
        "coords": [r['Latitude'], r['Longitude']],
        "popup":  f"<b>{r['PDV']}</b><br>{r['Logradouro']}, {r['Numero']}<br>{r['Bairro']} - {r['Cidade']}",
        "bairro": str(r['Bairro']).strip().upper(),
        "tipo":   "PIU"
    })

with open("dados.json", "w", encoding="utf-8") as f:
    json.dump(lista, f, ensure_ascii=False)

print(f"✅ {len(lista)} pontos exportados para dados.json")