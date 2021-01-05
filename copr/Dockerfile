FROM centos:7
WORKDIR /build
RUN yum install -y dnf epel-release \
  && yum install -y yum-plugin-copr \
  && dnf install -y 'dnf-command(copr)' \
  && dnf install -y python python-devel openssl openssl-devel \
  && dnf copr enable -y @copr/copr \
  && dnf install -y copr-cli \
  && yum -y copr enable -y managerforlustre/buildtools \
  && yum install -y spectool \
  && yum clean all \
  && dnf clean all \
  && mkdir /root/.config \
  && touch /root/.config/copr
ADD copr-mfl.enc /tmp
COPY create_build.py /usr/bin/create_build
ENTRYPOINT [ "/usr/bin/create_build" ]
