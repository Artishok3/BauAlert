FROM python:latest

WORKDIR /BauAlert

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
