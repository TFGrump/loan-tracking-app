FROM python:3.12

RUN apt-get update

WORKDIR /code

COPY requirements.txt .
RUN python3 -m pip install -r "requirements.txt"

COPY loan_tracker/ /code/loan_tracker
COPY app.py /code/

EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0"]
