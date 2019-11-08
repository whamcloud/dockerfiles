FROM imlteam/copr-rust:stable
ADD lustre-client.repo /etc/yum.repos.d
RUN yum -y install lustre-client \
  && yum clean all
