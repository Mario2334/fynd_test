FROM python:3.8-buster

ADD . /home/backend/
WORKDIR /home/backend/

RUN pip install -r requirements.txt
#RUN cd scripts && python seed.py
RUN chmod +x startup.sh
CMD ["sh","startup.sh"]