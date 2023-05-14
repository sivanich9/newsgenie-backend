# Use a base image with Python 3.8 pre-installed
FROM bitnami/pytorch

USER root
RUN mkdir /.cache
RUN chmod 777 /.cache

# Set the working directory
WORKDIR /.cache

# Copy the Python files to the container
COPY summarizer_api.py ./
COPY database.py ./
COPY simplet5-epoch-4-train-loss-0.6005-val-loss-1.6554/ ./simplet5-epoch-4-train-loss-0.6005-val-loss-1.6554/

# Install the required packages
RUN pip install simplet5
RUN pip install "fastapi[all]"
RUN pip install uvicorn
RUN pip install loguru
RUN pip install pymongo


# Set the entrypoint command to run the summarizer.py script
#CMD ["python3", "-m", "uvicorn", "summarizer_api:app"]
CMD ["uvicorn", "summarizer_api:app","--host", "0.0.0.0", "--port", "8000"]
