# Note that RHEL6 is pinned at 0.3.6 due to ABI.  Fortunately most of what
# changed after 0.3.6 was deletions, and factoring some sub-libraries out
# to their own subpackages.

Name:		xcb-util
Version:	0.3.6
Release:	5%{?dist}
Summary:	Convenience libraries sitting on top of libxcb

Group:		System Environment/Libraries
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
# source compat header for post-0.3.8-expecting consumers
Source1:	xcb_util.h
Source2:	xcb-util.pc.in
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	gperf, pkgconfig, libxcb-devel >= 1.4, m4, xorg-x11-proto-devel
BuildRequires:	chrpath

%description
The xcb-util module provides a number of libraries which sit on top of
libxcb, the core X protocol library, and some of the extension
libraries. These experimental libraries provide convenience functions
and interfaces which make the raw X protocol more usable. Some of the
libraries also provide client-side code which is not strictly part of
the X protocol but which have traditionally been provided by Xlib.

%package 	devel
Summary:	Development and header files for xcb-util
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig
%description	devel
Development files for xcb-util.

%prep
%setup -q
# moral equivalent of fd626329982cc2766e5a85a75ea2800b7aa3f114
sed -i s/@LIBS@// */*.pc.in

%build
%configure --with-pic --disable-static

make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
install -p %{SOURCE1} %{buildroot}%{_includedir}/xcb
sed s!@LIBDIR@!%{_libdir}! %{SOURCE2} > %{buildroot}%{_libdir}/pkgconfig/xcb-util.pc

# remove RPATH
chrpath --delete $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libxcb-*.so.*

# remove libraries that have their own srpm now
rm -f %{buildroot}%{_libdir}/libxcb-{icccm,image,keysyms}.so*

# also pkgconfig
rm -f %{buildroot}%{_libdir}/pkgconfig/xcb-{icccm,image,keysyms}.pc

# also headers
rm -f %{buildroot}%{_includedir}/xcb/xcb_{icccm,image,keysyms}.h

rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libxcb-atom.so.1*
%{_libdir}/libxcb-aux.so.0*
%{_libdir}/libxcb-event.so.1*
%{_libdir}/libxcb-property.so.1*
%{_libdir}/libxcb-render-util.so.0*
%{_libdir}/libxcb-reply.so.1*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h

%changelog
* Wed Apr 23 2014 Adam Jackson <ajax@redhat.com> 0.3.6-5
- Add <xcb/xcb_util.h> and xcb-util.pc for source compat with >= 0.3.8
- Backport pkgconfig fix from upstream
- Don't install -{icccm,image,keysyms}, they live in their own srpms now

* Fri Aug 28 2009 Michal Nowak <mnowak@redhat.com> - 0.3.6-1
- 0.3.6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Adam Jackson <ajax@redhat.com> 0.3.5-1
- xcb-util 0.3.5

* Mon Jul 06 2009 Adam Jackson <ajax@redhat.com> 0.3.4-2
- Explicitly list DSOs so we're notified of version changes.

* Sat Jun 13 2009 Michal Nowak <mnowak@redhat.com> - 0.3.4-1
- 0.3.4; needed for Awesome 3.3

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Michal Nowak <mnowak@redhat.com> - 0.3.3-1
- 0.3.3
- removed patches already in git (and 0.3.3)

* Fri Dec 19 2008 Michal Nowak <mnowak@redhat.com> - 0.3.2-2
- hack the sed lines after %%configure out and hack chrpath in
- make check is running again

* Thu Dec 18 2008 Michal Nowak <mnowak@redhat.com> - 0.3.2-1
- 0.3.2
- remove rpath (x86-64)
- xcb_keysyms: remove xcb_lookup_t
- Revert "keysyms: use xcb_key_lookup_t type for col paramter"
- temporary disabled %%check due to RPATH regression

* Thu Dec  4 2008 Michal Nowak <mnowak@redhat.com> - 0.3.1-2
- patch for exit() in aux library (Peter Harris)
- slight changes in spec file

* Mon Nov 24 2008 Michal Nowak <mnowak@redhat.com> - 0.3.1-1
- 0.3.1
- fix license issue (Jonathan Landis)

* Fri Sep 19 2008 Michal Nowak <mnowak@redhat.com> - 0.3.0-1
- bump to 0.3.0

* Sun Aug 17 2008 Michal Nowak <mnowak@redhat.com> - 0.2.1-2
- new build deps: gperf, pkgconfig, libxcb, m4, xorg-x11-proto-devel
- not installing *.a files anymore
- configure with --with-pic

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> - 0.2.1-1
- initial package

