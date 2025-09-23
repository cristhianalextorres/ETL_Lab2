# Solución ETL Académica

Este proyecto implementa una **solución ETL** en Python con SQLite para la gestión de datos académicos (alumnos, matrículas y calificaciones), con monitoreo y logging de cada corrida.

---

## Estructura del Proyecto

Lo primero que encontrarás:

- **EjecucionETL.ps1** → Script PowerShell para ejecutar el ETL completo.  
- **environment.yaml** → Archivo para recrear el entorno `conda`.  
- **Carpetas**:
  - **data** → Contiene `lab2.db` y los archivos de carga (`alumnos.csv`, `matriculas.csv`, `calificaciones.csv`).
  - **logs** → Registro de ejecuciones (`etl.log`).
  - **src** → Código fuente:
    - `main.py` (script principal de la ETL).
    - `extract.py` (extracción de datos).
    - `load.py` (carga a la base de datos).
    - `logger.py` (logging de la corrida).
    - `monitor.py` (monitoreo y métricas ETL).

---

## Funcionamiento

1. **Ejecución**:  
   Se lanza con `EjecucionETL.ps1`, que activa el entorno, ejecuta el ETL y cierra el entorno.  

2. **Proceso ETL**:  
   - **Extract** → Lee los CSV de la carpeta `data`.  
   - **Load** → Crea tablas (si no existen) y carga los datos en `lab2.db`.  
   - **Logger** → Registra eventos e información en `logs/etl.log`.  
   - **Monitor** → Guarda métricas de ejecución en la tabla `etl_monitor`.  

---

## Arquitectura

- **Python + SQLite** como motor principal.  
- **Logging centralizado** en archivo y consola.  
- **Monitoreo de métricas** en base de datos (tiempo, registros leídos, válidos, descartados, errores).  
- **Ejecución automatizada** vía PowerShell y compatible con Task Scheduler.  

---

## Requisitos

- Conda/Miniconda instalado.  
- Crear el entorno:  
  ```bash
  conda env create -f environment.yaml
  conda activate LabETL
