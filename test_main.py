from fastapi.testclient import TestClient
from summarizer_api import app
from bson.objectid import ObjectId


import pytest
import mongomock
import json
import datetime


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
    comments = db.get_collection("comments")
    visits = db.get_collection("visits")

    article_data = {
        "_id": ObjectId("5e63c3a5e4232e4cd0274ac2"),
        "user": {"id": "u1", "email": "hanzoapi1@gmail.com"},
        "headline": "test_headline",
        "description": "test_desc",
        "genre": "test",
        "rating": 0,
    }
    articles.insert_one(article_data)


    comments_data = {
        "_id": ObjectId("5e63c3a5e4132eccd02d4ae2"),
        "user": {"id": "u1", "email": "hanzoapi1@gmail.com"},
        "comment": "test_comment",
        "article_id": "5e63c3a5e4232e4cd0274ac2",
        "created_at": str(datetime.datetime.now()),
    }
    comments.insert_one(comments_data)


    visits_data = {
        "_id": ObjectId("5e63c3a5e4132eccd02d4345"),
        "user": {"id": "u1", "email": "hanzoapi1@gmail.com"},
        "article": {
            "newsArticle": {
                "_id": "5e63c3a5e4232e4cd0274ac2",
                "user": {"id": "u1", "email": "hanzoapi1@gmail.com"},
                "headline": "test_headline",
                "description": "test_desc",
                "genre": "test",
                "rating": 0,
            }
        },
        "created_at": str(datetime.datetime.now()),
    }
    visits.insert_one(visits_data)


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
    "user": {"id": "u2", "email": "sivani@gmail.com"},
    "headline": "sivani_headline",
    "description": "sivani_desc",
    "genre": "test",
    "rating": 0,
}


comment_data = {
    "user": {"id": "u2", "email": "sivani@gmail.com"},
    "comment": "sivani_comment",
    "article_id": "5e63c3a5e4132eccd02d4ae2",
    "created_at": str(datetime.datetime.now()),
}


visit_data = {
    "user": {"id": "u2", "email": "sivani@gmail.com"},
    "article": {
        "newsArticle": {
            "_id": "5e63c3a5e4232e4cd0274ac2",
            "user": {"id": "u1", "email": "hanzoapi1@gmail.com"},
            "headline": "test_headline",
            "description": "test_desc",
            "genre": "test",
            "rating": 0,
        }
    },
    "created_at": str(datetime.datetime.now()),
}


summary_article = {
    "newsArticle": """Due to the superhero fatigue, I have to admit that my excitement towards the film Guardians of the Galaxy Vol. 3 was very minimal. 
    But surprisingly enough, this was perhaps the most entertaining MCU film after No Way Home. With James Gunn retaining his quirkiness in the narrative in a pretty balanced screenplay, 
    this final volume was a fun watch that had almost all the elements you expect in a Marvel film. One day the guardians are attacked by Adam, son of Sovereign Empress Ayesha, 
    and Rocket gets badly injured in that attack. When they tried to save Rocket, they found out that there was a kill switch embedded in Rocket's body, and they needed to bypass it first to save him. 
    The journey of the guardians to save their friend is what we see in Guardians of the Galaxy Vol. 3. While Vol. 1 had a totally different texture from other MCU films and was extremely funny, 
    Vol. 2 didn't really work for me as it was burdened with a sentimental angle of Peter Quill, aka Star-Lord. What was satisfying about Vol. 3 is that this one balances both aspects. 
    You get a really deep and emotional story about the origin of Rocket, and Gunn uses the rest of the characters to maintain the signature humor. Even though it has that “insensitive” tone in the way it presents the humor, 
    James Gunn knows that the team's camaraderie has a fan following. The final moments that focus on that teamwork created those whistle-worthy theater moments.
    In the role of Peter Quill, Chris Pratt continues to be in that funny zone, and the banter comedy between him and the other folks still works. Karen Gillian's Nebula has more empathetic behavior this time, 
    and Zoe Saldana as Gamora is all the more ruthless and impulsive in this version. As Drax, Dave Bautista is funny as always, and this time Gunn makes Drax a lot more adorable, 
    contrary to his title of Destroyer. Pom Klementieff was also hilarious in the way she said her lines. Chukwudi Iwuji, as the antagonist High Evolutionary, 
    is similar to Thanos in terms of ideology (Gunn even acknowledges that through dialogue by Quill), but a lot louder. Sean Gunn, as Kraglin, also gets a prominent screen time this time. 
    The character is seen handling a crucial moment in the final phase of the film."""
}




def test_create_article(mongo_mock):
    response = client.post("/create_article", data=json.dumps(article_data))
    assert response.status_code == 201
    assert response.json()["insertion"] == True




def test_get_article(mongo_mock):
    response = client.post(
        "/get_article", data=json.dumps({"id": "5e63c3a5e4232e4cd0274ac2"})
    )
    assert response.status_code == 201
    print(response.json())
    article = response.json()["article"]
    assert article["user"]["id"] == "u1"
    assert article["user"]["email"] == "hanzoapi1@gmail.com"
    assert article["headline"] == "test_headline"
    assert article["description"] == "test_desc"
    assert article["genre"] == "test"



def test_get_comments(mongo_mock):
    response = client.post(
        "/get_comments", data=json.dumps({"id": "5e63c3a5e4232e4cd0274ac2"})
    )
    assert response.status_code == 202
    comments = response.json()["comments"]
    assert comments[0]["user"]["id"] == "u1"
    assert comments[0]["user"]["email"] == "hanzoapi1@gmail.com"
    assert comments[0]["comment"] == "test_comment"



def test_create_comment(mongo_mock):
    response = client.post("/create_comment", data=json.dumps(comment_data))
    assert response.status_code == 201
    assert response.json()["insertion"] == True



def test_get_history(mongo_mock):
    response = client.post("/get_visits", data=json.dumps({"userId": "u1"}))
    assert response.status_code == 202
    visits = response.json()["visits"]
    assert visits[0]["user"]["id"] == "u1"
    assert visits[0]["user"]["email"] == "hanzoapi1@gmail.com"
    assert visits[0]["article"]["newsArticle"]["_id"] == "5e63c3a5e4232e4cd0274ac2"



def test_add_history(mongo_mock):
    response = client.post("/post_visit", data=json.dumps(visit_data))
    assert response.status_code == 201
    assert response.json()["insertion"] == True



def test_summarization(mongo_mock):
    response = client.post(
        "/summary",
        data=json.dumps(summary_article),
    )
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()[0]) < len(summary_article["newsArticle"])
