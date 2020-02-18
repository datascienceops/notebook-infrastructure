FROM alpine:latest
LABEL maintainer="manasibelhe@gmail.com"

RUN apk --no-cache add bash
RUN apk --no-cache add --update curl ca-certificates
RUN apk --no-cache add jq gettext

ENV KUBE_LATEST_VERSION="v1.14.2"

RUN curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl

RUN apk --no-cache add git
RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN git clone https://github.com/datascienceops/notebook-infrastructure.git
RUN pip install WTForms

RUN ls -lrt
RUN pwd
EXPOSE 8000
RUN ls -lrt /notebook-infrastructure/ContainerAsService/
RUN /usr/bin/python /notebook-infrastructure/ContainerAsService/ContainerAsService.py
RUN python /notebook-infrastructure/ContainerAsService/ContainerAsService.py