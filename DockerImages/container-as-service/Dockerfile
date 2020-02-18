FROM alpine:3.9
LABEL maintainer="manasibelhe@gmail.com"

RUN apk --no-cache add bash
RUN apk --no-cache add --update curl ca-certificates
RUN apk --no-cache add jq gettext

ENV KUBE_LATEST_VERSION="v1.14.2"

RUN curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl

RUN apk --no-cache add git

RUN git clone https://github.com/datascienceops/notebook-infrastructure.git \
RUN pip install WTForms
RUN ls
RUN pwd
ADD ContainerAsService ./ ContainerAsService/

EXPOSE 8000
CMD ["python ContainerAsService/ContainerAsService.py"]