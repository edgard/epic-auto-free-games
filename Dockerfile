FROM debian:stable-slim

# update apt db
RUN apt-get update

# install chromium/driver
RUN apt-get install -y --no-install-recommends chromium chromium-driver

# install selenium and deps
RUN apt-get install -y --no-install-recommends python3 python3-bs4 python3-lxml python3-selenium

# copy script
COPY free_games.py /usr/src/app/

# switch to workdir
WORKDIR /usr/src/app

# cleanup
RUN apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

# run app
ENTRYPOINT ["./free_games.py"]
