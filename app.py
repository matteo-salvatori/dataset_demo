import streamlit as st
import pandas as pd
import os

# Datos de personajes (fuerza, inteligencia, altura, clase)
data = {
    "nombre": ["Superman", "Iron Man", "Spider-Man", "Hulk", "Thor", "Batman", "Wonder Woman", "Doctor Strange",
               "Captain America", "Black Panther",
               "Flash", "Green Lantern", "Aquaman", "Cyclops", "Deadpool",  # Héroes extra
               "Thanos", "Joker", "Lex Luthor", "Green Goblin", "Venom", "Ultron", "Loki", "Magneto", "Darkseid",
               "Red Skull",
               "Hela", "Reverse Flash", "Kingpin", "Doctor Doom", "Mystique"],  # Villanos extra
    "fuerza": [10, 7, 6, 10, 9, 5, 9, 4, 8, 7, 9, 6, 8, 5, 7,
               4, 3, 2, 4, 6, 5, 3, 5, 2, 3, 9, 4, 8, 6, 7],  # Algunos villanos fuertes y héroes débiles
    "inteligencia": [9, 10, 9, 5, 9, 10, 8, 10, 7, 9, 7, 6, 5, 7, 8,
                     6, 9, 10, 7, 3, 8, 10, 9, 5, 8, 2, 10, 3, 4, 9],  # Algunos héroes con baja inteligencia
    "altura": [191, 175, 178, 244, 198, 188, 183, 180, 188, 182, 180, 185, 190, 175, 177,
               201, 180, 183, 178, 190, 210, 191, 180, 260, 180, 170, 200, 210, 190, 175],  # Altura irrelevante
    "clase": ["heroe"] * 15 + ["villano"] * 15
}

# Crear DataFrame de los datos
df_personajes = pd.DataFrame(data)

# ---- 1. Inicializar y Obtener el Índice del Personaje ----
if "persona_idx" not in st.session_state:
    st.session_state.persona_idx = 0  # Inicializar el índice del primer personaje

# ---- 2. Selección del Personaje ----
persona_idx = st.session_state.persona_idx
personaje = df_personajes.iloc[persona_idx]

# Mostrar la selección del personaje
st.write(f"Has seleccionado: {personaje['nombre']} - {personaje['clase'].capitalize()}")

# ---- 3. Mostrar Foto del Personaje (opcional) ----
image_path = f"images/{personaje['nombre'].replace(' ', '_')}.jpeg"  # Asume que las imágenes están en una carpeta 'images' y se nombran según el personaje
if os.path.exists(image_path):
    st.image(image_path, caption=personaje["nombre"], use_container_width=True)
else:
    st.write("No se encontró imagen para este personaje.")

# ---- 4. Visualizar y Modificar Datos ----
# Valores propuestos para cada atributo
fuerza = st.number_input("Fuerza:", min_value=1, max_value=20, value=personaje["fuerza"])
inteligencia = st.number_input("Inteligencia:", min_value=1, max_value=20, value=personaje["inteligencia"])
altura = st.number_input("Altura (cm):", min_value=100, max_value=300, value=personaje["altura"])

# ---- 5. Botón para pasar al siguiente personaje ----
next_button = st.button("Siguiente personaje")
guardar_button = st.button("Guardar dataset")

# Agregar los datos del personaje al DataFrame
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["nombre", "fuerza", "inteligencia", "altura", "clase"])

# Añadir los datos del personaje al dataset
if next_button:
    # Guardar los datos del personaje en el DataFrame
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame({
        "nombre": [personaje["nombre"]],
        "fuerza": [fuerza],
        "inteligencia": [inteligencia],
        "altura": [altura],
        "clase": [personaje["clase"]]
    })], ignore_index=True)

    # Avanzar al siguiente personaje
    if persona_idx < len(df_personajes) - 1:
        st.session_state.persona_idx += 1
    else:
        st.session_state.persona_idx = 0  # Si hemos llegado al final, volvemos al principio
    st.rerun()

# ---- 6. Guardar Dataset en CSV ----
if guardar_button:
    # Pedir la ruta para guardar el archivo
    file_path = st.text_input("Introduce la ruta donde guardar el archivo CSV (incluye el nombre del archivo):",
                              value="dataset.csv")

    if file_path:
        try:
            st.session_state.df.to_csv(file_path, sep=";", index=False, header=True)
            st.write(f"¡Dataset guardado en {file_path}!")
        except Exception as e:
            st.write(f"Error al guardar el archivo: {e}")

# ---- 7. Mostrar el dataset en progreso ----
st.write("Dataset en progreso:")
st.dataframe(st.session_state.df)
