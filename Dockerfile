FROM python:3.10-bullseye

# Installing Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
# Installing Chrome Driver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# Set display port as an environment variable
ENV DISPLAY=:99

# Preparing Docker
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD crontab /etc/cron.d/hello-cron
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/hello-cron

RUN apt-get update
RUN apt-get -y install cron

COPY entrypoint.sh /entrypoint.sh
COPY ./src /app

ENTRYPOINT ["sh", "/entrypoint.sh"]
CMD cron && tail -f /var/log/cron.log