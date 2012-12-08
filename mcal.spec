%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Modular Calendar Access Library
Name:		mcal
Version:	0.7
Release:	18
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
BuildRequires:	autoconf automake libtool
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

%package -n	%{develname}
Summary:	MCAL header files
Group:		Development/C
Requires:	%{libname} >= %{version}
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
%makeinstall_std

mv -f mstore/Changelog Changelog.mstore
mv -f mstore/README README.mstore

install -d -m 1777 %{buildroot}/var/lib/calendar
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/mpasswd

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%doc CHANGELOG FAQ-MCAL FEATURE-IMPLEMENTATION HOW-TO-MCAL *.mstore
%config(noreplace) %{_sysconfdir}/mpasswd
%attr(0755,root,root) %{_libdir}/lib*.so.*
%attr(1777,root,root) /var/lib/calendar

%files -n %{develname}
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7-17mdv2011.0
+ Revision: 666395
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7-16mdv2011.0
+ Revision: 606633
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7-15mdv2010.1
+ Revision: 519039
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.7-14mdv2010.0
+ Revision: 426080
- rebuild

* Sun Dec 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.7-13mdv2009.1
+ Revision: 317083
- use %%ldflags, except --Wl,--no-undefined

* Fri Jul 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.7-12mdv2009.0
+ Revision: 231647
- fix build
- fix license
- fix devel package naming
- misc spec file fixes

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix no-buildroot-tag

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.7-10mdv2008.1
+ Revision: 153048
- rebuild
- kill re-definition of %%buildroot on Pixel's request


* Wed Mar 07 2007 Oden Eriksson <oeriksson@mandriva.com> 0.7-8mdv2007.1
+ Revision: 134575
- make it build on x86_64
- fix deps
- new P0 (PLD)
- added P4 (gnusolaris)
- bunzip patches
- misc spec file fixes
- Import mcal

* Wed Jan 11 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.7-5mdk
- add BuildRequires: libtool

* Sun Aug 21 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.7-4mdk
- patch3: fix build with gcc 4.0

