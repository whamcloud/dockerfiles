FROM imlteam/copr

ARG toolchain=stable
RUN yum install -y gcc \
  && yum install -y clang llvm-devel \
  && yum install -y kmod-devel \
  && yum clean all \
  && cd /root \
  && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain $toolchain
ENV PATH $PATH:/root/.cargo/bin
ENV CARGO_HOME /root/.cargo
ENV RUSTUP_HOME /root/.rustup
