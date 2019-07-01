FROM imlteam/copr
RUN yum remove -y cargo \
  && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable \
  && $HOME/.cargo/bin/rustup target add wasm32-unknown-unknown \
  && $HOME/.cargo/bin/cargo install -f wasm-bindgen-cli
ENV PATH $PATH:/root/.cargo/bin
