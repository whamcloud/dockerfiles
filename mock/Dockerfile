FROM centos:latest

RUN yum -y install epel-release yum-plugin-copr \
  && yum -y copr enable @mock/mock-stable \
  && yum -y copr enable clime/rpkg-util \
  && yum update -y \
  && yum install -y git rpm-build ed sudo rpmlint rpkg mock \
  && yum clean all \
  && rm -rf /var/cache/yum

RUN useradd --gid mock mockbuild
