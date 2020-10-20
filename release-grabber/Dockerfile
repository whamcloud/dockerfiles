FROM centos:7.7.1908

WORKDIR /build

COPY build-deps.sh /usr/bin/build-deps.sh

RUN yum clean all \
  && yum install -y createrepo

CMD ["build-deps.sh"]
