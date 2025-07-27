#!/bin/bash

# Move arquivos já processados para o diretório de arquivos prontos
process() {
    local fname=$(basename "$1")
    local prefix=${fname%.processed.jsonl.gz}
    local ntPath="./nt/${prefix}.nt.fas"

    echo "$ntPath"
    if [[ -f $ntPath ]]; then
        mv "$ntPath" "./done/${prefix}.nt.fas"
    fi
}

export -f process

find ./processed -name '*.processed.jsonl.gz' | rush -j 12 'process {1}'

