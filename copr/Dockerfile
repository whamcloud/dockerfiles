FROM centos:latest
WORKDIR /build
RUN yum install -y dnf epel-release \
  && yum install -y yum-plugin-copr \
  && yum install -y openssl \
  && yum install -y openssl-devel \
  && dnf install -y 'dnf-command(copr)' \
  && dnf install -y python openssl \
  && dnf copr enable -y @copr/copr \
  && dnf install -y copr-cli \
  && yum -y copr enable -y managerforlustre/buildtools \
  && yum install -y rust-bundled-packaging spectool \
  && yum clean all \
  && dnf clean all \
  && mkdir /root/.config \
  && touch /root/.config/copr
ADD copr-mfl.enc /tmp
COPY create_build.py /usr/bin/create_build
ENTRYPOINT [ "/usr/bin/create_build" ]
