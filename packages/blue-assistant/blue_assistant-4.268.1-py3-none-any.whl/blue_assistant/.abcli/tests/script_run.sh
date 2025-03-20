#! /usr/bin/env bash

function test_blue_assistant_script_run() {
    local options=$1
    local list_of_script_name=$(blue_assistant_script_list \
        --delim + \
        --log 0)
    list_of_script_name=$(abcli_option "$options" script $list_of_script_name)

    local script_name
    for script_name in $(echo "$list_of_script_name" | tr + " "); do
        abcli_log "testing $script_name ..."

        abcli_eval ,$options \
            blue_assistant_script_run \
            ~upload,$options \
            script=$script_name \
            test_blue_assistant_script_run-$(abcli_string_timestamp_short) \
            "${@:2}" \
            --test_mode 1 \
            --verbose 1

        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
