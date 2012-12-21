%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:    python-psys
Version: 0.1
Release: 1%{?dist}
Summary: A Python module with a set of basic tools for writing system utilities

Group:   Development/Languages
License: GPLv3
URL:     http://github.com/KonishchevDmitry/psys
Source:  http://pypi.python.org/packages/source/p/psys/psys-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python-setuptools

%description
A Python module with a set of basic tools for writing system utilities


%prep
%setup -n psys-%{version} -q


%build
%{__python} setup.py build


%install
[ %buildroot = "/" ] || rm -rf %buildroot

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
find %buildroot/ -name '*.egg-info' -exec rm -rf -- '{}' '+'


%files
%defattr(-,root,root,-)
%{python_sitelib}/pcore
%{python_sitelib}/psys


%clean
[ %buildroot = "/" ] || rm -rf %buildroot


%changelog
* Thu Dec 20 2012 Dmitry Konishchev <konishchev@gmail.com> - 0.1-1
- New package.
