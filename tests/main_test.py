from starlette.testclient import TestClient
from app.main import app

# client = TestClient(app)


# TODO: Delete this integration test then add integration that
# follows this format.
def test_test_api():
    with TestClient(app) as client:
        response = client.get('/test')
        assert response.status_code == 200
        assert len(response.json()) > 0
