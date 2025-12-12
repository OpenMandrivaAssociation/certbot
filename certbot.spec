Summary:	Tool to obtain certificates from Let's Encrypt and other ACME compliant CAs
Name:		certbot
Version:	3.3.0
Release:	2
License:	MIT
Group:		Development/Python
Url:		https://certbot.eff.org/
Source0:	https://github.com/certbot/certbot/archive/v%{version}.tar.gz
Source10:	https://src.fedoraproject.org/rpms/certbot/raw/rawhide/f/certbot-renew-systemd.service
Source11:	https://src.fedoraproject.org/rpms/certbot/raw/rawhide/f/certbot-renew-systemd.timer
Source12:	https://src.fedoraproject.org/rpms/certbot/raw/rawhide/f/certbot-sysconfig-certbot
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

# Systemd integration
install -Dm 0644 --preserve-timestamps %{SOURCE10} %{buildroot}%{_unitdir}/certbot-renew.service
install -Dm 0644 --preserve-timestamps %{SOURCE11} %{buildroot}%{_unitdir}/certbot-renew.timer
install -Dm 0644 --preserve-timestamps %{SOURCE12} %{buildroot}%{_sysconfdir}/sysconfig/certbot

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
%{_unitdir}/certbot-renew.service
%{_unitdir}/certbot-renew.timer
%config(noreplace) %{_sysconfdir}/sysconfig/certbot
%dir %{_localstatedir}/log/letsencrypt
%ghost %{_localstatedir}/log/letsencrypt/letsencrypt.log
%ghost %{_localstatedir}/log/letsencrypt/letsencrypt.log.1
