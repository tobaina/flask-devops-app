from app import app

def test_homepage():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Flask + SQLite app running via DevOps pipeline!" in response.data
