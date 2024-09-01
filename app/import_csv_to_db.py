import csv
import sqlite3

def import_csv_to_db(csv_file_path, db_file_path):
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Leer el archivo CSV
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cursor.execute('''
                INSERT INTO incident (project, description, position, responsible, status, created_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Proyecto'],
                row['Descripción'],
                row['Posición'],
                row['Responsable'],
                row['Estado'],
                row['Creado por'],
                row['Fecha de Creación']
            ))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    import_csv_to_db('uploads/incidents.csv', 'app/instance/db.sqlite')
