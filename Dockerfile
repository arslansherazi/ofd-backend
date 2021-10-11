FROM python:3.8.6
RUN git clone https://access_token:djVw1KHbykK3GShZbLsb@gitlab.com/arslansherazi/ofd-backend.git
WORKDIR /ofd-backend
RUN git checkout master
RUN git pull
RUN git checkout v100-aws-apps
RUN python3.8 -m venv venv
RUN . venv/bin/activate
RUN sh scripts/install_requirements.sh
EXPOSE 8000
ENTRYPOINT ["python3.8", "manage.py", "runserver"]
