# run_etl.ps1

# 1. Activar el entorno conda
conda activate LabETL

# 2. Ir a la carpeta src
Set-Location -Path "$PSScriptRoot\src"

# 3. Ejecutar el script Python
python.exe main.py

# 4. Volver a la carpeta raíz del proyecto
Set-Location -Path $PSScriptRoot

# 5. Desactivar el entorno conda
conda deactivate
