#!/usr/bin/env bash

set -eux

ansible-playbook find-challenge-filter-plugin.yml

ansible-playbook http-challenge-local.yml

ansible-playbook dns-challenge-pebble.yml
ansible-playbook dns-challenge-include-role.yml
ansible-playbook dns-challenge-missing-acme-domain.yml
