FROM python
WORKDIR app
COPY .. .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT uvicorn main:app --port 8000 --host 0.0.0.0 --workers 2
