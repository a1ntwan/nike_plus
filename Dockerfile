FROM openstax/selenium-chrome
ENV TZ=Europe/Moscow
ENV DISPLAY=:0
USER root
RUN mkdir -p /screen && \
    mkdir -p /sneakers/logs
COPY requirements.txt defender.crx webrtc.crx sneakers.py /sneakers/
WORKDIR /sneakers
RUN apt-get update -y && \
    apt-get install xvfb -y && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome-stable_current_amd64.deb && \
    dpkg -i /tmp/google-chrome-stable_current_amd64.deb && \
    rm -rf /tmp/google-chrome-stable_current_amd64.deb
ADD https://chromedriver.storage.googleapis.com/96.0.4664.18/chromedriver_linux64.zip /tmp/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver_linux64.zip -d /sneakers/chromedriver && \
    chmod 755 /sneakers/chromedriver && \
    rm -rf /tmp/chromedriver_linux64.zip
