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
declare markup=""
declare -a files=()
while getopts "hH:P:t:m:f:" option; do
	case "$option" in
		h)
			declare -r script_name="$(basename "$0")"
			echo "Usage:"
			echo "  $script_name -h"
			echo "  $script_name [-H HOST] [-P PORT] [-m MARKUP] -t TEXT"
			echo "  $script_name [-H HOST] [-P PORT] [-t TEXT] [-m MARKUP] -f PATH [-f PATH...]"
			echo
			echo "Options:"
			echo "  -h         - show this help message;"
			echo "  -H HOST    - set a host name (default: localhost);"
			echo "  -P PORT    - set a port number (default: 4000);"
			echo "  -t TEXT    - set a message text;"
			echo "  -m MARKUP  - set a message text markup" \
				"(allowed values: Markdown, MarkdownV2, or HTML);"
			echo "  -f PATH    - set a path to a message photo."

			exit 0
			;;
		H) host="$OPTARG";;
		P) port="$OPTARG";;
		t) text="$OPTARG";;
		m) markup="$OPTARG";;
		f) files+=("$OPTARG");;
		?) exit 1;;
	esac
done
if (( port < 1 || port > 65535 )); then
	error "port is incorrect"
fi
if [[
	"$markup" != ""
	&& "$markup" != "Markdown"
	&& "$markup" != "MarkdownV2"
	&& "$markup" != "HTML"
]]; then
	error "markup is incorrect"
fi

if (( ${#files[@]} != 0 )); then
	send "$host" "$port" photo \
		"file=$(realpath "${files[0]}")" "text=$text" "format=$markup"
	exit 0
fi
if [[ "$text" != "" ]]; then
	send "$host" "$port" message "text=$text" "format=$markup"
fi
