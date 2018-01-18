FROM python:3.5

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
RUN find /app -regex "\(.*__pycache__.*\|*.py[co]\)" -delete
WORKDIR /app/crawler
CMD ["python", "get_diameter.py"]