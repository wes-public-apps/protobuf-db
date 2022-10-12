# Compiling Protobufs
1. navigate to the tests directory
2. verify protoc version is >= 3.19.0
3. run the following command: protoc --proto_path=$(pwd)/protobuf_definitions --python_out=$(pwd) $(pwd)/protobuf_definitions/*.proto

# Installing Newest Protoc
1. the linux apt repository is very outdated
2. follow instructions outlined here https://grpc.io/docs/protoc-installation/#install-pre-compiled-binaries-any-os
3. instead of installing to $HOME/.local unzip to /usr/local/
4. chown /usr/local/bin/protoc to be your user so you do not need sudo