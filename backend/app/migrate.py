from app.core.db import execute_query


def create_tables():
    """Crea las tablas necesarias para la aplicación"""
    
    # Crear tabla claims
    claims_table = """
    CREATE TABLE IF NOT EXISTS claims (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'IN_REVIEW', 'FINALIZED', 'CANCELED'))
    );
    """
    
    # Crear tabla damages
    damages_table = """
    CREATE TABLE IF NOT EXISTS damages (
        id SERIAL PRIMARY KEY,
        piece VARCHAR(255) NOT NULL,
        severity VARCHAR(10) NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH')),
        image_url VARCHAR(500) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10),
        claim_id INTEGER NOT NULL REFERENCES claims(id) ON DELETE CASCADE
    );
    """
    
    execute_query(claims_table)
    execute_query(damages_table)
    print("Tablas creadas exitosamente")


if __name__ == "__main__":
    create_tables()