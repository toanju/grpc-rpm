Summary: gRPC, A high performance, open-source universal RPC framework
Name: grpc
Version: 1.8.4
Release: 1%{?dist}
License: BSD
URL: http://www.grpc.io/
Source0: https://github.com/grpc/grpc/archive/v%{version}.tar.gz
Patch0: Silence_openssl_1.1.0_warnings.patch
Patch1: Add-pkgconfig-results-to-LDFLAGS.patch

BuildRequires: pkgconfig gcc-c++
BuildRequires: protobuf-devel
BuildRequires: protobuf-compiler
BuildRequires: openssl-devel
%if 0%{?rhel}
BuildRequires: git
BuildRequires: iproute
%else
BuildRequires: c-ares-devel
%endif

%description
Remote Procedure Calls (RPCs) provide a useful abstraction for
building distributed applications and services. The libraries in this
package provide a concrete implementation of the gRPC protocol,
layered over HTTP/2. These libraries enable communication between
clients and servers using any combination of the supported languages.

%package plugins
Summary: gRPC protocol buffers compiler plugins
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: protobuf-compiler

%description plugins
Plugins to the protocol buffers compiler to generate gRPC sources.

%package devel
Summary: gRPC library development files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and files for gRPC libraries.

%package static
Summary: gRPC library static files
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libraries for gRPC.

%prep
%setup -q
%if 0%{?fedora} > 25
%patch0 -p1
%endif
%patch1 -p1
%if 0%{?rhel}
git clone -b cares-1_12_0 https://github.com/c-ares/c-ares.git third_party/cares/cares
%endif

%build
%make_build

%check

%install
rm -rf %{buildroot}; mkdir %{buildroot}
make install prefix="%{buildroot}/usr"
%ifarch x86_64
mkdir -p %{buildroot}/usr/lib64
mv %{buildroot}/usr/lib/* %{buildroot}/usr/lib64/
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_libdir}/*.so.*
%{_datadir}/grpc
%attr(0644, root, root) %{_datadir}/grpc/roots.pem

%files plugins
%doc README.md
%license LICENSE
%{_bindir}/*

%files devel
%{_libdir}/*.so
%attr(0644, root, root) %{_libdir}/pkgconfig/*
%{_includedir}/*

%files static
%attr(0644, root, root) %{_libdir}/*.a

%changelog
* Sun Oct 15 2017 Tobias Jungel <tobias.jungel@gmail.com> - 1.6.6-1
- Update upstream
* Wed Sep 06 2017 Jeff Mendoza <jeffmendoza@google.com> - 1.4.5-1
- Update upstream
* Wed Jun 28 2017 Jeff Mendoza <jeffmendoza@google.com> - 1.4.1-1
- Initial revision
