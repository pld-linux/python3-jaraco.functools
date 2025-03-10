#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (fail for python2 because of top jaraco module local vs system location mismatch)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Functools like those found in stdlib
Summary(pl.UTF-8):	Functools podobne do tych z biblioteki standardowej
Name:		python-jaraco.functools
# keep 2.x here for python2 support
Version:	2.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco.functools/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco.functools/jaraco.functools-%{version}.tar.gz
# Source0-md5:	c245ade3e753bc556415f1fec102f232
URL:		https://pypi.org/project/jaraco.functools/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:31.0.1
BuildRequires:	python-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python-backports.functools_lru_cache >= 1.0.3
BuildRequires:	python-backports.unittest_mock
BuildRequires:	python-jaraco.classes
BuildRequires:	python-more_itertools
BuildRequires:	python-pytest >= 3.5
# lint only?
#BuildRequires:	python-pytest-checkdocs
BuildRequires:	python-pytest-flake8
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python3-jaraco.classes
BuildRequires:	python3-more_itertools
BuildRequires:	python3-pytest >= 3.5
# lint only?
#BuildRequires:	python3-pytest-checkdocs
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-jaraco.packaging >= 3.2
BuildRequires:	python-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-jaraco
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Additional functools in the spirit of stdlib's functools.

%description -l pl.UTF-8
Dodatkowe narzędzia funkcyjne w duchu functools z biblioteki
standardowej.

%package -n python3-jaraco.functools
Summary:	Functools like those found in stdlib
Summary(pl.UTF-8):	Functools podobne do tych z biblioteki standardowej
Group:		Libraries/Python
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.5

%description -n python3-jaraco.functools
Additional functools in the spirit of stdlib's functools.

%description -n python3-jaraco.functools -l pl.UTF-8
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
%setup -q -n jaraco.functools-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=backports.unittest_mock,pytest_flake8 \
%{__python} -m pytest test_functools.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_flake8 \
%{__python3} -m pytest test_functools.py
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# these belong to python-jaraco common package
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/jaraco/__init__.py*

%py_postclean
%endif

%if %{with python3}
%py3_install

# these belong to python3-jaraco common package
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__init__.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__pycache__/__init__.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/jaraco/functools.py[co]
%{py_sitescriptdir}/jaraco.functools-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jaraco.functools
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/jaraco/functools.py
%{py3_sitescriptdir}/jaraco/__pycache__/functools.cpython-*.py[co]
%{py3_sitescriptdir}/jaraco.functools-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
