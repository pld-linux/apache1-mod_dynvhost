%define		mod_name	dynvhost
%define 	apxs		/usr/sbin/apxs
Summary:	Dynamic Virtual Hosting
Summary(pl):	Dynamiczne Serwery Wirtualne
Name:		apache-mod_%{mod_name}
Version:	1
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(cs):	S��ov�/D�moni
Group(da):	Netv�rks/D�moner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	R�seau/Serveurs
Group(is):	Net/P�kar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	����/������
Group(sl):	Omre�ni/Stre�niki
Group(sv):	N�tverk/Demoner
Group(uk):	������/������
Source0:	http://funkcity.com/0101/projects/dynvhost/mod_%{mod_name}.tar.gz
URL:		http://funkcity.com/0101
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
BuildRequires:	zlib-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
The "mod_dynvhost" module will create pseudo name based VirtualHosts
on the fly. All you need is a directory with the fully qualified
domain name ( FQDN ) of your virtual site and the module will take
care of the rest.

%description -l pl
Modu� "mod_dynvhost" pozwala na tworzenie pseudo serwer�w wirtualnych
(name based). Wszystko czego potrzebujesz to katalog o pe�nej nazwie
(FQDN) wirtualnego serwera - modu� zajmie si� reszt�.

%prep 
%setup -q -n %{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

gzip -9nf README ChangeLog

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_pkglibdir}/*