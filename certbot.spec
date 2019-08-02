Summary:	Tool to obtain certificates from Let's Encrypt and other ACME compliant CAs
Name:		certbot
Version:	0.36.0
Release:	1
License:	MIT
Group:		Development/Python
Url:		http://certbot.eff.org/
Source0:	https://github.com/certbot/certbot/archive/v%{version}.tar.gz
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-setuptools
BuildRequires:	python-pkg-resources
BuildArch:	noarch
 
%description
Tool to obtain certificates from Let's Encrypt and other ACME compliant CAs
 
%prep
%autosetup -p1
 
%build
python setup.py build
 
%install
python setup.py install -O2 --skip-build --root=%{buildroot} --prefix=%{_prefix}

%files
%{python3_sitelib}/certbot
%{python3_sitelib}/*.egg-info
%{_bindir}/certbot
