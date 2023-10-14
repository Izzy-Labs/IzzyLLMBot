FROM python:3.10
WORKDIR telegram
COPY telegram/requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3", "run.py"]