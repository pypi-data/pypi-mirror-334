#!/bin/bash
set -e

pushd girder/web
npm ci
npm run build
popd

python .circleci/build_plugins.py plugins/

# Build and publish all Python packages in this repo
readonly PUBLISHED_PYTHON_PACKAGES=(
  .
  plugins/*
  pytest_girder
  clients/python
  worker
)
for directory in "${PUBLISHED_PYTHON_PACKAGES[@]}"; do
    pushd "$directory"
    rm -fr dist
    python -m build
    twine upload --skip-existing dist/*
    popd
done
