FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

RUN groupadd -g 1000 app && \
    useradd -u 1000 -g app -s /bin/bash -m app && \
    chown -R app:app /app

USER app

# TODO: Update module path for your project
ENTRYPOINT ["python", "-m", "my_app.main"]
