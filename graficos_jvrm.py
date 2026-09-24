import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Directorio para guardar las imágenes
output_dir = 'graficos'
os.makedirs(output_dir, exist_ok=True)


# Función auxiliar para aplicar el formato del eje X por día (dd-mm-yyyy)
def aplicar_formato_eje_x(ax):
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.xlabel('Fecha Reportada', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)


# =============================================================
# 1. PROCESAR CAUDALES, DOTACIONES Y TURBIEDAD (caudales_jvrm.csv)
# =============================================================
if os.path.exists('caudales_jvrm.csv'):
    df_caudales = pd.read_csv('caudales_jvrm.csv')
    df_caudales['Fecha_Hora'] = pd.to_datetime(
        df_caudales['Fecha_Hora'], errors='coerce'
    )

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
        if col in df_caudales.columns:
            df_caudales[col] = pd.to_numeric(df_caudales[col], errors='coerce')

    df_caudales = (
        df_caudales.dropna(subset=['Fecha_Hora'])
        .sort_values('Fecha_Hora')
        .drop_duplicates(subset=['Fecha_Hora'])
    )

    # GRÁFICO 1: Caudales (m³/s)
    plt.figure(figsize=(10, 5))
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Q_Tot_m3s'],
        label='Q Total',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Q_SinReg_m3s'],
        label='Q Sin Reg',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Q_Rep1_m3s'],
        label='Q Rep 1',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Q_Rep2_m3s'],
        label='Q Rep 2',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.title('Caudales JVRM', fontsize=14, fontweight='bold', pad=12)
    plt.ylabel('Caudal (m³/s)', fontsize=10)
    aplicar_formato_eje_x(plt.gca())
    plt.legend(loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'caudales.png'), dpi=120)
    plt.close()

    # GRÁFICO 2: Dotaciones (l/s/acc)
    plt.figure(figsize=(10, 5))
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Dot_SinReg_ls_acc'],
        label='Dot Sin Reg',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Dot1_ls_acc'],
        label='Dot 1',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Dot2_ls_acc'],
        label='Dot 2',
        marker='o',
        markersize=3,
        linewidth=1.5,
    )
    plt.title('Dotaciones JVRM', fontsize=14, fontweight='bold', pad=12)
    plt.ylabel('Dotación (l/s/acc)', fontsize=10)
    aplicar_formato_eje_x(plt.gca())
    plt.legend(loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dotaciones.png'), dpi=120)
    plt.close()

    # GRÁFICO 3: Turbiedad (UNT)
    plt.figure(figsize=(10, 5))
    plt.plot(
        df_caudales['Fecha_Hora'],
        df_caudales['Turbiedad_UNT'],
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

# =============================================================
# 2. PROCESAR LLUVIA (lluvia_jvrm.csv)
# =============================================================
if os.path.exists('lluvia_jvrm.csv'):
    df_lluvia = pd.read_csv('lluvia_jvrm.csv')
    df_lluvia['Fecha_Hora'] = pd.to_datetime(
        df_lluvia['Fecha_Hora'], errors='coerce'
    )

    cols_lluvia = [c for c in df_lluvia.columns if c != 'Fecha_Hora']
    for c in cols_lluvia:
        df_lluvia[c] = pd.to_numeric(df_lluvia[c], errors='coerce')

    df_lluvia = (
        df_lluvia.dropna(subset=['Fecha_Hora'])
        .sort_values('Fecha_Hora')
        .drop_duplicates(subset=['Fecha_Hora'])
    )

    plt.figure(figsize=(10, 5))
    nombres_lluvia = {
        'La_Obra_JVRM_mm': 'La Obra (JVRM)',
        'La_Obra_EMOS_DGA_mm': 'La Obra EMOS (DGA)',
        'BT_San_Carlos_SCM_mm': 'BT San Carlos (SCM)',
        'BT_El_Clarillo_mm': 'BT El Clarillo',
        'BT_Los_Morros_mm': 'BT Los Morros',
        'Isla_Lonquen_mm': 'Isla Lonquén',
        'Qta_Normal_mm': 'Qta Normal',
        'Embalse_EEY_mm': 'Embalse EEY',
    }

    for col in cols_lluvia:
        label = nombres_lluvia.get(
            col, col.replace('_mm', '').replace('_', ' ')
        )
        plt.plot(
            df_lluvia['Fecha_Hora'],
            df_lluvia[col],
            label=label,
            marker='o',
            markersize=3,
            linewidth=1.5,
        )

    plt.title(
        'Precipitación Pluvial (Lluvia) JVRM',
        fontsize=14,
        fontweight='bold',
        pad=12,
    )
    plt.ylabel('Lluvia (mm)', fontsize=10)
    aplicar_formato_eje_x(plt.gca())
    plt.legend(loc='upper right', fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'lluvia.png'), dpi=120)
    plt.close()

# =============================================================
# 3. PROCESAR NIEVE (nieve_jvrm.csv)
# =============================================================
if os.path.exists('nieve_jvrm.csv'):
    df_nieve = pd.read_csv('nieve_jvrm.csv')
    df_nieve['Fecha_Hora'] = pd.to_datetime(
        df_nieve['Fecha_Hora'], errors='coerce'
    )

    cols_nieve = [c for c in df_nieve.columns if c != 'Fecha_Hora']
    for c in cols_nieve:
        df_nieve[c] = pd.to_numeric(df_nieve[c], errors='coerce')

    df_nieve = (
        df_nieve.dropna(subset=['Fecha_Hora'])
        .sort_values('Fecha_Hora')
        .drop_duplicates(subset=['Fecha_Hora'])
    )

    plt.figure(figsize=(10, 5))
    nombres_nieve = {
        'Embalse_El_Yeso_cm': 'Embalse El Yeso',
        'Volcan_Maipo_cm': 'Volcán Maipo',
    }

    for col in cols_nieve:
        label = nombres_nieve.get(col, col.replace('_cm', '').replace('_', ' '))
        plt.plot(
            df_nieve['Fecha_Hora'],
            df_nieve[col],
            label=label,
            marker='o',
            markersize=3,
            linewidth=1.5,
        )

    plt.title('Altura de Nieve JVRM', fontsize=14, fontweight='bold', pad=12)
    plt.ylabel('Altura de Nieve (cm)', fontsize=10)
    aplicar_formato_eje_x(plt.gca())
    plt.legend(loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'nieve.png'), dpi=120)
    plt.close()

# =============================================================
# 4. GENERAR README.md
# =============================================================
readme_content = (
    '# 📊 Monitoreo de Caudales, Precipitaciones y Turbiedad - JVRM\n\n'
)
readme_content += 'Visualización de parámetros reportados por la Junta de Vigilancia del Río Maipo (JVRM).\n\n'
readme_content += (
    '> *Los gráficos se actualizan automáticamente.*\n\n---\n\n'
)

if os.path.exists(os.path.join(output_dir, 'caudales.png')):
    readme_content += (
        '## Caudales (m³/s)\n\n![Caudales JVRM](graficos/caudales.png)\n\n---\n\n'
    )

if os.path.exists(os.path.join(output_dir, 'dotaciones.png')):
    readme_content += '## Dotaciones (l/s/acc)\n\n![Dotaciones JVRM](graficos/dotaciones.png)\n\n---\n\n'

if os.path.exists(os.path.join(output_dir, 'turbiedad.png')):
    readme_content += '## Turbiedad (UNT)\n\n![Turbiedad JVRM](graficos/turbiedad.png)\n\n---\n\n'

if os.path.exists(os.path.join(output_dir, 'lluvia.png')):
    readme_content += '## Precipitación Pluvial - Lluvia (mm)\n\n![Lluvia JVRM](graficos/lluvia.png)\n\n---\n\n'

if os.path.exists(os.path.join(output_dir, 'nieve.png')):
    readme_content += '## Precipitación Nival - Altura de Nieve (cm)\n\n![Nieve JVRM](graficos/nieve.png)\n\n---\n\n'

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print('Gráficos y README.md actualizados correctamente.')
