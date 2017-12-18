#!/usr/bin/env bash

function error() {
	declare -r message="$1"

	echo "error: $message" 1>&2
	exit 1
}

declare -i port=4000
declare text=""
while getopts "hp:t:" option; do
	case "$option" in
		h)
			declare -r script_name="$(basename "$0")"
			echo "Usage:"
			echo "  $script_name -h"
			echo "  $script_name [-p PORT] -t TEXT"
			echo
			echo "Options:"
			echo "  -h       - show this help message;"
			echo "  -p PORT  - set a port number (default: 4000);"
			echo "  -t TEXT  - set a message text."

			exit 0
			;;
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

curl --silent --fail --data "text=$text" "http://localhost:$port/api/v1/message"
if [[ $? != 0 ]]; then
	error "request failed"
fi
