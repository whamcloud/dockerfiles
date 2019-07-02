FROM imlteam/copr
RUN yum remove -y cargo \
  && cd /root \
  && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable \
  && $HOME/.cargo/bin/rustup target add wasm32-unknown-unknown \
  && $HOME/.cargo/bin/cargo install -f wasm-bindgen-cli
ENV PATH $PATH:/root/.cargo/bin
ENV CARGO_HOME /root/.cargo
