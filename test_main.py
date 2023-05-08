from fastapi.testclient import TestClient
from summarizer_api import app
from bson.objectid import ObjectId

import pytest
import mongomock
import json


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
        "_id": ObjectId("5e63c3a5e4232e4cd0274ac2"),
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


article_data = {
        "user": {
            "id": "u2",
            "email": "sivani@gmail.com"
        },
        "headline": "sivani_headline",
        "description": "sivani_desc",
        "genre": "test",
        "rating": 0
    }


def test_create_article(mongo_mock):
    response = client.post("/create_article", data=json.dumps(article_data))
    assert response.status_code == 201
    assert response.json()["insertion"] == True  


def test_get_article(mongo_mock):
    response = client.post("/get_article", data=json.dumps({"id":"5e63c3a5e4232e4cd0274ac2"}))
    assert response.status_code == 201
    print(response.json())
    article = response.json()["article"]
    assert article["user"]["id"] == "u1"
    assert article["user"]["email"] == "hanzoapi1@gmail.com"
    assert article["headline"] == "test_headline"
    assert article["description"] == "test_desc"
    assert article["genre"] == "test"