%define		mod_name	dynvhost
%define 	apxs		/usr/sbin/apxs1
Summary:	Dynamic Virtual Hosting
Summary(pl.UTF-8):   Dynamiczne Serwery Wirtualne
Name:		apache1-mod_%{mod_name}
Version:	1
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://funkcity.com/0101/projects/dynvhost/mod_%{mod_name}.tar.gz
# Source0-md5:	7608ca6ce5c906bfe960cd0f92bdb6d8
URL:		http://funkcity.com/0101/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_dynvhost <= 1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
The "mod_dynvhost" module will create pseudo name based VirtualHosts
on the fly. All you need is a directory with the fully qualified
domain name (FQDN) of your virtual site and the module will take care
of the rest.

%description -l pl.UTF-8
Moduł "mod_dynvhost" pozwala na tworzenie pseudo serwerów wirtualnych
(name based). Wszystko czego potrzebujesz to katalog o pełnej nazwie
(FQDN) wirtualnego serwera - moduł zajmie się resztą.

%prep
%setup -q -n %{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1-2.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
