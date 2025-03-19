#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gcil -c ./.gitlab-ci.builds.yml -p
gcil -c ./.gitlab-ci.host.yml -p -r
gcil -c ./.gitlab-ci.clone.yml -p
gcil -c ./.gitlab-ci.clone.yml -p -r && exit 1 || true
