FROM centos:latest

RUN yum update -y \
  && yum -y install epel-release \
  && yum install -y git rpm-build ed sudo rpmlint rpkg mock \
  && yum clean all \
  && rm -rf /var/cache/yum

RUN useradd --gid mock mockbuild
