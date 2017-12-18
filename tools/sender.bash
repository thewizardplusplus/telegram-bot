#!/usr/bin/env bash

set -o errexit

function error() {
	declare -r message="$1"

	echo "error: $message" 1>&2
	exit 1
}

declare -i port=4000
declare text=""
while getopts "p:t:" option; do
	case "$option" in
		p) port="$OPTARG";;
		t) text="$OPTARG";;
		?) exit 1;;
	esac
done
if (( port < 1 || port > 65535 )); then
	error "port is incorrect"
fi
if [[ "$text" == "" ]]; then
	error "text can't be empty"
fi

echo "port: $port"
echo "text: $text"
