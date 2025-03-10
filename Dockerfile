FROM python:3.10

ADD requirements.txt .
ADD scraper.py .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["python", "./scraper.py"]