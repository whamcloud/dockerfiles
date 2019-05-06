FROM imlteam/copr
RUN rpm -Uvh https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm \
  && yum-config-manager --add-repo=https://download.mono-project.com/repo/centos7-stable.repo \
  && yum install -y epel-release \
  && yum install -y mono-devel dotnet-sdk-2.1 nodejs nodejs-packaging \
  && yum clean all \
  && rm -rf /var/cache/yum \
  && rpm --rebuilddb \
  && dotnet tool install fake-cli --tool-path=/usr/local/bin
