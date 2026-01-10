from torch import amp
from evo2 import Evo2
from langchain.text_splitter import CharacterTextSplitter

import numpy as np
import pandas as pd
from datasets import load_dataset
from Bio.Seq import Seq
import torch
import gc

torch.cuda.empty_cache()
gc.collect()

def get_evo():
    torch.cuda.empty_cache()
    gc.collect()

    model = Evo2('evo2_7b_base')
    model.model = model.model.eval().to(torch.float32)
    return model

class CFG:
    LAYER = 'blocks.26.mlp.l3'
    CHUNK_SIZE = 8192
    CHUNK_OVERLAP = int(np.ceil(CHUNK_SIZE / 2))
    EMBEDDING_DIM = 4096
    MODEL = get_evo()

def forward_and_reverse(embedder_fn):
    def wrapper(cds):
        fwd = embedder_fn(cds)
        rev = embedder_fn(str(Seq(cds).reverse_complement()))
        return fwd, rev
    return wrapper

def sliding_window(cds):
    splitter = CharacterTextSplitter(
        chunk_size=CFG.CHUNK_SIZE,
        chunk_overlap=CFG.CHUNK_OVERLAP,
        separator=""
    )
    
    return splitter.split_text(cds)

@forward_and_reverse
def embedder(cds):
    model = CFG.MODEL
    
    with torch.no_grad():
        input_ids = torch.tensor(
            [model.tokenizer.tokenize(cds)],
            dtype=torch.int,
            device="cuda"
        )

        with amp.autocast("cuda", dtype=torch.bfloat16):
            _, hidden = model(
                input_ids,
                return_embeddings=True,
                layer_names=[CFG.LAYER]
            )

        embeddings = (
            hidden[CFG.LAYER]
            .to(torch.float32)
            .squeeze(0)
            .cpu()
            .numpy()
        )

    del input_ids, hidden
    torch.cuda.empty_cache()

    return embeddings

def nucleotide_to_codon_embeddings(fwd, rev):
    fwd_codons = fwd.reshape(fwd.shape[0]//3, 3, CFG.EMBEDDING_DIM)
    rev_codons = rev.reshape(fwd.shape[0]//3, 3, CFG.EMBEDDING_DIM)
    
    return np.concatenate(
        [fwd_codons, 
         rev_codons],
        axis=1
    )

def build_codons(batch):
    res = []
    
    for idx, codon in enumerate(batch["codon_embedding"]):
        codon_seq = batch["sequence"][idx*3:(idx*3)+3]
        
        sample = {
            "codon_sequence": codon_seq,
            "name":batch["name"],
            "family": batch["family"],
            "root": batch["root"],
            "subtree": batch["subtree"],
            "codon_embedding": codon.tolist(),
            "Prob[alpha>beta]": batch["Prob[alpha>beta]"][idx],
            "Prob[alpha<beta]": batch["Prob[alpha<beta]"][idx],
            "BayesFactor[alpha<beta]": batch["BayesFactor[alpha<beta]"][idx],
            "weight": batch["weight"]
        }
        res.append(sample)
    
    return res
    
def process(dataset):
    for batch in dataset:
        sequence = batch["sequence"]
        chunks = sliding_window(sequence)

        forward_embeddings, reverse_embeddings = (
            np.zeros((len(sequence), CFG.EMBEDDING_DIM)),
            np.zeros((len(sequence), CFG.EMBEDDING_DIM))
        )

        for chunk_idx, chunk in enumerate(chunks):
            fwd, rev = embedder(chunk)
                     
            if chunk_idx == 0:
                idx = fwd.shape[0]
                forward_embeddings[:idx] = fwd
                reverse_embeddings[:idx] = rev 
            else:
                fwd = fwd[CFG.CHUNK_OVERLAP:]
                rev = rev[CFG.CHUNK_OVERLAP:]
                chunk_len = fwd.shape[0]
                forward_embeddings[idx:idx + chunk_len] = fwd
                reverse_embeddings[idx:idx + chunk_len] = rev
                idx += chunk_len

        assert idx == len(sequence), (
            f"Mismatch: {idx} embeddings | {len(sequence)} nucleotides."
        )

        assert not np.isnan(forward_embeddings).any(), f"NaNs in forward | {batch['name']}"
        assert not np.isnan(reverse_embeddings).any(), f"NaNs in reverse | {batch['name']}"

        batch["codon_embedding"] = nucleotide_to_codon_embeddings(forward_embeddings, reverse_embeddings)

        codons = build_codons(batch)

        pd.DataFrame(codons).to_parquet(f"./embeddings/{batch['family']}.{batch['name']}.{batch['root']}.{batch['subtree']}.embeddings.parquet")

def main():
    dataset = load_dataset("parquet", data_dir="processed_data")
    process(dataset["train"])

if __name__ == "__main__":
    main()
