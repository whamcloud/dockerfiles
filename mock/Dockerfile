FROM centos:latest

RUN yum -y install epel-release yum-plugin-copr \
  && yum -y copr enable @mock/mock-stable \
  && yum -y copr enable clime/rpkg-util \
  && yum update -y \
  && yum install -y git make rpm-build ed sudo rpmlint rpkg mock \
  && yum clean all \
  && rm -rf /var/cache/yum \
  && sed -i $'1i config_opts[\'use_nspawn\'] = False' /etc/mock/default.cfg
