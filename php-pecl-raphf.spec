%define		php_name	php%{?php_suffix}
%define		modname		raphf
%define		status		stable
Summary:	%{modname} - Resource and persistent handles factory
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.4
Release:	1
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	e5e7e5c3954a5fd31c034c347f22c4a5
URL:		http://pecl.php.net/package/raphf/
BuildRequires:	%{php_name}-devel >= 3:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A reusable split-off of pecl_http's persistent handle and resource
factory API.

In PECL status of this extension is: %{status}.

%package devel
Summary:	Header files for raphf PECL extension
Group:		Development/Libraries
# does not require base
Requires:	php-devel >= 4:5.2.0

%description devel
Header files for raphf PECL extension.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%{__libtoolize}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

install -D php_raphf.h $RPM_BUILD_ROOT%{_includedir}/php/ext/raphf/php_raphf.h

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%files devel
%defattr(644,root,root,755)
%dir %{php_includedir}/ext/raphf
%{php_includedir}/ext/raphf/php_raphf.h
