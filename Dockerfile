FROM python:3-alpine

# update apk repo
RUN apk update

# install chromedriver
RUN apk add chromium chromium-chromedriver

# upgrade pip
RUN pip install --upgrade pip

# install app deps
RUN apk add build-base
RUN apk add libxml2-dev libxslt-dev
RUN pip install selenium bs4 lxml

# copy script
COPY free_games.py /usr/src/app/

# switch to workdir
WORKDIR /usr/src/app

# run app
ENTRYPOINT ["./free_games.py"]
