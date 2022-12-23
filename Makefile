SHELL := /bin/bash
.DEFAULT_GOAL := dev

TOPTARGETS := production test clean setup

SUBDIRS := client server

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

dev:
	(trap 'kill 0' SIGINT; $(MAKE) -C client dev & $(MAKE) -C server dev & wait)

install:
	mkdir -p ~/.config/systemd/user/
	cp superstonk_mod_website.service ~/.config/systemd/user/
	systemctl --user daemon-reload
	systemctl --user enable superstonk_mod_website.service
	systemctl --user start superstonk_mod_website.service
	loginctl enable-linger

.PHONY: $(TOPTARGETS) $(SUBDIRS) force_pull bot install
