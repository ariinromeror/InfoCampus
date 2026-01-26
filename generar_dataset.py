import csv

def generar_csv():
    usuarios = [
        # --- STAFF (Poderes Administrativos) ---
        ['admin_gral', 'admin@infocampus.com', 'director', '101010', 'False', 'False', '0', 'Ingeniería'],
        ['coord_acad', 'coord@infocampus.com', 'coordinador', '202020', 'False', 'False', '0', 'Derecho'],
        ['juan_tesorero', 'pagos@infocampus.com', 'tesorero', '303030', 'False', 'False', '0', 'Administración'],
        
        # --- PROFESORES ---
        ['profe_garcia', 'garcia@infocampus.com', 'profesor', '404040', 'False', 'False', '0', 'Ingeniería'],
        ['profe_martinez', 'martinez@infocampus.com', 'profesor', '505050', 'False', 'False', '0', 'Psicología'],

        # --- ESTUDIANTES: CASOS DE PRUEBA (Golden Cases) ---
        ['ana_elite', 'ana@estudiante.com', 'estudiante', '111111', 'False', 'True', '100', 'Ingeniería'], # BECADA 100%
        ['pedro_mora', 'pedro@estudiante.com', 'estudiante', '222222', 'True', 'False', '0', 'Ingeniería'],  # EN MORA (BLOQUEADO)
        ['luis_regular', 'luis@estudiante.com', 'estudiante', '333333', 'False', 'False', '0', 'Derecho'],   # SOLVENTE
        ['maria_beca50', 'maria@estudiante.com', 'estudiante', '444444', 'False', 'True', '50', 'Psicología'], # BECA PARCIAL
        ['carla_deudora', 'carla@estudiante.com', 'estudiante', '555555', 'True', 'False', '0', 'Administración'], # MORA
        ['jose_alumni', 'jose@egresado.com', 'estudiante', '666666', 'False', 'False', '0', 'Diseño'], # CASO HISTÓRICO
    ]

    headers = ['username', 'email', 'rol', 'dni', 'en_mora', 'es_becado', 'porcentaje_beca', 'carrera']

    with open('usuarios_maestros.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(usuarios)

    print("✅ CSV 'usuarios_maestros.csv' generado con éxito con 11 casos maestros.")

if __name__ == "__main__":
    generar_csv()