FROM python:3.12-alpine

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV VERSION=20240916205000


WORKDIR /app
COPY requirements.txt ./
COPY --chmod=777 *.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "/usr/local/bin/python", "/app/feed.py" ]
