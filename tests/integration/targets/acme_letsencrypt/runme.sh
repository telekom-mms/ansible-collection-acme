#!/usr/bin/env bash

set -eux

ansible-playbook dns-challenge-pebble.yml
ansible-playbook http-challenge-local.yml
ansible-playbook dns-challenge-include-role.yml
ansible-playbook dns-challenge-missing-acme-domain.yml
ANSIBLE_FILTER_PLUGINS=../../../roles/acme/filter_plugins ansible-playbook find-challenge-filter-plugin.yml