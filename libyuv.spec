#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	neon		# disable neon

%ifnarch %{arm}
%undefine	with_neon
%endif

Summary:	YUV conversion and scaling functionality library
Name:		libyuv
Version:	0
Release:	0.14.20121001svn389
License:	BSD
Group:		Development/Libraries
URL:		http://code.google.com/p/libyuv/
## svn -r 389 export http://libyuv.googlecode.com/svn/trunk libyuv-0
## tar -cjvf libyuv-0.tar.bz2 libyuv-0
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	06a4d57a1d0848fcc9f5695accd771a7
Patch1:		autotools-support.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtest-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
%{?with_neon:BuildRequires:	neon-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an open source project that includes YUV conversion and
scaling functionality. Converts all webcam formats to YUV (I420).
Convert YUV to formats for rendering/effects. Rotate by 90 degrees to
adjust for mobile devices in portrait mode. Scale YUV to prepare
content for compression, with point, bilinear or box filter.

%package devel
Summary:	The development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Additional header files for development with %{name}.

%prep
%setup -q
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--with-pic \
	--with-test \
	--with-mjpeg \
	%{__enable_disable neon} \
	%{nil}

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE PATENTS
%attr(755,root,root) %{_libdir}/libyuv.so.*.*.*
%ghost %{_libdir}/libyuv.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}.h
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_pkgconfigdir}/%{name}.pc
