#!/bin/bash
set -e
uv lock --no-upgrade
git add uv.lock
