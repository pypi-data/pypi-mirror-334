#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Prepare paths
mkdir -p ~/.ssh

# Run tests
gcil
gcil -p
gcil '1' && exit 1 || true
gcil 'Job 1'
gcil 'Job 9'
gcil -p local_first
gcil -n bridge 'Job 2' || (type podman >/dev/null 2>&1 && echo 'Podman engine: Network bridge may fail in GitLab CI containers')
CI_LOCAL_NETWORK='bridge' gcil 'Job 2' || (type podman >/dev/null 2>&1 && echo 'Podman engine: Network bridge may fail in GitLab CI containers')
gcil -n host 'Job 2'
CI_LOCAL_NETWORK='host' gcil 'Job 2'
gcil -n none 'Job 2'
CI_LOCAL_NETWORK='none' gcil 'Job 2'
gcil 'Job 10'
gcil --host 'Job 10'
gcil -c ./.gitlab-ci.deprecated.yml -p
gcil -c ./.gitlab-ci.paths.yml -p
gcil -c ./.gitlab-ci.paths.yml --real-paths -p
gcil -c ./.gitlab-ci.paths.yml --random-paths -p
gcil -c ./.gitlab-ci.paths.yml --real-paths --random-paths -p
