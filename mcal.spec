%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define lib_name_orig lib%{name}

Summary:	Modular Calendar Access Library
Name:		mcal
Version:	0.7
Release:	%mkrel 11
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
URL:		http://mcal.chek.com/
Source0:	lib%{name}-%{version}.tar.bz2
Source1:	mcaldrivers-0.9.tar.bz2
Patch0:		libmcal-make.patch
Patch2:		mcal-mstore_calendar_path.patch
Patch3:		libmcal-0.7-gcc-4.0-fix.patch
Patch4:		libmcal-0.7-flexfix.diff
BuildRequires:	flex libtool pam-devel

%description
libmcal is a C library for accessing calendars. It's written to be
very modular, with plugable drivers.

%package -n     %{lib_name}
Summary:        Modular Calendar Access Library
Group:		System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with mcal.

%package -n     %{lib_name}-devel
Summary:	MCAL header files
Group:		Development/C
Requires:       %{lib_name} = %{version}
Provides:       %{lib_name_orig}-devel = %{version}-%{release} 
Provides:       %{name}-devel = %{version}-%{release}   

%description -n %{lib_name}-devel 
Header files for MCAL-based programs development.

%prep

%setup -q -n %{lib_name_orig} -a1
mv -f mcal-drivers/* .
%patch0 -p1 -b .make
%patch2 -p0 -b .calpath
%patch3 -p1 -b .gcc4_0
%patch4 -p0 -b .flex

# lib64 fix
perl -pi -e "s|/lib|/%{_lib}|g" Makefile*

%build
%make -C icap
%make -C mstore

%configure --with-icap --with-mstore

%make 

%install
rm -rf %{buildroot}
install -d %{buildroot}

%make install DESTDIR=%{buildroot}

mv -f mstore/Changelog Changelog.mstore
mv -f mstore/README README.mstore

install -d -m 1777 %{buildroot}%{_localstatedir}/lib/calendar
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/mpasswd

%if %mdkversion < 200900
%post	-n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun	-n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(644,root,root,755)
%doc CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore
%config(noreplace) %{_sysconfdir}/mpasswd
%attr(755,root,root) %{_libdir}/lib*.so.*
%attr(1777,root,root) %{_localstatedir}/lib/calendar

%files -n %{lib_name}-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.la


