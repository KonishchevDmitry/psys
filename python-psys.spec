%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:    python-psys
Version: 0.3
Release: 1%{?dist}
Summary: A Python module with a set of basic tools for writing system utilities

Group:   Development/Languages
License: GPLv3
URL:     http://github.com/KonishchevDmitry/psys
Source:  http://pypi.python.org/packages/source/p/psys/psys-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python-setuptools

Requires: python-pcore

%description
A Python module with a set of basic tools for writing system utilities


%prep
%setup -n psys-%version -q


%build
%{__python} setup.py build


%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

%{__python} setup.py install -O1 --skip-build --root "%buildroot"


%files
%defattr(-,root,root,-)

%python_sitelib/psys
%python_sitelib/psys-*.egg-info


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
