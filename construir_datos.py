import csv

# 1. USUARIOS MAESTROS (DNA de tus archivos anteriores)
usuarios = [
    # username, email, rol, dni, en_mora, es_becado, %_beca, carrera
    ['admin_gral', 'admin@infocampus.com', 'director', '101010', 'False', 'False', '0', 'Ingenieria Sistemas'],
    ['profe_carlos', 'carlos@infocampus.com', 'profesor', '404040', 'False', 'False', '0', 'Ingenieria Sistemas'],
    ['ana_elite', 'ana@estudiante.com', 'estudiante', '111111', 'False', 'True', '100', 'Ingenieria Sistemas'], # Becada
    ['pedro_mora', 'pedro@estudiante.com', 'estudiante', '222222', 'True', 'False', '0', 'Derecho'], # Mora
    ['luis_regular', 'luis@estudiante.com', 'estudiante', '333333', 'False', 'False', '0', 'Medicina'],
]

# 2. MALLA DE ALTO NIVEL (350 materias)
carreras = ["Ingenieria Sistemas", "Derecho", "Medicina", "Psicologia", "Administracion"]
malla = []
for c in carreras:
    pref = c[:3].upper()
    for sem in range(1, 11):
        for m in range(1, 8):
            codigo = f"{pref}-{sem}{m}"
            prereq = f"{pref}-{sem-1}{m}" if sem > 1 else "" # Lógica de prerrequisito
            malla.append([c, sem, f"Materia {sem}.{m} de {c}", codigo, prereq])

# Escribir archivos
with open('csv_usuarios.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['username', 'email', 'rol', 'dni', 'en_mora', 'es_becado', 'beca', 'carrera'])
    writer.writerows(usuarios)

with open('csv_malla.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['carrera', 'semestre', 'nombre', 'codigo', 'prerrequisito'])
    writer.writerows(malla)

print("✅ Archivos CSV generados. Estructura de alto nivel lista.")