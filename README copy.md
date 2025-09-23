# 📌 Proyecto ETL lABORATORIO 2

Este proyecto implementa un **proceso ETL (Extract, Transform, Load)** en Python para manejar información de estudiantes, matrículas y calificaciones.  
El flujo carga datos desde archivos CSV, XML y JSON, los transforma y los almacena en una base de datos SQLite, mientras registra logs y métricas de ejecución.

---

## 🚀 Arquitectura del Proyecto

- **`main.py`** → Orquestador del proceso ETL.  
- **`extract.py`** → Contiene la clase `DataExtractor` con métodos para leer CSV, JSON y XML.  
- **`load.py`** → Contiene la clase `DataLoader` para crear tablas, inicializar la BD e insertar datos.  
- **`logger.py`** → Define `LoggerETL` para gestionar logs e integrar errores con el monitor.  
- **`monitor.py`** → Define `MonitorETL` para registrar métricas de cada corrida en la tabla `etl_monitor`.  
- **`..\data\`** → Carpeta que contiene la BD `lab2.db` y los archivos de entrada (`alumnos.csv`, `matriculas.xml`, `calificaciones.json`).  

---

## 📂 Tablas Principales en SQLite

- **`etl_monitor`** → Almacena métricas de ejecución del ETL (tiempo, registros leídos/validados, errores).  
- **`alumnos`** → Información de los estudiantes.  
- **`calificaciones`** → Notas de los estudiantes, vinculadas a `alumnos`.  
- **`matriculas`** → Información de matrículas de estudiantes.  

---

## 🛠️ Requisitos

- Python **3.10+**  
- Librerías:  

```bash
pip install pandas lxml unidecode
```

> SQLite está incluido en Python, no requiere instalación adicional.

---

## ⚙️ Ejecución del Proceso ETL

1. Coloca los archivos de datos en la carpeta `..\data\`:
   - `alumnos.csv`
   - `matriculas.xml`
   - `calificaciones.json`

2. Ejecuta el proceso:

```bash
python main.py
```

3. Durante la corrida verás mensajes en consola y en el archivo `etl.log`.

---

## 📝 Flujo del Proceso

1. **Inicio**  
   - Se inicializa la BD `lab2.db`.  
   - Se crean las tablas si no existen.  

2. **Extracción**  
   - Se cargan los datos desde CSV, JSON y XML.  

3. **Transformación**  
   - Eliminación de duplicados.  
   - Normalización de correos faltantes para alumnos.  
   - Restricción de notas entre 0 y 5.  

4. **Carga**  
   - Inserción de los datos transformados en SQLite.  

5. **Monitoreo y Logging**  
   - `LoggerETL` registra información y errores en `etl.log` y consola.  
   - `MonitorETL` guarda métricas en la tabla `etl_monitor`.  

---

## 📊 Monitoreo

Cada corrida queda registrada en la tabla **`etl_monitor`** con la siguiente información:

- Fecha de ejecución  
- Registros leídos, válidos y descartados  
- Duración (segundos)  
- Error (si ocurrió alguno)  

Puedes consultar los logs con:

```sql
SELECT * FROM etl_monitor;
```

---

## ✅ Ejemplo de Log en Consola

```
[INFO] Inicio del proceso ETL
[INFO] La BD ya existe: ..\data\lab2.db
[INFO] Tabla 'alumnos' creada correctamente
[INFO] CSV cargado correctamente: alumnos.csv
[INFO] Transformación - Creación de Correos Faltantes: 3
[INFO] 100 registros insertados en tabla 'alumnos'
===== Resumen corrida ETL =====
Registros leídos:      250
Registros válidos:     247
Registros descartados: 3
Duración (segundos):   1.85
```