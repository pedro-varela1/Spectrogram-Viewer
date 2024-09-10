FROM python:3.10.14-slim
WORKDIR /get_spec
COPY . /get_spec
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./app.py"]