FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev vim curl

RUN pip3 install --upgrade pip

COPY ./app /app
COPY requirements.txt /tmp/

WORKDIR /app

RUN pip3 install -r /tmp/requirements.txt -t /app
RUN pip3 install gevent -t /app --upgrade

# Expose port 
ENV PORT 8501

# cmd to launch app when container is run
CMD streamlit run app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

