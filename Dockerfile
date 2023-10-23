FROM python:3.9

WORKDIR /indu-c-q

COPY requirements.txt /indu-c-q/

ENV PATH  /indu-c-q:$PATH

RUN pip install --no-cache-dir -r requirements.txt

LABEL   name="quay.io/cristinag/indu-c-q" \
        description="Indu-C-Q package container for Gene Editing experiments" \
        version="1.0.0" \
        maintainer="Cristina Guijarro-Clarke"
