FROM python:3.9.2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY setup.py /code/
COPY README.md /code/
# TODO: Remove README.md?
RUN python setup.py develop
COPY . /code/