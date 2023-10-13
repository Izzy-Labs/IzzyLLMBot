FROM python:3.11
WORKDIR telegram
COPY ../requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3", "run.py"]