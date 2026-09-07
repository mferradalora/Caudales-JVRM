import os
import time
import requests
import pandas as pd

ARCHIVO_CSV = "caudales_jvrm.csv"

# Diccionario para convertir el mes abreviado a número
MESES_ES = {
    'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'ago': '08',
    'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
}

def normalizar_fecha(fecha_str):
    """Convierte '07/sep/2026 8:00' a formato ISO '2026-09-07 08:00:00' para poder ordenar."""
    try:
        partes = fecha_str.strip().split(' ')
        fecha_partes = partes[0].split('/')
        hora_partes = partes[1].split(':')
        
        dia = fecha_partes[0].zfill(2)
        mes = MESES_ES.get(fecha_partes[1].lower(), '01')
        anio = fecha_partes[2]
        
        hora = hora_partes[0].zfill(2)
        minuto = hora_partes[1].zfill(2)
        
        return f"{anio}-{mes}-{dia} {hora}:{minuto}:00"
    except Exception:
        return fecha_str

def extraer_y_guardar_datos():
    # Timestamp en milisegundos para simular la petición dinámica del navegador
    timestamp_ms = int(time.time() * 1000)
    url = f"https://jvriomaipo.cl/?json=1&t={timestamp_ms}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jvriomaipo.cl/'
    }

    print(f"Consultando API de JVRM: {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        json_data = response.json()
    except Exception as e:
        print(f"❌ Error al consultar la API: {e}")
        return

    if not json_data.get("exito") or "datos" not in json_data:
        print("⚠️ La API no devolvió datos estructurados o la respuesta no fue exitosa.")
        return

    registros = []
    for elem in json_data["datos"]:
        fecha_orig = elem.get("fecha", "")
        fecha_iso = normalizar_fecha(fecha_orig)
        
        registros.append({
            "Fecha_Hora": fecha_iso,
            "Q_Tot_m3s": elem.get("valor_AC", "-"),
            "Q_SinReg_m3s": elem.get("valor_AA", "-"),
            "Dot_SinReg_ls_acc": elem.get("valor_AB", "-"),
            "Q_Rep1_m3s": elem.get("valor_AE", "-"),
            "Dot1_ls_acc": elem.get("valor_AF", "-"),
            "Q_Rep2_m3s": elem.get("valor_AG", "-"),
            "Dot2_ls_acc": elem.get("valor_AH", "-"),
            "Aporte_Total_m3s": elem.get("valor_AD", "-"),
            "Turbiedad_UNT": elem.get("valor_GD", "-")
        })

    df_nuevos = pd.DataFrame(registros)

    # Combinación con CSV existente y eliminación de duplicados por Fecha_Hora
    if os.path.exists(ARCHIVO_CSV):
        df_existente = pd.read_csv(ARCHIVO_CSV)
        
        # Elimina la columna Fecha_Texto en caso de que ya existiera en el CSV previo
        if "Fecha_Texto" in df_existente.columns:
            df_existente = df_existente.drop(columns=["Fecha_Texto"])
            
        df_final = pd.concat([df_existente, df_nuevos], ignore_index=True)
        df_final = df_final.drop_duplicates(subset=["Fecha_Hora"], keep="last")
    else:
        df_final = df_nuevos

    # Ordenar por fecha y hora de forma ascendente
    df_final = df_final.sort_values(by="Fecha_Hora").reset_index(drop=True)
    
    df_final.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8")
    print(f"✅ Proceso exitoso. Registros acumulados en '{ARCHIVO_CSV}': {len(df_final)}")

if __name__ == "__main__":
    extraer_y_guardar_datos()

