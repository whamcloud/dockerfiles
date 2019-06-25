FROM imlteam/copr
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash - \
  && yum install -y nodejs gcc-c++ make \
  && yum clean all \
  && npm i -g npm
