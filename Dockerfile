FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python db_init.py || true
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
