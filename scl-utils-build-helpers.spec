# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_of_Additional_RPM_Macros
%global macrosdir       %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global rrcdir          %_libexecdir

Name:           scl-utils-build-helpers
Version:        0
Release:        5%{?dist}
Summary:        RPM macros and scripts for SCL maintainers

BuildArch:      noarch

License:        LGPLv2+
URL:            https://github.com/sclorg/scl-utils-build-helpers

Source0:        README
Source1:        COPYING
Source100:      scl-helper-wrap-bin.sh
Source101:      macros.scl-build-helpers

Requires:       scl-utils-build


%description
Several RPM macros and convenience scripts to make the maintenance of packages
for Software Collections easier.  The aim is to move as much duplicated code as
possible into one (dedicated) place.


%prep
%setup -c -T


%build


%install
# definitions
%global wrap_script %rrcdir/%(basename %SOURCE100)
%global macros %macrosdir/%(basename %SOURCE101)
substitutions=(
    -e 's|@SCRIPT_WRAP@|%wrap_script|g'
    -e 's|@MACROS@|%macros|g'
    -e 's|@GENERATOR@|%name-%version-%release|g'
)

# installation
install -p -m 644 %SOURCE0 .
install -p -m 644 %SOURCE1 .
mkdir -p %buildroot%rrcdir
mkdir -p %buildroot%macrosdir
sed "${substitutions[@]}" %{SOURCE100} > %buildroot%wrap_script
sed "${substitutions[@]}" %{SOURCE101} > %buildroot%macros


%files
%doc README COPYING
%attr(755,-,-) %wrap_script
%macros


%changelog
* Wed Jun 21 2017 Pavel Raiskup <praiskup@redhat.com> - 0-5
- add metapackage macros and fix some wording

* Mon Jun 19 2017 Pavel Raiskup <praiskup@redhat.com> - 0-4
- bugfixes, don't install wrapper for the directory itself, fix one-hit macro

* Mon Jun 19 2017 Pavel Raiskup <praiskup@redhat.com> - 0-2
- more automation macros

* Fri Jun 16 2017 Pavel Raiskup <praiskup@redhat.com> - 0-1
- add license

* Fri Jun 16 2017 Pavel Raiskup <praiskup@redhat.com> - 0-0
- initial version
