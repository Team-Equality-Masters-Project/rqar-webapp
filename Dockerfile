FROM python:3.8.2-slim-buster

# virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

WORKDIR /app

COPY ./app /app

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install streamlit

EXPOSE 8501
 
# cmd to launch app when container is run
ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]


