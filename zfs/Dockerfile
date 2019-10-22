FROM centos:7

RUN yum install -y epel-release http://download.zfsonlinux.org/epel/zfs-release.el7_6.noarch.rpm \
  && yum install -y zfs libzfs2-devel --nogpgcheck \
  && yum clean all \
  && cd /root \
  && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable \
  && $HOME/.cargo/bin/rustup component add clippy \
  && $HOME/.cargo/bin/rustup component add rustfmt
ENV PATH $PATH:/root/.cargo/bin
ENV CARGO_HOME /root/.cargo
