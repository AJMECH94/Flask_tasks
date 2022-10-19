FROM python:3
ENV PYTHONUNBUFFERED=1
COPY ./ /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
