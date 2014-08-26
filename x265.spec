Summary:	H.265/HEVC video encoder
Summary(pl.UTF-8):	Koder obrazu H.265/HEVC
Name:		x265
Version:	1.3
Release:	0.20140825.2
License:	GPL v2+
Group:		Libraries
# hg clone -r stable https://bitbucket.org/multicoreware/x265
# cd x265 && hg archive x265-stable.tar.bz2
Source0:	%{name}-stable.tar.bz2
# Source0-md5:	1e23098d7aa53729babc377ee8ada3d9
Patch0:		%{name}-opt.patch
Patch1:		%{name}-libdir.patch
URL:		http://x265.org/
BuildRequires:	cmake >= 2.8.8
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.605
%ifarch %{ix86} %{x8664}
BuildRequires:	yasm >= 1.2.0
%endif
Requires:	libx265 = %{version}-%{release}
# see CMakeLists.txt, more is probably possible
ExclusiveArch:	%{ix86} %{x8664} arm
# needs 64-bit atomic compare and swap
ExcludeArch:	i386 i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
H.265/HEVC video encoder.

%description -l pl.UTF-8
Koder obrazu H.265/HEVC.

%package -n libx265
Summary:	H.265/HEVC video encoder library
Summary(pl.UTF-8):	Biblioteka kodowania obrazu H.265/HEVC
Group:		Libraries

%description -n libx265
H.265/HEVC video encoder library.

%description -n libx265 -l pl.UTF-8
Biblioteka kodowania obrazu H.265/HEVC.

%package -n libx265-devel
Summary:	Header files for x265 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki x265
Group:		Development/Libraries
Requires:	libstdc++-devel
Requires:	libx265 = %{version}-%{release}

%description -n libx265-devel
Header files for x265 library.

%description -n libx265-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki x265.

%package -n libx265-static
Summary:	Static x265 library
Summary(pl.UTF-8):	Statyczna biblioteka x265
Group:		Development/Libraries
Requires:	libx265-devel = %{version}-%{release}

%description -n libx265-static
Static x265 library.

%description -n libx265-static -l pl.UTF-8
Statyczna biblioteka x265.

%prep
%setup -q -n x265-stable
%patch0 -p1
%patch1 -p1

%build
install -d source/build
cd source/build
%cmake .. \
	-DLIB_INSTALL_DIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C source/build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libx265 -p /sbin/ldconfig
%postun	-n libx265 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/reST/cli.rst
%attr(755,root,root) %{_bindir}/x265

%files -n libx265
%defattr(644,root,root,755)
%doc doc/reST/introduction.rst
%attr(755,root,root) %{_libdir}/libx265.so.31

%files -n libx265-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libx265.so
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_pkgconfigdir}/x265.pc

%files -n libx265-static
%defattr(644,root,root,755)
%{_libdir}/libx265.a
