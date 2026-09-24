import os
import time
import requests
import pandas as pd

ARCHIVOS = {
    'lluvia': 'lluvia_jvrm.csv',
    'nieve': 'nieve_jvrm.csv'
}

MESES_ES = {
    'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'ago': '08',
    'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
}

def normalizar_fecha(fecha_str):
    """
    Normaliza formatos variables de fecha a ISO 'YYYY-MM-DD HH:MM:SS'.
    Maneja: '23/9/2026 8:00', '21/sep/26 8:00' y '07/may/26'.
    """
    if not fecha_str or not isinstance(fecha_str, str):
        return fecha_str
    
    try:
        # Limpiar barra invertida de escape y espacios
        fecha_str = fecha_str.replace('\\', '').strip()
        partes = fecha_str.split(' ')
        fecha_partes = partes[0].split('/')
        
        dia = fecha_partes[0].zfill(2)
        
        # Procesar mes (puede ser número o texto)
        mes_raw = fecha_partes[1].lower()
        if mes_raw.isdigit():
            mes = mes_raw.zfill(2)
        else:
            mes = MESES_ES.get(mes_raw[:3], '01')
            
        # Procesar año (2 o 4 dígitos)
        anio = fecha_partes[2]
        if len(anio) == 2:
            anio = f"20{anio}"
            
        # Procesar hora (si no existe, se asume 08:00:00)
        if len(partes) > 1:
            hora_partes = partes[1].split(':')
            hora = hora_partes[0].zfill(2)
            minuto = hora_partes[1].zfill(2) if len(hora_partes) > 1 else '00'
        else:
            hora = "08"
            minuto = "00"
            
        return f"{anio}-{mes}-{dia} {hora}:{minuto}:00"
    except Exception:
        return fecha_str


def extraer_y_guardar_lluvia():
    """Extrae precipitaciones pluviales (mm) y actualiza lluvia_jvrm.csv."""
    timestamp_ms = int(time.time() * 1000)
    url = f"https://jvriomaipo.cl/caudal-del-maipo/?json=1&type=lluvia&t={timestamp_ms}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jvriomaipo.cl/'
    }

    print(f"\n🌧️ Consultando API de Lluvia: {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        json_data = response.json()
    except Exception as e:
        print(f"❌ Error al consultar la API de Lluvia: {e}")
        return

    if not json_data.get("exito") or "datos" not in json_data:
        print("⚠️ La API de Lluvia no devolvió datos exitosos.")
        return

    registros = []
    for elem in json_data["datos"]:
        registros.append({
            "Fecha_Hora": normalizar_fecha(elem.get("fecha", "")),
            "La_Obra_JVRM_mm": elem.get("valor_C", "-"),
            "La_Obra_EMOS_DGA_mm": elem.get("valor_D", "-"),
            "BT_San_Carlos_SCM_mm": elem.get("valor_E", "-"),
            "BT_El_Clarillo_mm": elem.get("valor_F", "-"),
            "BT_Los_Morros_mm": elem.get("valor_G", "-"),
            "Isla_Lonquen_mm": elem.get("valor_H", "-"),
            "Qta_Normal_mm": elem.get("valor_I", "-"),
            "Embalse_EEY_mm": elem.get("valor_J", "-")
        })

    guardar_dataframe(pd.DataFrame(registros), ARCHIVOS['lluvia'])


def extraer_y_guardar_nieve():
    """Extrae altura de nieve (cm) y actualiza nieve_jvrm.csv."""
    timestamp_ms = int(time.time() * 1000)
    url = f"https://jvriomaipo.cl/caudal-del-maipo/?json=1&type=nieve&t={timestamp_ms}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jvriomaipo.cl/'
    }

    print(f"\n❄️ Consultando API de Nieve: {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        json_data = response.json()
    except Exception as e:
        print(f"❌ Error al consultar la API de Nieve: {e}")
        return

    if not json_data.get("exito") or "datos" not in json_data:
        print("⚠️ La API de Nieve no devolvió datos exitosos.")
        return

    registros = []
    for elem in json_data["datos"]:
        registros.append({
            "Fecha_Hora": normalizar_fecha(elem.get("fecha", "")),
            "Embalse_El_Yeso_cm": elem.get("valor_C", "-"),
            "Volcan_Maipo_cm": elem.get("valor_D", "-")
        })

    guardar_dataframe(pd.DataFrame(registros), ARCHIVOS['nieve'])


def guardar_dataframe(df_nuevos, archivo_csv):
    """Combina datos con el CSV existente, elimina duplicados y guarda."""
    if os.path.exists(archivo_csv):
        df_existente = pd.read_csv(archivo_csv)
        df_final = pd.concat([df_existente, df_nuevos], ignore_index=True)
        df_final = df_final.drop_duplicates(subset=["Fecha_Hora"], keep="last")
    else:
        df_final = df_nuevos

    df_final = df_final.sort_values(by="Fecha_Hora").reset_index(drop=True)
    df_final.to_csv(archivo_csv, index=False, encoding="utf-8")
    print(f"✅ Proceso exitoso. Registros en '{archivo_csv}': {len(df_final)}")


if __name__ == "__main__":
    extraer_y_guardar_lluvia()
    extraer_y_guardar_nieve()
