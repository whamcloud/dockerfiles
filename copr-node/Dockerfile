FROM imlteam/copr
RUN curl -sL https://rpm.nodesource.com/setup_12.x | bash - \
  && yum install -y nodejs \
  && npm i -g npm \
  && yum clean all
