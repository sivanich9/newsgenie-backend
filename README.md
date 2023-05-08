# Steps to run the Backend API in prod environment
uvicorn -m summarizer_api:app

# Steps to run the Backend API in dev environment
uvicorn -m summarizer_api:app --reload

# Steps to test the application
pytest test_main.py -W ignore::DeprecationWarning