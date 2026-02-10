import pytest
from unittest.mock import patch, call
from app.migrate import create_tables


def test_create_tables(capsys):
    """Test create_tables creates both claims and damages tables"""
    with patch('app.migrate.execute_query') as mock_execute:
        create_tables()
        
        # Verify execute_query was called twice (claims + damages)
        assert mock_execute.call_count == 2
        
        # Verify claims table creation
        claims_call = mock_execute.call_args_list[0][0][0]
        assert "CREATE TABLE IF NOT EXISTS claims" in claims_call
        assert "id SERIAL PRIMARY KEY" in claims_call
        assert "title VARCHAR(255) NOT NULL" in claims_call
        assert "status VARCHAR(20)" in claims_call
        
        # Verify damages table creation
        damages_call = mock_execute.call_args_list[1][0][0]
        assert "CREATE TABLE IF NOT EXISTS damages" in damages_call
        assert "id SERIAL PRIMARY KEY" in damages_call
        assert "piece VARCHAR(255) NOT NULL" in damages_call
        assert "severity VARCHAR(10) NOT NULL" in damages_call
        assert "claim_id INTEGER NOT NULL REFERENCES claims(id)" in damages_call
        
        # Verify success message
        captured = capsys.readouterr()
        assert "Tablas creadas exitosamente" in captured.out
