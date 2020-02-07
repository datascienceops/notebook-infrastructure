FROM node:latest

# run installation/ build commands.
RUN git clone https://github.com/nteract/commuter.git
RUN npm install -g yarn --force

ENV HOST=0.0.0.0
ENV PORT=4000

EXPOSE 4000

