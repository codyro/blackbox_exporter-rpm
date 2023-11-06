%global debug_package %{nil}

Name:           blackbox_exporter
Version:        0.24.0
Release:        2%{?dist}
Summary:        Blackbox prober exporter
License:        Apache-2.0
URL:            https://github.com/prometheus/%{name}

Source0:        https://github.com/prometheus/%{name}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.service


BuildRequires:  git
BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Provides:       %{name} = %{version}

%description
The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP, ICMP and gRPC.

%prep
%autosetup

%build
make build

%pre
getent passwd %{name} >/dev/null || \
  useradd \
      --system --user-group --shell /sbin/nologin \
      --home-dir /var/lib/%{name} \
      --comment "Blackbox Exporter" %{name}
exit 0

%install
# Binary
install -Dpm 0755 %{name}-%{version} %{buildroot}%{_bindir}/%{name}

# Configuration
install -Dpm 0644 blackbox.yml %{buildroot}%{_sysconfdir}/%{name}/config.yml

# systemd service
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
go test -v ./...

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/usr/sbin/userdel %{name}

%files
# Binary
%{_bindir}/%{name}

# Configuration
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.yml

# systemd
%{_unitdir}/%{name}.service

%changelog
* Sat Nov 06 2023 Cody Robertson <cody@nerdymuffin.com>
- Move couple of lines for readability
- Bump release

* Sat Oct 21 2023 Fabian Mettler <dev@maveonair.com>
- Initial package creation of version 0.24.0
