import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="simahasiswa",
        user="postgres",
        password="postgres123"
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id SERIAL PRIMARY KEY,
            nim VARCHAR(20) UNIQUE NOT NULL,
            nama VARCHAR(100) NOT NULL,
            jurusan VARCHAR(100),
            password VARCHAR(100) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            nama VARCHAR(100),
            pesan TEXT
        )
    """)
    # Data dummy
    cur.execute("SELECT COUNT(*) FROM mahasiswa")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO mahasiswa (nim, nama, jurusan, password) VALUES
            ('32230178', 'Valwa Giraldy', 'Teknik Informatika', 'admin123'),
            ('32230099', 'Budi Santoso', 'Sistem Informasi', 'budi123'),
            ('32230050', 'Siti Aminah', 'Teknik Informatika', 'siti123')
        """)
    conn.commit()
    cur.close()
    conn.close()