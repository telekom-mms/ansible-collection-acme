#!/usr/bin/env bash

set -eux

ansible-playbook dns-challenge-pebble.yml
ansible-playbook dns-challenge-hetzner.yml -e acme_hetzner_auth_token=$HETZNER_AUTH_TOKEN
ansible-playbook http-challenge-local.yml
