FROM imlteam/copr

ARG toolchain=stable
RUN cd /root \
  && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain $toolchain
ENV PATH $PATH:/root/.cargo/bin
ENV CARGO_HOME /root/.cargo
