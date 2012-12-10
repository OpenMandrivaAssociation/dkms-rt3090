%define module rt3090
%define version 2.4.0.4
%define card Ralink RT3090 WiFi cards

%define distname RT3090_LinuxSTA_V%{version}_20101217

Summary: dkms package for %{module} driver
Name: dkms-%{module}
Version: %{version}
Release: %mkrel 1
Source0: http://www.ralinktech.com.tw/data/drivers/%{distname}.tar.bz2
Patch1: dkms-rt3090-use-firmware-in-file.patch
Patch2: dkms-rt3090-unexpected-format.patch
Patch3: dkms-rt3090-config-mk.patch
License: GPLv2+
Group: System/Kernel and hardware
URL: http://www.ralinktech.com/
Requires(preun): dkms
Requires(post): dkms
Suggests: rt3090-firmware
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
This package contains the %{module} driver for
%{card}.

%prep
%setup -q -n %{distname}
%apply_patches

# We don't want to ship firmware here, already provided by separated package
# (rt3090-firmware, see also dkms-rt3090-use-firmware-in-file.patch)
rm -f common/rt2860.bin
rm -rf tools

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/patches
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{module}
PACKAGE_VERSION=%{version}-%{release}

DEST_MODULE_LOCATION[0]=/kernel/3rdparty/%{module}
BUILT_MODULE_NAME[0]=%{module}sta
BUILT_MODULE_LOCATION[0]=os/linux

MAKE[0]="make LINUX_SRC=\$kernel_source_dir HAS_WPA_SUPPLICANT=y HAS_NATIVE_WPA_SUPPLICANT_SUPPORT=y"
AUTOINSTALL="yes"
EOF

tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

mkdir -p %{buildroot}%{_sysconfdir}/Wireless/RT2860STA
install -m 644 RT2860STA.dat %{buildroot}%{_sysconfdir}/Wireless/RT2860STA

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%{_sysconfdir}/Wireless
/usr/src/%{module}-%{version}-%{release}/

%post -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
exit 0

%preun -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
exit 0


%changelog
* Sun Oct 30 2011 Александр Казанцев <kazancas@mandriva.org> 2.4.0.4-1mdv2012.0
+ Revision: 707912
- update to last version 2.4.0.4 from 20111217
- drop dkms-rt3090-fix-rt_ioctl_siwencode-check.patch as fixed in upstream
- drop GFG80211 support due build error in os/linux/config.mk (patch dkms-rt3090-config-mk.patch) in kernel 2.6.38+

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.1.4-2mdv2011.0
+ Revision: 610253
- rebuild

* Thu Mar 11 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.3.1.4-1mdv2010.1
+ Revision: 518051
- update to latest upstream tarball

* Thu Aug 13 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.1.0.0-4mdv2010.0
+ Revision: 416201
- Fixup patch added in previous release.

* Thu Aug 13 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.1.0.0-3mdv2010.0
+ Revision: 416073
- Check if interface is on to switch radio, and turn on radio if enabled
  on interface up.

* Mon Aug 10 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.1.0.0-2mdv2010.0
+ Revision: 414436
- Rename spec file.

* Fri Aug 07 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.1.0.0-1mdv2010.0
+ Revision: 411504
- import dkms-rt3090

