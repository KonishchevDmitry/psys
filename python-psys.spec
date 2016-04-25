%if 0%{?fedora} > 12 || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif
%if 0%{with python3}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif  # with python3

%define project_name psys

Name:    python-%project_name
Version: 0.3
Release: 1%{?dist}
Summary: A Python module with a set of basic tools for writing system utilities

Group:   Development/Languages
License: GPLv3
URL:     http://github.com/KonishchevDmitry/%project_name
Source:  http://pypi.python.org/packages/source/p/%project_name/%project_name-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python2-devel python-setuptools
%if 0%{with python3}
BuildRequires: python3-devel python3-setuptools
%endif  # with python3

Requires: python-pcore

%description
A Python module with a set of basic tools for writing system utilities


%if 0%{with python3}
%package -n python3-%project_name
Summary: A Python module with a set of basic tools for writing system utilities

Requires: python3-pcore

%description -n python3-%project_name
A Python module with a set of basic tools for writing system utilities
%endif  # with python3


%prep
%setup -n %project_name-%version -q


%build
make PYTHON=%{__python2}
%if 0%{with python3}
make PYTHON=%{__python3}
%endif  # with python3


%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

make PYTHON=%{__python2} INSTALL_FLAGS="-O1 --root '%buildroot'" install
%if 0%{with python3}
make PYTHON=%{__python3} INSTALL_FLAGS="-O1 --root '%buildroot'" install
%endif  # with python3


%files
%defattr(-,root,root,-)
%{python2_sitelib}/psys
%{python2_sitelib}/psys-*.egg-info
%doc ChangeLog README INSTALL

%if 0%{with python3}
%files -n python3-%project_name
%defattr(-,root,root,-)
%{python3_sitelib}/psys
%{python3_sitelib}/psys-*.egg-info
%doc ChangeLog README INSTALL
%endif  # with python3


%clean
[ "%buildroot" = "/" ] || rm -rf "%buildroot"


%changelog
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
