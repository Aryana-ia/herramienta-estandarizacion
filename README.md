# Herramienta de Estandarización de Descripciones

Esta herramienta permite estandarizar descripciones de productos de manera interactiva usando Streamlit. Permite editar una descripción y propagar automáticamente cualquier cambio (reemplazos, inserciones, eliminaciones, movimientos de palabras) a otras descripciones que contengan las frases afectadas.

## Características
- Carga de datos desde un archivo CSV o Excel.
- Edición interactiva de descripciones.
- Detección automática de cambios usando `difflib` y `nltk`.
- Propagación de cambios a filas que contengan frases similares.
- Respeta IDs con ceros iniciales (tratados como strings).
- Vista previa de cambios aplicados.

## Instalación y Ejecución Local
1. Clona o descarga este repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta la app: `streamlit run app.py`
4. Abre el navegador en la URL indicada (generalmente http://localhost:8501).

## Despliegue en Streamlit Community Cloud
1. Sube este repositorio a GitHub (asegúrate de que sea público).
2. Ve a [share.streamlit.io](https://share.streamlit.io).
3. Conecta tu cuenta de GitHub, selecciona este repo y el archivo `app.py`.
4. Haz clic en "Deploy" y sigue las instrucciones.
5. La app estará disponible en una URL pública.

## Estructura de Archivos
- `app.py`: Código principal de la aplicación Streamlit.
- `descripciones.csv`: Archivo de ejemplo con datos ficticios.
- `requirements.txt`: Dependencias necesarias.
- `README.md`: Este archivo.

## Notas
- Para archivos grandes (20,000 filas), considera usar una base de datos en lugar de CSV/Excel.
- La propagación se basa en coincidencias exactas de frases; para similitudes avanzadas, se puede mejorar con bibliotecas como `fuzzywuzzy`.