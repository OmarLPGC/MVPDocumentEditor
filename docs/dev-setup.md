# Desarrollo: configuración del entorno

Requisitos locales
- Python 3.10+
- pip

Recomendado: crear un entorno virtual y usar el fichero requirements.txt

Pasos rápidos (Windows PowerShell):

1. Crear y activar entorno virtual
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Actualizar pip e instalar dependencias
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r dev-requirements.txt

3. Ejecutar tests
   pytest

4. Ejecutar la aplicación
   python -m editor

En entornos sin servidor gráfico, como CI, ejecutar los tests GUI en modo
offscreen:

   $env:QT_QPA_PLATFORM = "offscreen"
   pytest

Formato de código
- Formatear con black:
  black src tests
- Ordenar imports:
  isort src tests
- Comprobar lint:
  flake8 src tests

CI
La pipeline `.github/workflows/ci.yml` instalará dependencias y ejecutará `pytest` en push y PRs contra main/master.
