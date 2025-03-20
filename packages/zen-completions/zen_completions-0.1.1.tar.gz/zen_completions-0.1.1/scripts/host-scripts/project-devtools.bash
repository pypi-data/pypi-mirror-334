#!/bin/bash

#------------------------------------------------------------
# Source devtools scripts
#------------------------------------------------------------
zf_devtools_dir_local=${ZF_DEVTOOLS_DIR:-"/nonexistent/zenafide/devtools"}

# Order of sourcing matters
source "${zf_devtools_dir_local}/scripts/host-scripts/shell-utils.bash"
source "${zf_devtools_dir_local}/scripts/host-scripts/aws.bash"
source "${zf_devtools_dir_local}/scripts/host-scripts/docker.bash"

#------------------------------------------------------------
# Set project level env vars
#------------------------------------------------------------
source "${zf_devtools_dir_local}/scripts/host-scripts/project-envvar-defaults.bash"

echo "[project-devtools] Setting project-level env vars"
export PROJECT_ROOT=${PROJECT_ROOT:-$(pwd)}

echo "[project-devtools] Setting docker variables: project image"
export DOCKER_PROJ_REPO_NAME=${DOCKER_PROJ_REPO_NAME:-"zenafide/zen-completions"}
export DOCKER_PROJ_IMAGE_BASE_NAME="${DOCKER_REGISTRY}/${DOCKER_PROJ_REPO_NAME}"
export DOCKER_PROJ_IMAGE_TAG="${DOCKER_PROJ_IMAGE_BASE_NAME}:${BUILD_VERSION}"

# source dotenv files as well so we don't need to do it manually
if [[ -f "./.env" ]]; then
  source-dotenv-file-on-host "./.env"
fi 