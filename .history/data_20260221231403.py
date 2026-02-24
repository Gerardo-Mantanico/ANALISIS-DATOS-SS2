import csv
import os
import pandas as pd
from datetime import datetime
import re

def procesar_csv_a_inserts(carpeta_csv, nombre_tabla, columnas, delimitador=','):
    """
    Procesa archivos CSV y genera archivos SQL con inserts
    
    Args:
        carpeta_csv: Carpeta donde están los CSV
        nombre_tabla: Nombre de la tabla en BD
        columnas: Lista de nombres de columnas
        delimitador: Delimitador del CSV (por defecto ',')
    """
    
    # Crear carpeta para los archivos SQL
    carpeta_sql = "inserciones_sql"
    if not os.path.exists(carpeta_sql):
        os.makedirs(carpeta_sql)
    
    # Archivo SQL unificado
    archivo_unificado = os.path.join(carpeta_sql, "todos_los_inserts.sql")
    
    with open(archivo_unificado, 'w', encoding='utf-8') as sql_unificado:
        # Escribir encabezado
        sql_unificado.write(f"-- INSERTS PARA TABLA: {nombre_tabla}\n")
        sql_unificado.write(f"-- GENERADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        sql_unificado.write(f"-- ARCHIVOS PROCESADOS: {len(os.listdir(carpeta_csv))}\n")
        sql_unificado.write("="*80 + "\n\n")
        
        # Procesar cada archivo CSV
        archivos_csv = [f for f in os.listdir(carpeta_csv) if f.endswith('.csv')]
        
        for archivo_csv in archivos_csv:
            ruta_csv = os.path.join(carpeta_csv, archivo_csv)
            try:
                año = extraer_año(archivo_csv)
            except Exception:
                año = "DESCONOCIDO"
            print(f"📄 Procesando: {archivo_csv} (Año: {año})")
            try:
                # Leer CSV con diferentes codificaciones
                df = leer_csv_con_codificacion(ruta_csv, delimitador)
                # Saltar archivos vacíos o con error de servidor
                if df.empty or (len(df.columns) == 1 and df.columns[0].lower().startswith('internal server error')):
                    print(f"  ⚠️  Archivo vacío o con error de servidor: {archivo_csv}")
                    continue
                # Mostrar información del CSV
                print(f"  📊 Filas: {len(df)}, Columnas: {len(df.columns)}")
                print(f"  📋 Columnas encontradas: {list(df.columns)}")
                # Generar inserts para este archivo
                inserts_por_archivo = []
                for idx, fila in df.iterrows():
                    valores = []
                    for col in columnas:
                        if col in df.columns:
                            valor = fila[col]
                            valor_formateado = formatear_valor_sql(valor)
                            valores.append(valor_formateado)
                        else:
                            valores.append('NULL')
                    insert = f"INSERT INTO {nombre_tabla} ({', '.join(columnas)}) VALUES ({', '.join(valores)});"
                    inserts_por_archivo.append(insert)
                sql_unificado.write(f"-- INSERTS DESDE: {archivo_csv} (Año: {año})\n")
                sql_unificado.write(f"-- Total registros: {len(inserts_por_archivo)}\n\n")
                batch_size = 1000
                for i in range(0, len(inserts_por_archivo), batch_size):
                    batch = inserts_por_archivo[i:i+batch_size]
                    sql_unificado.write(f"-- Batch {i//batch_size + 1}\n")
                    for insert in batch:
                        sql_unificado.write(insert + "\n")
                    sql_unificado.write("\n")
                sql_unificado.write("\n" + "="*60 + "\n\n")
                print(f"  ✅ Generados {len(inserts_por_archivo)} inserts para {archivo_csv}")
                guardar_inserts_individuales(inserts_por_archivo, carpeta_sql, archivo_csv, año, nombre_tabla)
            except Exception as e:
                print(f"  ❌ Error procesando {archivo_csv}: {e}")
        print(f"\n✅ Archivo SQL unificado generado: {archivo_unificado}")

def leer_csv_con_codificacion(ruta_csv, delimitador):
    """
    Intenta leer CSV con diferentes codificaciones
    """
    codificaciones = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in codificaciones:
        try:
            df = pd.read_csv(ruta_csv, encoding=encoding, delimiter=delimitador, 
                           on_bad_lines='skip', low_memory=False)
            print(f"  ✅ Leído con encoding: {encoding}")
            return df
        except:
            continue
    
    # Último intento con configuración más flexible
    try:
        df = pd.read_csv(ruta_csv, encoding='utf-8', delimiter=delimitador, 
                       engine='python', on_bad_lines='skip')
        return df
    except:
        return pd.DataFrame()

def extraer_año(nombre_archivo):
    """
    Extrae el año del nombre del archivo
    """
    patrones = [r'(20\d{2})', r'(\d{4})']
    for patron in patrones:
        match = re.search(patron, nombre_archivo)
        if match:
            return match.group(1)
    return "DESCONOCIDO"

def formatear_valor_sql(valor):
    """
    Formatea un valor para ser usado en SQL
    """
    if pd.isna(valor) or valor is None:
        return 'NULL'
    
    if isinstance(valor, (int, float)):
        return str(valor)
    
    if isinstance(valor, (datetime, pd.Timestamp)):
        return f"'{valor.strftime('%Y-%m-%d')}'"
    
    # Limpiar y escapar el string
    valor_str = str(valor).strip()
    valor_str = valor_str.replace("'", "''")  # Escapar comillas simples
    valor_str = valor_str.replace('"', '""')  # Escapar comillas dobles
    
    return f"'{valor_str}'"

def guardar_inserts_individuales(inserts, carpeta_sql, archivo_csv, año, nombre_tabla):
    """
    Guarda los inserts en un archivo individual por CSV
    """
    nombre_base = os.path.splitext(archivo_csv)[0]
    archivo_sql = os.path.join(carpeta_sql, f"{nombre_base}_inserts.sql")
    
    with open(archivo_sql, 'w', encoding='utf-8') as f:
        f.write(f"-- INSERTS DESDE: {archivo_csv}\n")
        f.write(f"-- AÑO: {año}\n")
        f.write(f"-- TABLA: {nombre_tabla}\n")
        f.write(f"-- TOTAL REGISTROS: {len(inserts)}\n")
        f.write("="*60 + "\n\n")
        
        for insert in inserts:
            f.write(insert + "\n")
    
    print(f"  💾 Guardado individual: {archivo_sql}")

def analizar_estructura_csv(carpeta_csv):
    """
    Función auxiliar para analizar la estructura de los CSV
    """
    print("\n🔍 ANALIZANDO ESTRUCTURA DE CSVs")
    print("="*50)
    
    archivos_csv = [f for f in os.listdir(carpeta_csv) if f.endswith('.csv')]
    todas_columnas = set()
    info_archivos = {}
    
    for archivo in archivos_csv[:5]:  # Analizar primeros 5
        ruta = os.path.join(carpeta_csv, archivo)
        try:
            df = leer_csv_con_codificacion(ruta, ',')
            info_archivos[archivo] = {
                'columnas': list(df.columns),
                'filas': len(df),
                'tipos': df.dtypes.to_dict()
            }
            todas_columnas.update(df.columns)
            print(f"\n📁 {archivo}:")
            print(f"  Filas: {len(df)}")
            print(f"  Columnas: {list(df.columns)}")
        except Exception as e:
            print(f"  Error analizando {archivo}: {e}")
    
    print("\n📊 COLUMNAS ENCONTRADAS (muestra):")
    for i, col in enumerate(sorted(todas_columnas), 1):
        print(f"  {i}. {col}")
    
    return info_archivos, list(todas_columnas)

def generar_reporte_insercion(carpeta_sql):
    """
    Genera un reporte de los archivos SQL creados
    """
    print("\n📋 REPORTE DE ARCHIVOS GENERADOS")
    print("="*50)
    
    archivos_sql = [f for f in os.listdir(carpeta_sql) if f.endswith('.sql')]
    
    total_inserts = 0
    for archivo in archivos_sql:
        ruta = os.path.join(carpeta_sql, archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            num_inserts = contenido.count('INSERT INTO')
            tamaño = os.path.getsize(ruta) / 1024  # KB
            
            print(f"📄 {archivo}:")
            print(f"  📊 Inserts: {num_inserts}")
            print(f"  💾 Tamaño: {tamaño:.2f} KB")
            
            total_inserts += num_inserts
    
    print(f"\n✅ TOTAL INSERTS GENERADOS: {total_inserts}")
    print(f"📁 Carpeta: {os.path.abspath(carpeta_sql)}")

def crear_script_insercion_masiva(carpeta_sql, nombre_tabla):
    """
    Crea un script SQL para insertar todos los datos en la base de datos
    """
    script_masivo = os.path.join(carpeta_sql, "00_ejecutar_todos_los_inserts.sql")
    
    with open(script_masivo, 'w', encoding='utf-8') as f:
        f.write("-- SCRIPT PARA EJECUTAR TODOS LOS INSERTS\n")
        f.write("-- ======================================\n\n")
        f.write("BEGIN TRANSACTION;\n\n")
        
        # Desactivar triggers/índices temporalmente para mejor rendimiento
        f.write("-- Optimizaciones para inserción masiva\n")
        f.write(f"ALTER TABLE {nombre_tabla} DISABLE TRIGGER ALL;\n\n")
        
        # Ordenar archivos para ejecución
        archivos_sql = sorted([f for f in os.listdir(carpeta_sql) 
                              if f.endswith('.sql') and f != "00_ejecutar_todos_los_inserts.sql"])
        
        for archivo in archivos_sql:
            ruta_relativa = archivo
            f.write(f"-- Ejecutar: {archivo}\n")
            f.write(f"\\i {ruta_relativa}\n\n")
        
        # Reactivar triggers
        f.write(f"ALTER TABLE {nombre_tabla} ENABLE TRIGGER ALL;\n\n")
        f.write("COMMIT;\n")
        
        f.write("\n-- FIN DEL SCRIPT\n")
    
    print(f"✅ Script de ejecución masiva creado: {script_masivo}")

# EJEMPLO DE USO - COMPLETA ESTO CON TUS DATOS
if __name__ == "__main__":
    print("🔄 GENERADOR DE INSERTS SQL DESDE CSV")
    print("="*50)
    
    # CONFIGURACIÓN - MODIFICA ESTO SEGÚN TU BASE DE DATOS
    CARPETA_CSV = "descargas_estudiantes"  # Carpeta con los CSV descargados
    NOMBRE_TABLA = "estudiantes_inscritos"  # Nombre de tu tabla
    
    # Define las columnas de tu tabla - ¡MODIFICA ESTO!
    COLUMNAS_TABLA = [
        'correlativo_estudiante',
        'nombre_carrera',
        'fecha_inscripcion',
        'anio_inscripcion',
        'sexo',
        'pais_nacionalidad',
        'tipo_inscripcion'
    ]
    
    # Paso 1: Analizar estructura de los CSV
    print("\n🔍 ANALIZANDO ARCHIVOS CSV...")
    info_columnas, columnas_encontradas = analizar_estructura_csv(CARPETA_CSV)
    
    print("\n⚠️  IMPORTANTE: Las columnas de tu tabla deben coincidir con las del CSV")
    print("   Por favor, verifica que las columnas definidas arriba sean correctas")
    
    respuesta = input("\n¿Continuar con la generación de inserts? (s/n): ")
    
    if respuesta.lower() == 's':
        # Paso 2: Generar inserts
        print("\n🔄 GENERANDO INSERTS SQL...")
        procesar_csv_a_inserts(CARPETA_CSV, NOMBRE_TABLA, COLUMNAS_TABLA)
        
        # Paso 3: Generar reporte
        generar_reporte_insercion("inserciones_sql")
        
        # Paso 4: Crear script de ejecución masiva
        crear_script_insercion_masiva("inserciones_sql", NOMBRE_TABLA)
        
        print("\n✨ PROCESO COMPLETADO!")
        print("📁 Revisa la carpeta 'inserciones_sql' para ver los archivos generados")
    else:
        print("❌ Proceso cancelado")