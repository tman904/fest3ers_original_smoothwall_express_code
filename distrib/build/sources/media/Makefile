include ../Makefile.versions
include ../Makefile

TARGET_DIR = /build/target/

default: clean smoothwall-$(BASENAME).iso

cdrom:
	@mkdir cdrom
	@mkdir cdrom/images

images: cdrom
	@make -C bootdisktwo
#	@make -C bootdiskone MEDIA=diskone
	@make -C bootdiskone MEDIA=cdrom

cdrom/smoothwall.tgz:
	@mkdir distrib
	@(for I in \
		newt \
		libsmooth+setup \
		newt \
		devnodes \
		glibc \
		libstdc++ \
		libgcc \
		binutils \
		coreutils \
		iana-etc \
		mktemp \
		findutils \
		iana-etc \
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
		util-linux \
		joe \
		wget \
		iptables \
		pciutils \
		kernel \
		lilo \
		openssl \
		openssh \
		apache \
		squid \
		HTML-Parser \
		HTML-Tagset \
		URI \
		libwww-perl \
		strace \
		rrdtool \
		cron \
		tcpdump \
		traceroute \
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
		dhcp \
		snort \
		openswan \
		coretree \
	; do \
		if [ ! -e /$(TARGET_DIR)/smoothwall-$$I-*.tar.gz ]; then \
		make -C ../$$I clean all; \
			if [ $$? -ne 0 ]; then \
				echo "$$I FAILED"; \
				exit 0; \
			fi; \
		fi; \
		echo "Unpacking $$I ..."; \
		tar -zxf /$(TARGET_DIR)/smoothwall-$$I-*.tar.gz -C distrib; \
	done; \
	);

	@/build/striptree distrib

	@echo "PRODUCT='$(PRODUCT_NAME)'" > distrib/var/smoothwall/main/productdata
	@echo "VERSION='$(PRODUCT_VERSION)'" >> distrib/var/smoothwall/main/productdata
	@echo "REVISION='$(REVISION)'" >> distrib/var/smoothwall/main/productdata
	@echo "UI_VERSION='$(UI_VERSION)'" >> distrib/var/smoothwall/main/productdata
	@echo "FIXES='$(FIXES_NUMBER)'" >> distrib/var/smoothwall/main/productdata

	@chown nobody:nobody distrib/var/smoothwall/main/productdata

	@echo "Securing tree ..."
	@/build/securetree distrib
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

smoothwall-$(BASENAME).iso: images cdrom/smoothwall.tgz extracontent
	@/sbin/mkisofs -o $(TARGET_DIR)/isos/smoothwall-$(BASENAME).iso -J -c boot.cat \
		-b images/$(BASENAME)-bootcdrom.img -V $(BASENAME) cdrom
	@echo "smoothwall-$(BASENAME).iso build complete"

clean:
	@rm -rf cdrom distrib

	@make -C bootdisktwo clean
	@make -C bootdiskone MEDIA=diskone clean
	@make -C bootdiskone MEIDA=cdrom clean
	
download:
	@true
