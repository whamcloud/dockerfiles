FROM imlteam/copr
RUN rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm \
  && rpm --import "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF" \
  && su -c 'curl https://download.mono-project.com/repo/centos7-stable.repo | tee /etc/yum.repos.d/mono-centos7-stable.repo' \
  && yum install -y epel-release \
  && yum install -y mono-devel dotnet-sdk-2.1 nodejs nodejs-packaging \
  && yum clean all \
  && rm -rf /var/cache/yum \
  && rpm --rebuilddb \
  && dotnet tool install fake-cli --tool-path=/usr/local/bin
