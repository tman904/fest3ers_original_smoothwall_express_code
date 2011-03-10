# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions
include ../Makefile

TARGET_DIR = /build/target/

cdrom:
	@mkdir cdrom

images: cdrom
	@make -C booting

cdrom/smoothwall.tgz:
	@mkdir distrib

	@(for I in \
		glibc \
		libsmooth+setup \
		newt \
		slang \
		devnodes \
		libstdc++ \
		libgcc \
		binutils \
		coreutils \
		iana-etc \
		mktemp \
		findutils \
		gawk \
		ncurses \
		vim \
		less \
		sed \
		flex \
		gettext \
		net-tools \
		inetutils \
		iputils \
		whois \
		perl \
		bash \
		bzip2 \
		kbd \
		e2fsprogs \
		parted \
		grep \
		gzip \
		module-init-tools \
		procinfo \
		procps \
		psmisc \
		shadow \
		sysklogd \
		logrotate \
		sysvinit \
		tar \
		cpio \
		util-linux \
		joe \
		wget \
		iptables \
		xtables-addons \
		ipbatch \
		pciutils \
		kernel-runtime \
		ueagle-data \
		grub \
		openssl \
		openssh \
		httpd \
		smoothd \
		squid \
		HTML-Parser \
		HTML-Tagset \
		URI \
		libwww-perl \
		strace \
		libart_lgpl \
		freetype \
		rrdtool \
		cron \
		tcpdump \
		dnsmasq \
		libcap \
		ntp \
		openntpd \
		hdparm \
		hddtemp \
		iproute2 \
		libpng \
		gd \
		gmp \
		expat \
		ethtool \
		popt \
		listtables \
		beep2 \
		pcre \
		trafficstats \
		iftop \
		setuids \
		ppp \
		isdn4k-utils \
		speedtouch \
		rp-pppoe \
		ibod \
		dhcpcd \
		eciadsl-synch_bin \
		eciadsl-usermode \
		eagle-usb \
		cnxadsl \
		dhcp \
		snort \
		oinkmaster \
		openswan \
		wireless_tools \
		sqlite \
		imspector \
		diffutils \
		traceroute \
		clamav \
		p3scan \
		libosip2 \
		siproxd \
		which \
		miniupnpd \
		ez-ipupdate \
		noip \
		basicrootfs \
		coretree \
	; do \
		if [ ! -e /$(TARGET_DIR)/smoothwall-$$I.tar.gz ]; then \
		make -C ../$$I clean all; \
			if [ $$? -ne 0 ]; then \
				echo "$$I FAILED"; \
				exit 0; \
			fi; \
		fi; \
		echo "Unpacking $$I ..."; \
		tar -zxf /$(TARGET_DIR)/smoothwall-$$I.tar.gz -C distrib; \
	done; \
	);

ifeq ($(TYPE), -devel)
	@(for I in \
		kernel-headers \
		patch \
		make \
		autoconf \
		automake \
		bison \
		dejagnu \
		gcc \
		gdb \
		tcl \
		m4 \
		neon \
		apr \
		apr-util \
		subversion \
		git \
		screen \
		lynx \
		groff \
		man \
		man-pages \
	; do \
		if [ ! -e /$(TARGET_DIR)/smoothwall-$$I.tar.gz ]; then \
		make -C ../$$I clean all; \
			if [ $$? -ne 0 ]; then \
				echo "$$I FAILED"; \
				exit 0; \
			fi; \
		fi; \
		echo "Unpacking $$I ..."; \
		tar -zxf /$(TARGET_DIR)/smoothwall-$$I.tar.gz -C distrib; \
	done; \
	);
endif

ifneq ($(TYPE), -devel)
	@/build/striptree distrib
endif

	@echo "PRODUCT='$(PRODUCT_NAME)'" > distrib/var/smoothwall/main/productdata
	@echo "VERSION='$(PRODUCT_VERSION)'" >> distrib/var/smoothwall/main/productdata
	@echo "REVISION='$(REVISION)'" >> distrib/var/smoothwall/main/productdata
	@echo "UI_VERSION='$(UI_VERSION)'" >> distrib/var/smoothwall/main/productdata
	@echo "FIXES='$(FIXES_NUMBER)'" >> distrib/var/smoothwall/main/productdata
	@echo "ARCH='$(ARCH)'" >> distrib/var/smoothwall/main/productdata

	@chown nobody:nobody distrib/var/smoothwall/main/productdata

	@echo "Securing tree ..."
	@/build/securetree distrib
	@chmod u+s distrib/bin/traceroute
	@chmod u+s distrib/usr/bin/ping
	@chmod u+s distrib/usr/sbin/listtables
	@chown root:nobody distrib/usr/bin/setuids/*
	@chmod 4750 distrib/usr/bin/setuids/*
	
	@echo "Converting to shadow passwords ..."
	@/usr/bin/chroot distrib /usr/sbin/pwconv
	@/usr/bin/chroot distrib /usr/sbin/grpconv
	
	@echo "Updating library cache ..."
	@/sbin/ldconfig -r distrib

	@echo "Building smoothwall.tgz, stand by ..."
	@tar -zcf cdrom/smoothwall.tgz -C distrib .

extracontent: cdrom
	@cp extracontent/* cdrom -avR
	@(for I in README.txt README.html; do \
		cat templates/$$I | \
			sed "s@\%PRODUCT_NAME\%@$(PRODUCT_NAME)@g" | \
			sed "s@\%BASENAME\%@$(BASENAME)@g" \
		> cdrom/$$I; \
	done);
	@(cd cdrom; rm -rf `find -name CVS`)
	@(cd cdrom; rm -rf `find -name .svn`)

all: images cdrom/smoothwall.tgz extracontent
	@cp -avR booting/isolinux/ cdrom/
	@/sbin/mkisofs -o $(TARGET_DIR)/isos/smoothwall-$(BASENAME)$(PRODUCT_EXTRA)$(TYPE)-$(ARCH).iso -J -c boot.cat \
		-b isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -boot-info-table -V $(BASENAME) cdrom
	@echo "smoothwall-$(BASENAME)$(PRODUCT_EXTRA)$(TYPE)-$(ARCH).iso build complete"

clean:
	@rm -rf cdrom distrib

	@make -C booting clean
	
download:
	@true
