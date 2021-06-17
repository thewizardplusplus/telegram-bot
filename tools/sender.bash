#!/usr/bin/env bash

function error() {
	declare -r message="$1"

	echo "error: $message" 1>&2
	exit 1
}

function send() {
	declare -r host="$1"
	declare -r port="$2"
	declare -r endpoint="$3"

	declare -a data=()
	shift 3; for argument in "$@"; do
		if [[ !("$argument" =~ =$) ]]; then
			data+=(--data-urlencode "$argument")
		fi
	done

	curl \
		--silent \
		--fail \
		--header "Content-Type: application/x-www-form-urlencoded" \
		"${data[@]}" \
		"$host:$port/api/v1/$endpoint"
	if [[ $? != 0 ]]; then
		error "request failed"
	fi
}

declare host="localhost"
declare -i port=4000
declare text=""
declare file=""
while getopts "hH:P:t:f:" option; do
	case "$option" in
		h)
			declare -r script_name="$(basename "$0")"
			echo "Usage:"
			echo "  $script_name -h"
			echo "  $script_name [-H HOST] [-P PORT] -t TEXT"
			echo "  $script_name [-H HOST] [-P PORT] [-t TEXT] -f PATH"
			echo
			echo "Options:"
			echo "  -h       - show this help message;"
			echo "  -H HOST  - set a host name (default: localhost);"
			echo "  -P PORT  - set a port number (default: 4000);"
			echo "  -t TEXT  - set a message text;"
			echo "  -f PATH  - set a path to a message photo."

			exit 0
			;;
		H) host="$OPTARG";;
		P) port="$OPTARG";;
		t) text="$OPTARG";;
		f) file="$OPTARG";;
		?) exit 1;;
	esac
done
if (( port < 1 || port > 65535 )); then
	error "port is incorrect"
fi

if [[ "$file" != "" ]]; then
	send "$host" "$port" photo "file=$(realpath "$file")" "text=$text"
	exit 0
fi
if [[ "$text" != "" ]]; then
	send "$host" "$port" message "text=$text"
fi
