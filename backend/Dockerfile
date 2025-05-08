FROM python:3.11
COPY requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y openjdk-17-jre && \
    apt-get clean && \
    update-ca-certificates -f \
COPY . /app
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ,"--reload"]