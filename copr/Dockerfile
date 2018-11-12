FROM fedora:latest
WORKDIR /build
RUN dnf install -y 'dnf-command(copr)' \
  && dnf install -y python openssl \
  && dnf copr enable -y @copr/copr \
  && dnf install -y copr-cli \
  && mkdir /root/.config \
  && touch /root/.config/copr
ADD copr-mfl.enc /tmp
COPY create_build.py /usr/bin/create_build
ENTRYPOINT [ "/usr/bin/create_build" ]
