#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

Summary:	Functools like those found in stdlib
Summary(pl.UTF-8):	Functools podobne do tych z biblioteki standardowej
Name:		python3-jaraco.functools
# keep 2.x here for python2 support
Version:	4.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco.functools/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco_functools/jaraco_functools-%{version}.tar.gz
# Source0-md5:	b8a8d165da986efa1966abd91c45348e
URL:		https://pypi.org/project/jaraco.functools/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:61.1.2
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
BuildRequires:	python3-jaraco.classes
BuildRequires:	python3-more_itertools
BuildRequires:	python3-pytest >= 3.5
# lint only?
#BuildRequires:	python3-pytest-checkdocs
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 3.2
BuildRequires:	python3-jaraco.tidelift
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Additional functools in the spirit of stdlib's functools.

%description -l pl.UTF-8
Dodatkowe narzędzia funkcyjne w duchu functools z biblioteki
standardowej.

%package apidocs
Summary:	API documentation for Python jaraco.functools module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jaraco.functools
Group:		Documentation

%description apidocs
API documentation for Python jaraco.functools module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jaraco.functools.

%prep
%setup -q -n jaraco_functools-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_flake8 \
%{__python3} -m pytest test_functools.py
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%dir %{py3_sitescriptdir}/jaraco/functools
%{py3_sitescriptdir}/jaraco/functools/*.py
%{py3_sitescriptdir}/jaraco/functools/*.pyi
%{py3_sitescriptdir}/jaraco/functools/__pycache__
%{py3_sitescriptdir}/jaraco/functools/py.typed
%{py3_sitescriptdir}/jaraco.functools-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
