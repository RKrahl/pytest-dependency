%bcond_without tests
%global distname pytest-dependency

%if 0%{?sle_version} >= 150500
%global pythons python3 python311
%else
%{?!python_module:%define python_module() python3-%{**}}
%define skip_python2 1
%endif

Name:		python-%{distname}
Version:	$version
Release:	0
Summary:	$description
License:	Apache-2.0
URL:		$url
Group:		Development/Languages/Python
Source:		https://github.com/RKrahl/pytest-dependency/releases/download/%{version}/%{distname}-%{version}.tar.gz
BuildRequires:	%{python_module base >= 3.4}
BuildRequires:	%{python_module setuptools}
BuildRequires:	fdupes
BuildRequires:	python-rpm-macros
%if %{with tests}
BuildRequires:	%{python_module distutils-pytest}
BuildRequires:	%{python_module pytest >= 3.7}
%endif
Requires:	python-pytest >= 3.7
BuildArch:	noarch
%python_subpackages

%description
$long_description


%prep
%setup -q -n %{distname}-%{version}


%build
%python_build


%install
%python_install
%fdupes %{buildroot}%{python_sitelib}


%if %{with tests}
%check
%python_expand $$python setup.py test
%endif


%files %{python_files}
%license LICENSE.txt
%doc README.rst
%{python_sitelib}/*


%changelog
