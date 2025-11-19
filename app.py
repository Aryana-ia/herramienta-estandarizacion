import streamlit as st
import pandas as pd
import difflib
from io import BytesIO

# Función para detectar y extraer cambios (reemplazos, inserciones, eliminaciones)
def get_changes(original, modified):
    orig_tokens = original.lower().split()
    mod_tokens = modified.lower().split()
    matcher = difflib.SequenceMatcher(None, orig_tokens, mod_tokens)
    changes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            old_phrase = ' '.join(orig_tokens[i1:i2])
            new_phrase = ' '.join(mod_tokens[j1:j2])
            changes.append(('replace', old_phrase, new_phrase))
        elif tag == 'delete':
            old_phrase = ' '.join(orig_tokens[i1:i2])
            changes.append(('delete', old_phrase, ''))
        elif tag == 'insert':
            new_phrase = ' '.join(mod_tokens[j1:j2])
            changes.append(('insert', '', new_phrase))  # Nota: inserción requiere contexto, se aplica al final o inicio aproximado
    return changes

# Función para aplicar cambios a otra descripción
def apply_changes(desc, changes):
    desc_lower = desc.lower()
    updated_desc = desc
    for change_type, old_phrase, new_phrase in changes:
        if change_type == 'replace' and old_phrase in desc_lower:
            # Reemplaza la primera ocurrencia
            updated_desc = updated_desc.replace(old_phrase, new_phrase, 1)
        elif change_type == 'delete' and old_phrase in desc_lower:
            updated_desc = updated_desc.replace(old_phrase, '', 1)
        elif change_type == 'insert':
            # Inserta al final (aproximación simple; en producción, podría necesitar lógica de posición)
            updated_desc += ' ' + new_phrase
    return updated_desc.strip()

# Carga inicial del Excel (fuerza id como string, agrega columnas de seguimiento si no existen)
@st.cache_data
def load_data():
    df = pd.read_excel('descripciones.xlsx', dtype={'id': str})
    # Agrega columnas de seguimiento si no existen
    if 'modificado' not in df.columns:
        df['modificado'] = False
    if 'veces_modificado' not in df.columns:
        df['veces_modificado'] = 0
    return df

# Guarda el DataFrame actualizado en Excel
def save_data(df):
    df.to_excel('descripciones.xlsx', index=False)

# Función para crear un buffer de Excel para descarga
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

# Función principal
def main():
    st.title("Herramienta de Estandarización de Descripciones (con Propagación de Cualquier Cambio)")
    st.write("Edita una descripción; cualquier cambio (posición, contenido, etc.) se aplicará automáticamente a otras descripciones que contengan las frases afectadas.")
    
    # Carga datos
    df = load_data()
    total = len(df)
    
    # Selector de fila a editar
    row_index = st.selectbox("Selecciona la fila a editar:", range(total), format_func=lambda x: f"Fila {x+1}: {df.iloc[x]['descripcion_original'][:50]}...")
    
    # Muestra la fila actual
    current_row = df.iloc[row_index]
    st.write(f"**ID:** {current_row['id']}")
    st.write(f"**Tienda:** {current_row['tienda']}")
    st.write(f"**Descripción Original:** {current_row['descripcion_original']}")
    st.write(f"**Descripción Modificada Actual:** {current_row['descripcion_modificada']}")
    st.write(f"**Modificado:** {current_row['modificado']}")
    st.write(f"**Veces Modificado:** {current_row['veces_modificado']}")
    
    # Campo de edición
    new_description = st.text_area("Edita la descripción modificada:", value=current_row['descripcion_modificada'])
    
    if st.button("Aplicar Cambio"):
        original_desc = current_row['descripcion_modificada']
        
        # Detecta cambios
        changes = get_changes(original_desc, new_description)
        if changes:
            st.info(f"Cambios detectados: {changes}. Aplicando a descripciones que contengan las frases.")
            
            # Aplica a todas las filas (excepto la actual)
            for idx in df.index:
                if idx != row_index:
                    desc = df.at[idx, 'descripcion_modificada']
                    updated_desc = apply_changes(desc, changes)
                    if updated_desc != desc:  # Si cambió, marca como modificado
                        df.at[idx, 'descripcion_modificada'] = updated_desc
                        df.at[idx, 'modificado'] = True
                        df.at[idx, 'veces_modificado'] += 1
        else:
            st.warning("No se detectaron cambios. Aplicando solo a esta fila.")
        
        # Actualiza la fila editada
        if new_description != original_desc:
            df.at[row_index, 'descripcion_modificada'] = new_description
            df.at[row_index, 'modificado'] = True
            df.at[row_index, 'veces_modificado'] += 1
        
        # Guarda cambios
        save_data(df)
        st.success("Cambios guardados. Recarga la página para ver actualizaciones.")
        
        # Muestra preview de cambios
        st.write("Vista previa de filas afectadas (solo primeras 5):")
        affected = df[df.index != row_index] if changes else df.iloc[[row_index]]
        st.dataframe(affected[['id', 'descripcion_original', 'descripcion_modificada', 'modificado', 'veces_modificado']].head(5))

    # Botón de descarga del Excel actualizado
    st.write("---")
    st.write("Descarga el archivo Excel con todos los cambios aplicados:")
    excel_data = to_excel(df)
    st.download_button(
        label="Descargar Excel Actualizado",
        data=excel_data,
        file_name="descripciones_actualizado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()