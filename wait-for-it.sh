#!/usr/bin/env bash

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  sleep 1
  echo "Still waiting for $host:$port..."
done

echo "$host:$port is available. Running command: $cmd"
exec $cmd