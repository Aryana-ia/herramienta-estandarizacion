import streamlit as st
import pandas as pd
from nltk.tokenize import word_tokenize
import nltk
import difflib
nltk.download('punkt', quiet=True)

# Función para detectar y extraer cambios (reemplazos, inserciones, eliminaciones)
def get_changes(original, modified):
    orig_tokens = word_tokenize(original.lower())
    mod_tokens = word_tokenize(modified.lower())
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

# Carga inicial del Excel (fuerza id como string)
@st.cache_data
def load_data():
    return pd.read_excel('descripciones.xlsx', dtype={'id': str})

# Guarda el DataFrame actualizado en Excel
def save_data(df):
    df.to_excel('descripciones.xlsx', index=False)

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
                    df.at[idx, 'descripcion_modificada'] = updated_desc
        else:
            st.warning("No se detectaron cambios. Aplicando solo a esta fila.")
        
        # Actualiza la fila editada
        df.at[row_index, 'descripcion_modificada'] = new_description
        
        # Guarda cambios
        save_data(df)
        st.success("Cambios guardados. Recarga la página para ver actualizaciones.")
        
        # Muestra preview de cambios
        st.write("Vista previa de filas afectadas (solo primeras 5):")
        affected = df[df.index != row_index] if changes else df.iloc[[row_index]]
        st.dataframe(affected[['id', 'descripcion_original', 'descripcion_modificada']].head(5))

if __name__ == "__main__":
    main()