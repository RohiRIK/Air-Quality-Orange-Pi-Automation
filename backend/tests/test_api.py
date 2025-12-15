def test_history_endpoint(client):
    response = client.get("/api/history")
    # It might return 503 if sensor not initialized, or 200 with empty list
    # The sensor init is in background thread. In tests, it might not run or might fail (no hardware).
    # But the endpoint should exist.
    assert response.status_code in [200, 503]
