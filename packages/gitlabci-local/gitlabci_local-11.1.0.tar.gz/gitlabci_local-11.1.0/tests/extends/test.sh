#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gcil -H -p
gcil -c ./.gitlab-ci.incomplete.yml -H 'Job 1'
gcil -c ./.gitlab-ci.incomplete.yml -H 'Job 2'
gcil -c ./.gitlab-ci.incomplete.yml -H 'Job 3' && exit 1 || true
gcil -c ./.gitlab-ci.partial.yml -H -p
gcil -c ./.gitlab-ci.partial.yml -H 'Job 3' && exit 1 || true
gcil -c ./.gitlab-ci.partial.yml -H 'Job 4' && exit 1 || true
gcil -c ./.gitlab-ci.stages.yml -H -p
