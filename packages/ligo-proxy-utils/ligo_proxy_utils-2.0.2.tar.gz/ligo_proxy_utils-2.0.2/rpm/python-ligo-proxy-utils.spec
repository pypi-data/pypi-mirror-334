%global srcname ligo-proxy-utils
%global distname %{lua:name = string.gsub(rpm.expand("%{srcname}"), "[.-]", "_"); print(name)}
%global version 2.0.2
%global release 1

Name:    python-%{srcname}
Version: %{version}
Release: %{release}%{?dist}
Summary: Utilities for obtaining short-lived proxy certificates for LIGO

Source0: %pypi_source %distname

License: GPLv3+
Packager: Duncan Macleod <duncan.macleod@ligo.org>
Url: https://git.ligo.org/computing/iam/ligo-proxy-utils

BuildArch: noarch
Prefix: %{_prefix}

# -- build requirements

BuildRequires: python3-devel
BuildRequires: python3dist(argparse-manpage)
BuildRequires: python3dist(ciecplib)
BuildRequires: python3dist(pip)
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(wheel)

# -- packages

%global _description %{expand:
Utilities for generating short-lived LIGO Credentials.
}

%description %_description

# python3-ligo-proxy-utils
%package -n python3-%{srcname}
Summary: Python %{python3_version} modules for %{srcname}
%description -n python3-%{srcname}
%_description
This package provides the %{python3_version} library.
%files -n python3-%{srcname}
%doc README.md
%license COPYING
%{python3_sitelib}

# ligo-proxy-utils
%package -n %{srcname}
Summary: Command-line interfaces for %{srcname}
Requires: python3-%{srcname} = %{version}-%{release}
%description -n %{srcname}
%_description
This package provides the command-line interface scripts.
%files -n %{srcname}
%license COPYING
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*.1*

# -- build

%prep
%autosetup -n %{distname}-%{version}

%if 0%{?rhel} && 0%{?rhel} < 10
echo "Writing setup.cfg for setuptools %{setuptools_version}"
# hack together setup.cfg for old setuptools to parse
cat > setup.cfg << SETUP_CFG
[metadata]
name = %{srcname}
version = %{version}
author-email = %{packager}
description = %{summary}
license = %{license}
license_files = LICENSE
url = %{url}
[options]
packages = find:
python_requires = >=3.6
install_requires =
  ciecplib
[options.entry_points]
console_scripts =
  ligo-proxy-init = ligo_proxy_utils.ligo_proxy_init:ligo_proxy_init
[build_manpages]
manpages =
  man/ligo-proxy-init.1:function=create_parser:module=ligo_proxy_utils.ligo_proxy_init
SETUP_CFG
%endif

%if %{undefined pyproject_wheel}
echo "Writing setup.py for py3_build_wheel"
# write a setup.py to be called explicitly
cat > setup.py << SETUP_PY
from setuptools import setup
setup()
SETUP_PY
%endif

%build
# build a wheel
%if %{defined pyproject_wheel}
%pyproject_wheel
%else
%py3_build_wheel
%endif
# generate manuals
%python3 -c "from setuptools import setup; setup()" \
  --command-packages=build_manpages \
  build_manpages \
;

%install
# install the wheel
%if %{defined pyproject_wheel}
%pyproject_install
%else
%py3_install_wheel %{distname}-%{version}-*.whl
%endif
# install the manuals
%__mkdir -p -v %{buildroot}%{_mandir}/man1
%__install -m 644 -p -v man/*.1* %{buildroot}%{_mandir}/man1/

%check
export PATH="%{buildroot}%{_bindir}:${PATH}"
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
# run the unit tests
%pytest --pyargs ligo_proxy_utils.tests
# test basic executable functionality
ligo-proxy-init -h
ligo-proxy-init -v

# -- changelog

%changelog
* Tue Mar 18 2025 Duncan Macleod <duncan.macleod@ligo.org> - 2.0.2-1
- Release 2.0.2-1

* Mon Jun 10 2024 Duncan Macleod <duncan.macleod@ligo.org> - 2.0.1-1
- Move all metadata to pyproject.toml
- Use pyproject macros to build, if available, hack together setuptools files if not

* Wed Jan 27 2021 Duncan Macleod <duncan.macleod@ligo.org> - 2.0.0-1
- rewrite in python

* Thu Dec 03 2020 Satya Mohapatra <patra@mit.edu> - 1.3.6-1
- kagra access
* Mon Dec 17 2018 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.5-1
- Use 2048 bits for RFC 3820 compliant impersonation proxy
* Wed Nov 28 2018 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.4-1
- Use addressbook.ligo.org to verify uid instead of ldap.ligo.org
* Wed Apr 12 2017 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.3-1
- Remove shred and store intermediate files in /dev/shm if available
* Fri Dec 02 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.2-1
- Add option to specify certificate lifetime which now defaults to 11.5 days
* Tue Nov 22 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.1-1
- Add option to create RFC 3820 compliant impersonation proxy
* Mon Aug 01 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.0-1
- Remove LDAP user check
- Use "rm -P" to safely delete files on Mac OS X
* Mon Jun 13 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.5-1
- Allow Virgo members to use ligo-proxy-init
- Print LDAP lookup warning only in debug mode
* Wed Feb 17 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.4-1
- Perform LDAP lookup check on port 80
- Continue script if LDAP lookup check fails to run
* Thu Nov 05 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.3-1
- Fixed bugs in Kerberos support
- Modified user validity check to use unencrypted connection
* Thu Oct 15 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.2-1
- Modified group check to only whitelist LSC and LIGOLab
- Fixed invalid password warning
- Added explicit Kerberos support
- Added destroy option
* Mon Jul 20 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.1-1
- Added automatic failover for LIGO IdP servers
* Fri Jun 06 2014 Adam Mercer <adam.mercer@ligo.org) - 1.0.1-1
- Curl now asks for password directly
- Clears (DY)LD_LIBRARY_PATH environment variables
- Explicitly sets umask
- Checks user is not Virgo member
- Minor bugfixes
* Fri Feb 22 2013 Scott Koranda <scott.koranda@ligo.org> - 1.0.0-1
- Initial version.
