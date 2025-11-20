# Herramienta de Estandarización de Descripciones

Esta herramienta permite estandarizar descripciones de productos de manera interactiva usando Streamlit. Permite editar una descripción y propagar automáticamente cualquier cambio (reemplazos, inserciones, eliminaciones, movimientos de palabras) a otras descripciones similares que contengan las frases afectadas.

## Características
- Carga de datos desde un archivo Excel (.xlsx).
- Edición interactiva de descripciones.
- Detección automática de cambios usando `difflib` para identificar frases cambiadas.
- Propagación de cambios solo a descripciones con similitud > 70% (para evitar corrupciones).
- Respeta IDs con ceros iniciales (tratados como strings).
- Seguimiento de modificaciones: columna para indicar si fue modificada y cuántas veces.
- Descarga del archivo Excel actualizado con cambios aplicados.
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
- `descripciones.xlsx`: Archivo de ejemplo con datos ficticios (crea uno en Excel con las columnas indicadas).
- `requirements.txt`: Dependencias necesarias.
- `README.md`: Este archivo.

## Notas
- Para archivos grandes (20,000 filas), considera usar una base de datos en lugar de Excel.
- La propagación se basa en similitud y coincidencias exactas de frases; ajusta el umbral si es necesario.
- Los cambios se aplican en memoria; descarga el Excel para guardar permanentemente.