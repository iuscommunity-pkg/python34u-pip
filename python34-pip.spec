%global srcname pip

%if %{undefined el6}
%global __python3 /usr/bin/python3.4
%endif

Name:           python34-%{srcname}
Version:        9.0.1
Release:        2%{?dist}
Summary:        A tool for installing and managing Python packages
Group:          Development/Libraries
License:        MIT
URL:            https://pip.pypa.io
Source0:        %pypi_source
BuildArch:      noarch
BuildRequires:  python3-rpm-macros
BuildRequires:  python34-devel
BuildRequires:  python34-setuptools
Requires:       python34-setuptools

# Rename from python36u-pip
Provides:       python34u-pip = %{version}-%{release}
Obsoletes:      python34u-pip < 9.0.1-2


%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%prep
%setup -q -n %{srcname}-%{version}
find %{srcname} -type f -name \*.py -print0 | xargs -0 sed -i -e '1 {/^#!\//d}'


%build
%py3_build


%install
%py3_install
rm %{buildroot}%{_bindir}/pip
%if %{undefined el6}
rm %{buildroot}%{_bindir}/pip3
%endif

mkdir -p %{buildroot}%{bash_completion_dir}

%if %{defined el6}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{buildroot}%{_bindir}/pip3 completion --bash \
    > %{buildroot}%{bash_completion_dir}/pip3
ln -s pip3 %{buildroot}%{bash_completion_dir}/pip%{python3_version}
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 pip3 pip%{python3_version}/" \
    -e s/_pip_completion/_pip3_completion/ \
    %{buildroot}%{bash_completion_dir}/pip3
%else
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{buildroot}%{_bindir}/pip%{python3_version} completion --bash \
    > %{buildroot}%{bash_completion_dir}/pip3
mv %{buildroot}%{bash_completion_dir}/pip{3,%{python3_version}}
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 pip%{python3_version}/" \
    -e s/_pip_completion/_pip%{python3_version_nodots}_completion/ \
    %{buildroot}%{bash_completion_dir}/pip%{python3_version}
%endif


%files
%license LICENSE.txt
%doc README.rst docs
%if %{defined el6}
%{_bindir}/pip3
%endif
%{_bindir}/pip%{python3_version}
%{python3_sitelib}/pip
%{python3_sitelib}/pip-%{version}-py%{python3_version}.egg-info
%dir %{_datadir}/bash-completion
%dir %{bash_completion_dir}
%if %{defined el6}
%{bash_completion_dir}/pip3
%endif
%{bash_completion_dir}/pip%{python3_version}


%changelog
* Sun Sep 22 2019 Carl George <carl@george.computer> - 9.0.1-2
- Rename to python34-pip
- Switch to EPEL python3 macros

* Tue Nov 08 2016 Ben Harper <ben.harper@rackspace.com> - 9.0.1.-1.ius
- Latest upstream

* Mon May 23 2016 Carl George <carl.george@rackspace.com> - 8.1.2-1.ius
- Latest upstream

* Tue May 03 2016 Ben Harper <ben.harper@rackspace.com> - 8.1.1-1.ius
- Upstream 8.1.1
- update Source0 url to pypi.io see
  https://bitbucket.org/pypa/pypi/issues/438/backwards-compatible-un-hashed-package

* Thu Mar 17 2016 Carl George <carl.george@rackspace.com> - 8.1.0-1.ius
- Latest upstream
- Remove build_wheel
- Strip shebangs
- Use %%license when possible
- Macro clean up
- Import bash-completion from Fedora
- Ensure commands are executable

* Fri Jan 22 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.2-1.ius
- Latest upstream

* Fri Jan 22 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.1-2.ius
- correct patch0

* Thu Jan 21 2016 Ben Harper <ben.harper@rackspace.com> - 8.0.1-1.ius
- Latest upstream
- Refresh patch0

* Mon Aug 24 2015 Ben Harper <ben.harper@rackspace.com> - 7.1.2-1.ius
- Latest upstream

* Fri Aug 21 2015 Ben Harper <ben.harper@rackspace.com> - 7.1.1-1.ius
- Latest upstream

* Thu Jul 02 2015 Ben Harper <ben.harper@rackspace.com> - 7.1.0-1.ius
- Latest upstream

* Mon Jun 08 2015 Carl George <carl.george@rackspace.com> - 7.0.3-1.ius
- Latest upstream

* Fri May 22 2015 Carl George <carl.george@rackspace.com> - 7.0.0-1.ius
- Latest upstream
- Refresh patch0

* Tue Apr 07 2015 Carl George <carl.george@rackspace.com> - 6.1.1-1.ius
- Latest upstream
- Refresh patch0

* Thu Feb 05 2015 Ben Harper <ben.harper@rackspace.com> - 6.0.8-1.ius
- Latest sources from upstream

* Thu Jan 29 2015 Carl George <carl.george@rackspace.com> - 6.0.7-1.ius
- Latest upstream

* Mon Jan 05 2015 Carl George <carl.george@rackspace.com> - 6.0.6-1.ius
- Latest upstream

* Fri Dec 26 2014 Carl George <carl.george@rackspace.com> - 6.0.3-1.ius
- Latest upstream
- Refresh patch0

* Wed Aug 13 2014 Carl George <carl.george@rackspace.com> - 1.5.6-3.ius
- Make pip3 a symlink to pip3.4
- Enable wheel

* Tue Aug 12 2014 Carl George <carl.george@rackspace.com> - 1.5.6-2.ius
- Port from Fedora to IUS
- Update Patch0 for latest source

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

