FROM imlteam/copr-rust:stable
RUN $HOME/.cargo/bin/rustup target add wasm32-unknown-unknown \
  && $HOME/.cargo/bin/cargo install -f wasm-bindgen-cli
ENV PATH $PATH:/root/.cargo/bin
ENV CARGO_HOME /root/.cargo
