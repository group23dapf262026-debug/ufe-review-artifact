# Data and external-code requirements

## HEIG-Phish

Obtain the processed HEIG-Phish graph from the official Meta-IFD release:

`https://github.com/GISce-Team/Meta-IFD`

Expected location in the released layout:

`Phish/processed/data.pt`

Required SHA-256:

`8cc653bb389ea1a316f72c3893d0487ab09321552ae022ceaa89cd2499f690e8`

The study uses 2,763 labeled externally owned accounts: 1,206 phishing and
1,557 normal. The processed graph has no timestamp or block-number field, so
the evaluation is static and transductive rather than temporal.

Do not commit `data.pt` to this repository. The file is large and belongs to
the external dataset release.

## Meta-IFD code and checkpoint

The Meta-IFD experiment additionally requires the official source tree and its
pretrained IC-VAE checkpoint:

`pretrain_model/icvae_Phish.pkl`

Required checkpoint SHA-256:

`536c13bc765039c7e1d0fa5ec168e9bfbe47ad92aebd156ccc73de6d194d0bf8`

Place the official source tree where the notebook can discover it, or adapt
only the input-location cell without changing seeds, configurations, or the
evaluation protocol.

## Files intentionally omitted

- raw and processed blockchain archives;
- trained checkpoints and sampled-batch caches;
- node-level prediction exports;
- temporary notebook outputs and local machine paths.

Compact aggregate CSV and JSON results are included under `results/`.
