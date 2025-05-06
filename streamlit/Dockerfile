FROM python:3.12

COPY requirements.txt app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y openjdk-17-jre && \
    apt-get clean && \
    update-ca-certificates -f
COPY . /app

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["app.py"]