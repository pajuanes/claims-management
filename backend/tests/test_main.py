import pytest
from unittest.mock import AsyncMock, patch
from app.main import lifespan, app


@pytest.mark.asyncio
async def test_lifespan_startup_shutdown():
    """Test lifespan context manager calls connect and close"""
    with patch('app.main.connect_to_mongo', new_callable=AsyncMock) as mock_connect, \
         patch('app.main.close_mongo_connection', new_callable=AsyncMock) as mock_close:
        
        async with lifespan(app):
            # Verify startup was called
            mock_connect.assert_called_once()
            # Verify shutdown not called yet
            mock_close.assert_not_called()
        
        # Verify shutdown was called after context exit
        mock_close.assert_called_once()
