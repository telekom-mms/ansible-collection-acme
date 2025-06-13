#!/usr/bin/env bash

set -eux

ansible-playbook dns-challenge-pebble.yml -vv
ansible-playbook http-challenge-local.yml
ansible-playbook dns-challenge-include-role.yml
ansible-playbook dns-challenge-missing-acme-domain.yml
export ANSIBLE_FILTER_PLUGINS=plugins/filter/
ansible-playbook find-challenge-filter-plugin.yml -vvvv