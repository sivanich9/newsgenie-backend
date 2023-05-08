from fastapi.testclient import TestClient
from summarizer_api import app

import pytest
import mongomock


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}



@pytest.fixture()
def mongo_mock(monkeypatch):
    client = mongomock.MongoClient()
    db = client.get_database("newsgenieTest")
    articles = db.get_collection("articles")
    article_data = {
        "user": {
            "id": "u1",
            "email": "hanzoapi1@gmail.com"
        },
        "headline": "test_headline",
        "description": "test_desc",
        "genre": "test",
        "rating": 0
    }
    articles.insert_one(article_data)

    def fake_db(dbName):
        return db
    
    monkeypatch.setattr("summarizer_api.get_db", fake_db)



def test_get_articles(mongo_mock):
    response = client.get("/get_articles")
    print(response.json())
    assert response.status_code == 202
    assert response.json()[0]["user"]["id"] == "u1"
    assert response.json()[0]["user"]["email"] == "hanzoapi1@gmail.com"
    assert response.json()[0]["headline"] == "test_headline"
    assert response.json()[0]["description"] == "test_desc"
    assert response.json()[0]["genre"] == "test"