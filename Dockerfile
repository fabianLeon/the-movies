FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y curl

RUN curl https://bootstrap.pypa.io/get-pip.py | python - pip==23.1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY credits.csv.zip .
COPY keywords.csv.zip .
COPY movies_metadata.csv.zip .

COPY init.py .
RUN python init.py

COPY model.py .
RUN python model.py

COPY movies_all_data.csv .
COPY similarity_matrix.csv .
COPY app.py .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]