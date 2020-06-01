FROM python

RUN apt-get update -y
RUN apt-get install -y curl sudo
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get install -y nodejs

COPY . .

RUN pip install virtualenv
RUN yes | npm run init

CMD [ "npm", "run", "start" ]
