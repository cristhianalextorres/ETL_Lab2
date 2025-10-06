from extract import DataExtractor
from monitor import  MonitorETL
from logger import LoggerETL
from load import DataLoader
import unidecode as ucode

file_path = "..\\data\\"
path_db = "..\\data\\lab2.db"

# Instancias

monitor = MonitorETL()
logger = LoggerETL(monitor=monitor)

try:
    logger.info("Inicio del proceso ETL")
    monitor.start()

    conn, log = DataLoader.init_db(path_db = path_db)
    logger.info(log)

    etl_monitor = """
    CREATE TABLE IF NOT EXISTS etl_monitor (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    registros_leidos INTEGER,
                    registros_validos INTEGER,
                    registros_descartados INTEGER,
                    duracion_segundos REAL,
                    error TEXT
    )
    """

    alumnos = """
    CREATE TABLE IF NOT EXISTS alumnos (
        id_alumno TEXT PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        grado INTEGER,
        correo TEXT,
        fecha_nacimiento DATE,
    )
    """

    calificaciones = """
    CREATE TABLE IF NOT EXISTS calificaciones (
        id_calificacion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alumno TEXT,
        asignatura TEXT,
        periodo INTEGER,
        nota REAL,
        FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
    )
    """

    matriculas = """
    CREATE TABLE IF NOT EXISTS matriculas (
        id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alumno TEXT,
        anio INTEGER,
        estado TEXT,
        jornada TEXT,
        FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
    )
    """

    tables = [
        ("etl_monitor", etl_monitor),
        ("alumnos", alumnos),
        ("calificaciones", calificaciones),
        ("matriculas", matriculas)
    ]

    # Crear todas las tablas en ciclo
    for name, create_sql in tables:
        log = DataLoader.create_table(conn= conn, create_table_sql = create_sql, table_name=name)
        logger.info(log)

    log, df_alumnos = DataExtractor.from_csv(ruta=file_path, archivo='alumnos.csv')
    logger.info(log)
    log, df_matriculas = DataExtractor.from_xml(ruta=file_path, archivo='matricula.xml')
    logger.info(log)
    log, df_calificaciones = DataExtractor.from_json(ruta=file_path, archivo='calificaciones.json')
    logger.info(log)

    registros_validos = 0
    registros_validos = 0
    registros_descartados = 0

    registros_leidos = int(len(df_alumnos)) + int(len(df_matriculas)) + int(len(df_calificaciones))

    df_alumnos.drop_duplicates(inplace=True)
    df_matriculas.drop_duplicates(inplace=True)
    df_calificaciones.drop_duplicates(inplace=True)

    registros_validos = int(len(df_alumnos)) + int(len(df_matriculas)) + int(len(df_calificaciones))

    indices_nan = df_alumnos[df_alumnos["correo"].isna()].index

    print(len(indices_nan))

    for i in indices_nan:
        nombre = ucode.unidecode(df_alumnos.loc[i, "nombre"].lower())
        apellido = ucode.unidecode(df_alumnos.loc[i, "apellido"].lower())
        correo_generado = nombre +'.'+ apellido + '@colegio.edu'

        df_alumnos.loc[i, "correo"] = correo_generado

    logger.info(f"Transformación - Creación de Correos Faltantes: {len(indices_nan)}")

    df_calificaciones["nota"] = df_calificaciones["nota"].clip(lower=0, upper=5)

    log = DataLoader.insert_data(conn, "alumnos", df_alumnos)
    logger.info(log)
    log = DataLoader.insert_data(conn, "calificaciones", df_calificaciones)
    logger.info(log)
    log = DataLoader.insert_data(conn, "matriculas", df_matriculas)
    logger.info(log)

    registros_descartados = registros_leidos - registros_validos

    monitor.set_metrics(leidos=registros_leidos, validos=registros_validos, descartados=registros_descartados)
    monitor.end()
    logger.info("Fin del proceso ETL Satisfactoriamente")

except Exception as e:
    logger.info(f"[ERROR] Error en la corrida ETL: {e}")