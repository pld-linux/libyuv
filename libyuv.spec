#
# Conditional build:
%bcond_without	tests		# unit tests

Summary:	YUV conversion and scaling functionality library
Summary(pl.UTF-8):	Biblioteka do konwersji i skalowania YUV
Name:		libyuv
# see include/libyuv/version.h
%define	yuv_ver	1788
%define	gitref	d19f69d9df7a54eae9cfae0b650921f675d9f01a
%define	snap	20210611
%define	rel	1
Version:	0.%{yuv_ver}
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Development/Libraries
Source0:	https://chromium.googlesource.com/libyuv/libyuv/+archive/%{gitref}.tar.gz?/%{name}-%{snap}.tar.gz
# Source0-md5:	9783a72e05ef548dd6f6ff7c1775e744
Source1:	%{name}.pc
Patch0:		shared-lib.patch
URL:		https://chromium.googlesource.com/libyuv/libyuv
BuildRequires:	cmake >= 2.8
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
%setup -q -c
%patch0 -p1

%build
mkdir -p build
cd build
%cmake .. \
	%{?with_tests:-DTEST=ON}

%{__make}

%{?with_tests:./libyuv_unittest}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -e 's|@PACKAGE_VERSION@|%{yuv_ver}|' \
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
%attr(755,root,root) %{_bindir}/yuvconvert
%attr(755,root,root) %{_libdir}/libyuv.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libyuv.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libyuv.so
%{_includedir}/libyuv.h
%{_includedir}/libyuv
%{_pkgconfigdir}/libyuv.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libyuv.a
