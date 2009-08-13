%define module rt3090
%define version 2.1.0.0
%define card Ralink RT3090 WiFi cards

%define distname 2009_0612_RT3090_Linux_STA_V%{version}_DPO

Summary: dkms package for %{module} driver
Name: dkms-%{module}
Version: %{version}
Release: %mkrel 4
Source0: http://www.ralinktech.com.tw/data/drivers/%{distname}.tar.gz
Source1: dkms-rt3090-net_device_ops.patch
Patch0: dkms-rt3090-Makefile.patch
Patch1: dkms-rt3090-use-firmware-in-file.patch
Patch2: dkms-rt3090-fix-rt_ioctl_siwencode-check.patch
Patch3: dkms-rt3090-return-value-with-void.patch
Patch4: dkms-rt3090-unexpected-format.patch
Patch5: dkms-rt3090-radio-switch.patch
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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
PATCH[0]="dkms-rt3090-net_device_ops.patch"
PATCH_MATCH[0]="^2\.6\.(3[1-9])|([4-9][0-9]+)|([1-9][0-9][0-9]+)"
EOF

tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

mkdir -p %{buildroot}%{_sysconfdir}/Wireless/RT2860STA
install -m 644 RT2860STA.dat %{buildroot}%{_sysconfdir}/Wireless/RT2860STA

cp %{_sourcedir}/dkms-rt3090-net_device_ops.patch \
   %{buildroot}/usr/src/%{module}-%{version}-%{release}/patches

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
