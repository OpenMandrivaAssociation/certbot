Summary:	Tool to obtain certificates from Let's Encrypt and other ACME compliant CAs
Name:		certbot
Version:	2.1.1
Release:	3
License:	MIT
Group:		Development/Python
Url:		http://certbot.eff.org/
Source0:	https://github.com/certbot/certbot/archive/v%{version}.tar.gz
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python-pkg-resources
BuildArch:	noarch

%description
Tool to obtain certificates from Let's Encrypt and other ACME compliant CAs

%global subprojects acme certbot certbot-apache certbot-ci certbot-compatibility-test certbot-dns-cloudflare certbot-dns-digitalocean certbot-dns-dnsimple certbot-dns-dnsmadeeasy certbot-dns-gehirn certbot-dns-google certbot-dns-linode certbot-dns-luadns certbot-dns-nsone certbot-dns-ovh certbot-dns-rfc2136 certbot-dns-route53 certbot-dns-sakuracloud certbot-nginx letstest

%global dnsservices cloudflare digitalocean dnsimple dnsmadeeasy gehirn google linode luadns nsone ovh rfc2136 route53 sakuracloud
%(for i in %{dnsservices}; do
cat <<EOF
%package dns-$i
Summary:	Library for Let's Encrypt DNS authentication with the $i DNS
Requires:	%{name} = %{EVRD}

%description dns-$i
Library for Let's Encrypt DNS authentication with the $i DNS

%files dns-$i
%{python3_sitelib}/certbot_dns_$i
%{python3_sitelib}/certbot_dns_$i-*-info
EOF
done)
 
%package test
Summary:	Tests for the certbot Let's Encrypt client
Requires:	%{name} = %{EVRD}

%description test
Tests for the certbot Let's Encrypt client

%files test
%{_bindir}/certbot_test
%{python3_sitelib}/certbot_integration_tests
%{python3_sitelib}/certbot_ci-*-info
%{_bindir}/letstest
%{python3_sitelib}/letstest
%{python3_sitelib}/letstest-*-info
 
%prep
%autosetup -p1
# Indent nginx.conf entries with tabs to match our system defaults
sed -i -e 's,\\n        ,\\n		,g;s,\\n    ,\\n	,g' certbot-nginx/certbot_nginx/_internal/configurator.py

%build
for i in %{subprojects}; do
	cd $i
	%py_build
	cd ..
done
 
%install
for i in %{subprojects}; do
	cd $i
	%py_install
	cd ..
done

# We're neither BrokenBuntu nor that other broken OS
rm -rf %{buildroot}%{python3_sitelib}/{snap,windows_installer}_integration_tests

# Let's own the log directories we'd otherwise create on first run
mkdir -p %{buildroot}%{_localstatedir}/log/letsencrypt
touch %{buildroot}%{_localstatedir}/log/letsencrypt/letsencrypt.log
touch %{buildroot}%{_localstatedir}/log/letsencrypt/letsencrypt.log.1

%files
%{_bindir}/certbot
%{_bindir}/certbot-compatibility-test
%{_bindir}/run_acme_server
%{python3_sitelib}/certbot
%{python3_sitelib}/acme
%{python3_sitelib}/certbot_apache
%{python3_sitelib}/certbot_compatibility_test
%{python3_sitelib}/certbot_nginx
%{python3_sitelib}/certbot-*-info
%{python3_sitelib}/acme-*-info
%{python3_sitelib}/certbot_apache-*-info
%{python3_sitelib}/certbot_compatibility_test-*-info
%{python3_sitelib}/certbot_nginx-*-info
%dir %{_localstatedir}/log/letsencrypt
%ghost %{_localstatedir}/log/letsencrypt/letsencrypt.log
%ghost %{_localstatedir}/log/letsencrypt/letsencrypt.log.1
