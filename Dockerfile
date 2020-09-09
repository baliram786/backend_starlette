FROM tiangolo/uvicorn-gunicorn:python3.8
RUN echo "Installing python packages.. "
COPY ./app /app
WORKDIR /app 
RUN pip install -r requirements.txt
