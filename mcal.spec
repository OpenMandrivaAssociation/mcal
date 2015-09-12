%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Modular Calendar Access Library
Name:		mcal
Version:	0.7
Release:	28
Group:		System/Libraries
License:	GPLv2+
Url:		http://mcal.chek.com/
Source0:	lib%{name}-%{version}.tar.gz
Source1:	mcaldrivers-0.9.tar.gz
Patch0:		libmcal-make.patch
Patch2:		mcal-mstore_calendar_path.patch
Patch3:		libmcal-0.7-gcc-4.0-fix.patch
Patch4:		libmcal-0.7-flexfix.diff
Patch5:		libmcal-0.7-flex-2.5.37.patch
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	pam-devel

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

%package -n	%{devname}
Summary:	MCAL header files
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}   

%description -n	%{devname}
Header files for MCAL-based programs development.

%prep

%setup -q -n lib%{name} -a1
mv -f mcal-drivers/* .
rm -rf mcal-drivers
%patch0 -p1 -b .make
%patch2 -p0 -b .calpath
%patch3 -p1 -b .gcc4_0
%patch4 -p0 -b .flex
%patch5 -p1

# lib64 fix
sed -i -e "s|/lib\b|/%{_lib}|g" Makefile*

%build
export OPTFLAGS="%{optflags} -fPIC -D_REENTRANT"

%make -C icap
%make -C mstore

%configure2_5x \
	--disable-static \
	--with-icap \
	--with-mstore

%make

%install
%makeinstall_std

mv -f mstore/Changelog Changelog.mstore
mv -f mstore/README README.mstore

install -d -m 1777 %{buildroot}/var/lib/calendar
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/mpasswd

%files -n %{libname}
%config(noreplace) %{_sysconfdir}/mpasswd
%{_libdir}/libmcal.so.%{major}*
/var/lib/calendar

%files -n %{devname}
%doc CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore
%{_libdir}/lib*.so
%{_includedir}/*

