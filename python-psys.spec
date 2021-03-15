%if 0%{?fedora} > 12 || 0%{?epel} >= 6
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?epel} >= 7
%bcond_without python3_other
%endif

%if 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif
%if 0%{with python3}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python3_pkgversion: %global python3_pkgversion 3}
%endif  # with python3

%define project_name psys
%global project_description %{expand:
A Python module with a set of basic tools for writing system utilities}

Name:    python-%project_name
Version: 0.4.2
Release: 1%{?dist}
Summary: A Python module with a set of basic tools for writing system utilities

Group:   Development/Languages
License: MIT
URL:     http://github.com/KonishchevDmitry/%project_name
Source:  http://pypi.python.org/packages/source/p/%project_name/%project_name-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python2-devel python-setuptools

Requires: python-pcore

%description %{project_description}


%if 0%{with python3}
%package -n python%{python3_pkgversion}-%project_name
Summary: %{summary}
Requires: python%{python3_pkgversion}-pcore
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools

%description -n python%{python3_pkgversion}-%project_name %{project_description}
%endif  # with python3


%if 0%{with python3_other}
%package -n python%{python3_other_pkgversion}-%project_name
Summary: %{summary}
Requires: python%{python3_other_pkgversion}-pcore
BuildRequires: python%{python3_other_pkgversion}-devel
BuildRequires: python%{python3_other_pkgversion}-setuptools

%description -n python%{python3_other_pkgversion}-%project_name %{project_description}
%endif  # with python3_other


%prep
%setup -n %project_name-%version -q


%build
make PYTHON=%{__python2}
%if 0%{with python3}
make PYTHON=%{__python3}
%endif  # with python3
%if 0%{with python3_other}
make PYTHON=%{__python3_other}
%endif  # with python3_other


%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

make PYTHON=%{__python2} INSTALL_FLAGS="-O1 --root '%buildroot'" install
%if 0%{with python3}
make PYTHON=%{__python3} INSTALL_FLAGS="-O1 --root '%buildroot'" install
%endif  # with python3
%if 0%{with python3_other}
make PYTHON=%{__python3_other} INSTALL_FLAGS="-O1 --root '%buildroot'" install
%endif  # with python3_other


%files
%defattr(-,root,root,-)
%{python2_sitelib}/psys
%{python2_sitelib}/psys-*.egg-info
%doc ChangeLog README INSTALL

%if 0%{with python3}
%files -n python%{python3_pkgversion}-%project_name
%defattr(-,root,root,-)
%{python3_sitelib}/psys
%{python3_sitelib}/psys-*.egg-info
%doc ChangeLog README INSTALL
%endif  # with python3

%if 0%{with python3_other}
%files -n python%{python3_other_pkgversion}-%project_name
%defattr(-,root,root,-)
%{python3_other_sitelib}/psys
%{python3_other_sitelib}/psys-*.egg-info
%doc ChangeLog README INSTALL
%endif  # with python3_other


%clean
[ "%buildroot" = "/" ] || rm -rf "%buildroot"


%changelog
* Mon Mar 15 2021 Dmitry Konishchev <konishchev@gmail.com> - 0.4.2-1
- New version

* Sun Jan 13 2019 Mikhail Ushanov <gm.mephisto@gmail.com> - 0.4-2
- Add python3 package build for EPEL

* Thu Apr 28 2016 Dmitry Konishchev <konishchev@gmail.com> - 0.4-1
- Add psys.pipe module
- Add psys.process module
- Add psys.daemon.write_pidfile() and psys.daemonize() functions

* Mon Nov 18 2013 Dmitry Konishchev <konishchev@gmail.com> - 0.3-1
- New version

* Wed Nov 13 2013 Dmitry Konishchev <konishchev@gmail.com> - 0.2-1
- New version

* Fri Jun 28 2013 Dmitry Konishchev <konishchev@gmail.com> - 0.1.1-2
- Don't remove *.egg-info to make setup.py with entry_points work
- Provide python-pcore

* Thu Jun 27 2013 Dmitry Konishchev <konishchev@gmail.com> - 0.1.1-1
- New version

* Thu Dec 20 2012 Dmitry Konishchev <konishchev@gmail.com> - 0.1-1
- New package
