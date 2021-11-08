%define git_commit_short 516144c
%define git_commit 516144c6a05a149d888ec4b983f3f5ba76acded6

Name:           anbox-modules
Version:        git%{git_commit_short}
Release:        1%{?dist}
Summary:        DKMS Kernel modules for Anbox

License:        GPL
URL:            https://github.com/choff/%{name}
Source0:        https://github.com/choff/%{name}/archive/%{git_commit_short}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       dkms
Requires:       systemd-udev
%{?systemd_requires}
BuildRequires:	systemd
Requires(posttrans): dkms
Requires(preun):  dkms

%description
Kernel modules required by Anbox

%prep
%setup -q -n %{name}-%{git_commit}

%build

%install
install -dm 755 %{buildroot}%{_udevrulesdir}
install -pm 644 99-anbox.rules %{buildroot}%{_udevrulesdir}/99-anbox.rules

install -dm 755 %{buildroot}%{_modulesloaddir}
install -pm 644 anbox.conf %{buildroot}%{_modulesloaddir}/anbox.conf

install -dm 755 %{buildroot}%{_usrsrc}
cp -rT ashmem %{buildroot}%{_usrsrc}/anbox-ashmem-1
cp -rT binder %{buildroot}%{_usrsrc}/anbox-binder-1

%check

%files
%defattr(-,root,root,-)
%{_udevrulesdir}/99-anbox.rules
%{_modulesloaddir}/anbox.conf
%{_usrsrc}/anbox-ashmem-1/
%{_usrsrc}/anbox-binder-1/

%posttrans
%udev_rules_update
dkms install anbox-ashmem/1
dkms install anbox-binder/1

%preun
dkms remove anbox-ashmem/1 --all
dkms remove anbox-binder/1 --all

%postun
%udev_rules_update


%changelog
* Mon Nov 08 2021 Jerzy Drozdz <jerzy.drozdz@jdsieci.pl> - git516144c-1
- Initial build

