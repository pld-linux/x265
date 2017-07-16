#
# Conditional build:
%bcond_without	asm	# x86 assembler

%ifnarch %{ix86} %{x8664} x32
%undefine	with_asm
%endif

Summary:	H.265/HEVC video encoder
Summary(pl.UTF-8):	Koder obrazu H.265/HEVC
Name:		x265
Version:	2.5
Release:	1
License:	GPL v2+
Group:		Libraries
# also at https://bitbucket.org/multicoreware/x265/downloads
Source0:	http://ftp.videolan.org/pub/videolan/x265/%{name}_%{version}.tar.gz
# Source0-md5:	192e54fa3068b594aa44ab2b703f071d
Patch0:		%{name}-opt.patch
Patch1:		%{name}-x32.patch
URL:		http://x265.org/
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	numactl-devel >= 2
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_asm:BuildRequires:	yasm >= 1.2.0}
Requires:	libx265 = %{version}-%{release}
# see CMakeLists.txt, more is probably possible
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} ppc64 ppc64le
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
Requires:	libstdc++-devel >= 6:4.8
Requires:	libx265 = %{version}-%{release}
Requires:	numactl-devel >= 2

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
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1

%build
install -d source/build
cd source/build
%cmake .. \
	-DENABLE_ASSEMBLY=%{!?with_asm:OFF}%{?with_asm:ON} \
	-DENABLE_HDR10_PLUS=ON \
	-DENABLE_SHARED=ON \
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
%attr(755,root,root) %{_libdir}/libx265.so.130
%attr(755,root,root) %{_libdir}/libhdr10plus.so

%files -n libx265-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libx265.so
%{_includedir}/hdr10plus.h
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_pkgconfigdir}/x265.pc

%files -n libx265-static
%defattr(644,root,root,755)
%{_libdir}/libhdr10plus.a
%{_libdir}/libx265.a
