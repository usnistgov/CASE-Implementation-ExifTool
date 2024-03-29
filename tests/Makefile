#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

PYTHON3 ?= python3

all: \
  .venv.done.log
	$(MAKE) \
	  --directory govdocs1

.PHONY: \
  check-mypy \
  download

.venv.done.log: \
  $(top_srcdir)/.git_submodule_init.done.log \
  $(top_srcdir)/setup.cfg \
  $(top_srcdir)/setup.py
	rm -rf venv
	$(PYTHON3) -m venv \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv/bin/activate \
	  && pip install \
	    --editable \
	    $(top_srcdir)[testing]
	touch $@

check: \
  check-mypy
	$(MAKE) \
	  --directory govdocs1 \
	  check

check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy \
	    --strict \
	    $(top_srcdir)/case_exiftool \
	    .

clean:
	@rm -f \
	  .venv.done.log
	@rm -rf \
	  .pytest_cache \
	  venv
	@$(MAKE) \
	  --directory govdocs1 \
	  clean

download: \
  .venv.done.log
