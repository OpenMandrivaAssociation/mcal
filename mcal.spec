%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Modular Calendar Access Library
Name:		mcal
Version:	0.7
Release:	%mkrel 15
Group:		System/Libraries
License:	GPLv2+
URL:		http://mcal.chek.com/
Source0:	lib%{name}-%{version}.tar.bz2
Source1:	mcaldrivers-0.9.tar.bz2
Patch0:		libmcal-make.patch
Patch2:		mcal-mstore_calendar_path.patch
Patch3:		libmcal-0.7-gcc-4.0-fix.patch
Patch4:		libmcal-0.7-flexfix.diff
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libmcal is a C library for accessing calendars. It's written to be very
modular, with plugable drivers.

%package -n	%{libname}
Summary:        Modular Calendar Access Library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with mcal.

%package -n	%{develname}
Summary:	MCAL header files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release} 
Provides:	%{name}-devel = %{version}-%{release}   
Obsoletes:	%{mklibname mcal -d 0}

%description -n	%{develname}
Header files for MCAL-based programs development.

%prep

%setup -q -n lib%{name} -a1
mv -f mcal-drivers/* .
rm -rf mcal-drivers
%patch0 -p1 -b .make
%patch2 -p0 -b .calpath
%patch3 -p1 -b .gcc4_0
%patch4 -p0 -b .flex

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" Makefile*

%build
export OPTFLAGS="%{optflags} -fPIC -D_REENTRANT"

%make -C icap
%make -C mstore

%configure2_5x \
    --with-icap \
    --with-mstore

%make

%install
rm -rf %{buildroot}

%makeinstall_std

mv -f mstore/Changelog Changelog.mstore
mv -f mstore/README README.mstore

install -d -m 1777 %{buildroot}/var/lib/calendar
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/mpasswd

%if %mdkversion < 200900
%post	-n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun	-n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(0644,root,root,0755)
%doc CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore
%config(noreplace) %{_sysconfdir}/mpasswd
%attr(0755,root,root) %{_libdir}/lib*.so.*
%attr(1777,root,root) /var/lib/calendar

%files -n %{develname}
%defattr(0644,root,root,0755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.la
