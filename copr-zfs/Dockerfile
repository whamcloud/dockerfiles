FROM imlteam/copr-rust:stable
RUN yum -y install http://download.zfsonlinux.org/epel/zfs-release.el7_6.noarch.rpm \
  && yum install -y zfs libzfs2-devel --nogpgcheck \
  && yum clean all
