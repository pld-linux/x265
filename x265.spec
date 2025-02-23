# TODO: vmaf
#
# Conditional build:
%bcond_without	asm		# assembler
%bcond_with	svt_hevc	# SVT-HEVC Encoder support
%bcond_with	vmaf		# VMAF support

%ifarch %{arm}
%define		with_asm	1
%endif

Summary:	H.265/HEVC video encoder
Summary(pl.UTF-8):	Koder obrazu H.265/HEVC
Name:		x265
Version:	4.1
Release:	1
License:	GPL v2+
Group:		Libraries
# some versions also at
#Source0:	https://download.videolan.org/videolan/x265/%{name}_%{version}.tar.gz
#Source0Download: https://bitbucket.org/multicoreware/x265_git/downloads/
Source0:	https://bitbucket.org/multicoreware/x265_git/downloads/%{name}_%{version}.tar.gz
# Source0-md5:	f1c3c80248d8574378a4aac8f374f6de
Patch0:		%{name}-opt.patch
Patch1:		%{name}-x32.patch
Patch2:		%{name}-arm_flags.patch
Patch3:		%{name}-vmaf.patch
URL:		https://www.x265.org/
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	numactl-devel >= 2
BuildRequires:	rpmbuild(macros) >= 2.007
%if %{with asm}
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm >= 2.13.0
%endif
%endif
%{?with_svt_hevc:BuildRequires:	svt-hevc-devel}
%{?with_vmaf:BuildRequires:	vmaf-devel}
Requires:	libx265 = %{version}-%{release}
# see CMakeLists.txt, more is probably possible
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} ppc64 ppc64le aarch64
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
%patch -P0 -p1
%patch -P1 -p1
%ifarch %{arm} aarch64
%patch -P2 -p1
%endif
%patch -P3 -p1

%build
install -d source/build
cd source/build
%ifarch %{arm} aarch64
export CFLAGS="%{rpmcflags} -fPIC"
export CXXFLAGS="%{rpmcxxflags} -fPIC"
%ifarch %{arm_with_neon}
export CFLAGS="$CFLAGS -DHAVE_NEON"
export CXXFLAGS="$CXXFLAGS -DHAVE_NEON"
%endif
%ifarch aarch64
export CFLAGS="$CFLAGS -flax-vector-conversions"
export CXXFLAGS="$CXXFLAGS -flax-vector-conversions"
%endif
%endif
%cmake .. \
	-DENABLE_ASSEMBLY=%{!?with_asm:OFF}%{?with_asm:ON} \
	-DENABLE_HDR10_PLUS=ON \
	%{?with_vmaf:-DENABLE_LIBVMAF=ON} \
	-DENABLE_SHARED=ON \
	%{?with_svt_hevc:-DENABLE_SVT_HEVC=ON} \
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
%attr(755,root,root) %{_libdir}/libx265.so.215
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
