FROM python:3.9

WORKDIR /usr/src/app

COPY api.py .

COPY db.py .

COPY utilModule.py .

COPY unhautorizedException.py .

RUN pip install flask

RUN pip install jsonify

RUN pip install requests

RUN pip install mysql.connector

RUN pip install matplotlib

EXPOSE 8000:8000

CMD ["python", "api.py"]