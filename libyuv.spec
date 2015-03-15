#
# Conditional build:
%bcond_with	static_libs	# don't build static library
%bcond_without	tests		# build without tests

%define	svnver	1325
Summary:	YUV conversion and scaling functionality library
Summary(pl.UTF-8):	Biblioteka do konwersji i skalowania YUV
Name:		libyuv
Version:	0.%{svnver}
Release:	1
License:	BSD
Group:		Development/Libraries
## svn -r 1325 export http://libyuv.googlecode.com/svn/trunk libyuv
## tar -cJf libyuv-svn1325.tar.bz2 --exclude-vcs libyuv
Source0:	%{name}-svn%{svnver}.tar.xz
# Source0-md5:	f18002950f43df0d168fbf8fcb5fc9c1
Source1:	%{name}.pc
Patch0:		shared-lib.patch
URL:		http://code.google.com/p/libyuv/
BuildRequires:	cmake
%{?with_tests:BuildRequires:	gtest-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an open source project that includes YUV conversion and
scaling functionality. Converts all webcam formats to YUV (I420).
Convert YUV to formats for rendering/effects. Rotate by 90 degrees to
adjust for mobile devices in portrait mode. Scale YUV to prepare
content for compression, with point, bilinear or box filter.

%description -l pl.UTF-8
Ten projekt o otwartych źródłach funkcjonalnością obejmuje konwersję
oraz skalowanie YUV. Potrafi:
- tłumaczyć formaty kamer internetowych na YUV (I420)
- przekształcać YUV na formaty zdatne do renderowania i efektów
- obracać obraz o 90 stopni, aby dostosowaćdo urządzeń przenośnych w
  trybie portretowym
- skalować YUV w celu przygotowania do kompresji z filtrem punktowym,
  dwuliniowym lub prostokątnym.

%package devel
Summary:	The development files for libyuv
Summary(pl.UTF-8):	Pliki programistyczne libyuv
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for development with libyuv.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem libyuv.

%package static
Summary:	Static libyuv library
Summary(pl.UTF-8):	Statyczna biblioteka libyuv
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libyuv library.

%description static -l pl.UTF-8
Statyczna biblioteka libyuv.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
mkdir -p build
cd build
%cmake .. %{?with_tests:-DTEST=ON}

%{__make}
%{?with_tests:./libyuv_unittest}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -e 's|@PACKAGE_VERSION@|%{svnver}|' \
	-e 's|@prefix@|%{_prefix}|' \
	-e 's|@exec_prefix@|%{_prefix}|' \
	-e 's|@libdir@|%{_libdir}|' \
	-e 's|@includedir@|%{_includedir}|' %{SOURCE1} >$RPM_BUILD_ROOT%{_pkgconfigdir}/libyuv.pc

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
%attr(755,root,root) %{_libdir}/libyuv.so
%{_includedir}/%{name}.h
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libyuv.a
%endif
