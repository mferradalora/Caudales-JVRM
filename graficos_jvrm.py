import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# 1. Cargar el archivo CSV
df = pd.read_csv('caudales_jvrm.csv')

# 2. Convertir la columna Fecha_Hora a datetime
df['Fecha_Hora'] = pd.to_datetime(df['Fecha_Hora'], errors='coerce')

# Convertir columnas a numéricas por si existen guiones '-' u otro carácter no numérico
cols_numericas = [
    'Q_Tot_m3s',
    'Q_SinReg_m3s',
    'Q_Rep1_m3s',
    'Q_Rep2_m3s',
    'Dot_SinReg_ls_acc',
    'Dot1_ls_acc',
    'Dot2_ls_acc',
    'Turbiedad_UNT',
]
for col in cols_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Limpiar filas con fecha nula y ordenar cronológicamente
df = df.dropna(subset=['Fecha_Hora']).sort_values('Fecha_Hora')
df = df.drop_duplicates(subset=['Fecha_Hora'])

# 3. Directorio para guardar las imágenes
output_dir = 'graficos'
os.makedirs(output_dir, exist_ok=True)


# Función auxiliar para aplicar el formato del eje X por día (dd-mm-yyyy)
def aplicar_formato_eje_x(ax):
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.xlabel('Fecha Reportada', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)


# -------------------------------------------------------------
# GRÁFICO 1: Caudales (m³/s)
# -------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(
    df['Fecha_Hora'],
    df['Q_Tot_m3s'],
    label='Q Total',
    marker='o',
    markersize=3,
    linewidth=1.5,
)
plt.plot(
    df['Fecha_Hora'],
    df['Q_SinReg_m3s'],
    label='Q Sin Reg',
    marker='o',
    markersize=3,
    linewidth=1.5,
)
plt.plot(
    df['Fecha_Hora'],
    df['Q_Rep1_m3s'],
    label='Q Rep 1',
    marker='o',
    markersize=3,
    linewidth=1.5,
)
plt.plot(
    df['Fecha_Hora'],
    df['Q_Rep2_m3s'],
    label='Q Rep 2',
    marker='o',
    markersize=3,
    linewidth=1.5,
)

plt.title('Caudales JVRM', fontsize=14, fontweight='bold', pad=12)
plt.ylabel('Caudal (m³/s)', fontsize=10)
aplicar_formato_eje_x(plt.gca())
plt.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'caudales.png'), dpi=120)
plt.close()

# -------------------------------------------------------------
# GRÁFICO 2: Dotaciones (l/s/acc)
# -------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(
    df['Fecha_Hora'],
    df['Dot_SinReg_ls_acc'],
    label='Dot Sin Reg',
    marker='o',
    markersize=3,
    linewidth=1.5,
)
plt.plot(
    df['Fecha_Hora'],
    df['Dot1_ls_acc'],
    label='Dot 1',
    marker='o',
    markersize=3,
    linewidth=1.5,
)
plt.plot(
    df['Fecha_Hora'],
    df['Dot2_ls_acc'],
    label='Dot 2',
    marker='o',
    markersize=3,
    linewidth=1.5,
)

plt.title('Dotaciones JVRM', fontsize=14, fontweight='bold', pad=12)
plt.ylabel('Dotación (l/s/acc)', fontsize=10)
aplicar_formato_eje_x(plt.gca())
plt.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dotaciones.png'), dpi=120)
plt.close()

# -------------------------------------------------------------
# GRÁFICO 3: Turbiedad (UNT)
# -------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(
    df['Fecha_Hora'],
    df['Turbiedad_UNT'],
    color='#d9534f',
    marker='o',
    markersize=3,
    linewidth=1.5,
)

plt.title('Turbiedad JVRM', fontsize=14, fontweight='bold', pad=12)
plt.ylabel('Turbiedad (UNT)', fontsize=10)
aplicar_formato_eje_x(plt.gca())
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'turbiedad.png'), dpi=120)
plt.close()

# -------------------------------------------------------------
# 4. Generar README.md
# -------------------------------------------------------------
readme_content = "# 📊 Monitoreo de Caudales, Dotaciones y Turbiedad - JVRM\n\n"
readme_content += "Visualización de parámetros reportados por la Junta de Vigilancia del Río Maipo (JVRM).\n\n"
readme_content += (
    "> *Los gráficos se actualizan cada 6 horas.*\n\n---\n\n"
)

readme_content += "## Caudales (m³/s)\n\n"
readme_content += "![Caudales JVRM](graficos/caudales.png)\n\n---\n\n"

readme_content += "## Dotaciones (l/s/acc)\n\n"
readme_content += "![Dotaciones JVRM](graficos/dotaciones.png)\n\n---\n\n"

readme_content += "## Turbiedad (UNT)\n\n"
readme_content += "![Turbiedad JVRM](graficos/turbiedad.png)\n\n---\n\n"

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("Gráficos y README.md actualizados correctamente.")
