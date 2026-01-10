#!/usr/bin/env bash

set -xe

process_file() {
    local fasta="$1"
    local fname=$(basename "$fasta")
    local prefix=${fname%.nt.fas}
    local tree="./nwk/${prefix}.nwk"

    if [[ -f "$tree" ]]; then
        echo "Processando $prefix"
        trimal -maxidentity 0.95 -in "./nt/${prefix}.nt.fas" -out "./nt_filtered/${prefix}.nt.filtered.fas"
        gotree prune -r -f <(seqkit fx2tab -ni "./nt_filtered/${prefix}.nt.filtered.fas") \
            -i "$tree" > "./nwk_filtered/${prefix}.filtered.nwk"
        seqkit grep -f <(gotree labels -i "./nwk_filtered/${prefix}.filtered.nwk") \
            "./nt_filtered/${prefix}.nt.filtered.fas" > "./nt_tree_filtered/${prefix}.nt.filtered.fas"
        hyphy fubar \
            --code $(./get_code.py "./nt_tree_filtered/${prefix}.nt.filtered.fas") \
            --alignment "./nt_tree_filtered/${prefix}.nt.filtered.fas" \
            --tree "./nwk_filtered/${prefix}.filtered.nwk" \
            --output "./output/${prefix}.filtered.fubar.json" \
            > ./err/hyphy_errors_$prefix.log.txt 2>&1
        rm "./nt_tree_filtered/${prefix}.nt.filtered.fas.FUBAR.cache" 2>/dev/null
    else
        echo "${prefix}.nt" >> ./err/missing_trees.txt
    fi
}

export -f process_file

mkdir -p nt_filtered nwk_filtered nt_tree_filtered output

ls ./nt/*.fas | rush -j 1 'process_file {1}'
