Summary:	Linux console utilities
Summary(pl):	Narz�dzia do obs�ugi konsoli
Name:		kbd
Version:	1.06
Release:	7
License:	GPL
Group:		Applications/Console
Group(de):	Applikationen/Konsole
Group(pl):	Aplikacje/Konsola
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/kbd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	kbdrate.8.pl
Source4:	lat2u-16.psf.gz
Source5:	lat2u.sfm.gz
Source6:	console.sh
Source7:	console.csh
Patch0:		%{name}-install.patch
Patch1:		%{name}-sparc.patch
Patch2:		%{name}-compose.patch
Patch3:		%{name}-compat-suffixes.patch
Patch4:		%{name}-unicode_start.patch
URL:		http://www.win.tue.nl/~aeb/linux/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Provides:	console-tools
Provides:	console-data
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	util-linux < 2.11
Obsoletes:	console-data
Obsoletes:	console-tools
Obsoletes:	console-tools-devel
Obsoletes:	console-tools-static

%description
This package contains utilities to load console fonts and keyboard
maps. It also includes a number of different fonts and keyboard maps.

%description -l pl
Pakiet zawiera narz�dzia do �adowania font�w konsolowych oraz map
klawiatury. Dodaktowo do��czono znaczn� liczb� r�nych font�w i map.

%prep
%setup  -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
./configure \
	--datadir=%{_datadir}
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{sysconfig,rc.d/init.d,profile.d},%{_mandir}/pl/man8}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

ln -sf /bin/loadkeys $RPM_BUILD_ROOT%{_bindir}/loadkeys

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/console
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/console
install %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/pl/man8
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/consolefonts/lat2u-16.psfu.gz
gunzip -c %{SOURCE5} >$RPM_BUILD_ROOT%{_datadir}/unimaps/lat2u.uni
install %{SOURCE6} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

rm -f doc/{*,*/*}.sgml
gzip -9nf CHANGES CREDITS README doc/*.txt

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add console

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz doc
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/console
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/console
%attr(755,root,root) /etc/profile.d/console.*

%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/console*
%{_datadir}/keymaps
%{_datadir}/unimaps

%{_mandir}/man?/*
%lang(pl) %{_mandir}/pl/man?/*
