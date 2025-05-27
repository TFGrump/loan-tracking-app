FROM python:3.12

RUN apt-get update

WORKDIR /code

COPY requirements.txt .
RUN python3 -m pip install -r "requirements.txt"

COPY loan-tracker/ /code/loan-tracker

EXPOSE 5000
CMD ["python3", "-m", "flask", "--app", "loan-tracker", "run", "--host", "0.0.0.0"]
