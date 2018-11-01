FROM centos:centos7.5.1804

RUN yum -y install epel-release yum-plugin-copr http://download.zfsonlinux.org/epel/zfs-release.el7_5.noarch.rpm \
  && yum -y copr enable alonid/llvm-5.0.0 \
  && yum -y install nodejs clang-5.0.0 zfs libzfs2-devel --nogpgcheck \
  && yum clean all \
  && rm -rf /var/cache/yum
RUN curl https://sh.rustup.rs -sSf > /rustup.sh \
  && chmod 755 rustup.sh \
  && /rustup.sh -y \
  && rm -f /rustup.sh
ENV PATH="/root/.cargo/bin:${PATH}"
RUN npm i -g neon-cli@0.1.23
