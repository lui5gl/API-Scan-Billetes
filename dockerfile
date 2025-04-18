FROM python:3.11.2

COPY . /ScanCashAPI

WORKDIR /ScanCashAPI

RUN python -m venv venv

RUN ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/python", "-u", "src/main.py"]
