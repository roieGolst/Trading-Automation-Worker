#!/bin/bash

cd "$(dirname "$0")/.." || {
  echo "Failed to navigate to the project root"
  exit 1
}

cd app/networkLayer/dataSource/grpc || {
  echo "Failed to navigate to app/service/networkService/dataSource/rpcService"
  exit 1
}

mkdir "dist"

poetry run python -m grpc_tools.protoc \
  -I proto/ \
  --python_out=dist/ \
  --grpc_python_out=dist/ \
  --mypy_out=dist/ \
  ./proto/*.proto

protol \
  --create-package \
  --in-place \
  --python-out dist/ \
  protoc --proto-path=proto/ myService.proto types.proto