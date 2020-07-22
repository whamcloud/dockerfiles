FROM imlteam/copr

ARG toolchain=stable
RUN yum clean all \
  && yum install -y gcc https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
  && yum install -y postgresql96-devel \
  && yum clean all \
  && cd /root \
  && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain $toolchain
RUN wget https://github.com/mozilla/sccache/releases/download/0.2.13/sccache-0.2.13-x86_64-unknown-linux-musl.tar.gz \
  && tar -xzvf sccache-*-x86_64-unknown-linux-musl.tar.gz \
  && mv sccache-*-x86_64-unknown-linux-musl/sccache /usr/bin \
  && rm -rf sccache-*-x86_64-unknown-linux-musl*
ENV PATH $PATH:/root/.cargo/bin
ENV CARGO_HOME /root/.cargo
ENV RUSTUP_HOME /root/.rustup
ENV SCCACHE_CACHE_SIZE="40G"
ENV SCCACHE_DIR /.cache/sccache
ENV RUSTC_WRAPPER="sccache"
