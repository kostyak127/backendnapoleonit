FROM python:3
EXPOSE 8000
RUN git clone https://github.com/kostyak127/backendnapoleonit.git
RUN pip install --no-cache-dir -r backendnapoleonit/requirements.txt