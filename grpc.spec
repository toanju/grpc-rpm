Summary: gRPC, A high performance, open-source universal RPC framework
Name: grpc
Version: 1.13.0
Release: 1%{?dist}
License: BSD
URL: http://www.grpc.io/
Source0: https://github.com/grpc/grpc/archive/v%{version}.tar.gz

Patch0: 0001-mitigate-gcc8-Wstringop-truncation-and-Wignored-qual.patch
Patch1: 0002-mitigate-gcc8-Werror-class-memaccess.patch

BuildRequires: pkgconfig gcc-c++
BuildRequires: protobuf-devel >= 3.5
BuildRequires: protobuf-compiler >= 3.5
BuildRequires: openssl-devel
BuildRequires: gtest-devel
BuildRequires: git
%if 0%{?rhel}
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
Requires: protobuf-compiler >= 3.5

%description plugins
Plugins to the protocol buffers compiler to generate gRPC sources.

%package cli
Summary: gRPC protocol buffers cli
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gflags
BuildRequires: gflags-devel

%description cli
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
%patch0 -p1
%patch1 -p1
%if 0%{?rhel}
git clone -b cares-1_13_0 https://github.com/c-ares/c-ares.git third_party/cares/cares
%endif
# goolgetest is pretty hardwired to the third_party dir
git clone -b release-1.8.0 https://github.com/google/googletest.git third_party/googletest

%build
%make_build

%check

%install
rm -rf %{buildroot}; mkdir %{buildroot}
make install prefix="%{buildroot}/usr"
make install-grpc-cli prefix="%{buildroot}/usr"
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

%files cli
%{_bindir}/grpc_cli

%files plugins
%doc README.md
%license LICENSE
%{_bindir}/grpc_*_plugin

%files devel
%{_libdir}/*.so
%attr(0644, root, root) %{_libdir}/pkgconfig/*
%{_includedir}/*

%files static
%attr(0644, root, root) %{_libdir}/*.a

%changelog
* Tue May 15 2018 Tobias Jungel <tobias.jungel@gmail.com> - 1.11.1-1
- Update to upsteam release
* Sat Apr 21 2018 Tobias Jungel <tobias.jungel@gmail.com> - 1.11.0-1
- Update to upsteam release
* Fri Feb 16 2018 Tobias Jungel <tobias.jungel@gmail.com> - 1.9.1-1
- Update to upsteam release
- add grpc_cli
* Mon Jan 22 2018 Tobias Jungel <tobias.jungel@gmail.com> - 1.8.5-1
- Update upstream
* Sun Oct 15 2017 Tobias Jungel <tobias.jungel@gmail.com> - 1.6.6-1
- Update upstream
* Wed Sep 06 2017 Jeff Mendoza <jeffmendoza@google.com> - 1.4.5-1
- Update upstream
* Wed Jun 28 2017 Jeff Mendoza <jeffmendoza@google.com> - 1.4.1-1
- Initial revision
