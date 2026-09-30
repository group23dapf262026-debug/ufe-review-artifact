# Anonymous artifact for local interaction features in Ethereum phishing detection

This repository is the double-blind review artifact for a controlled evaluation
of a 12-dimensional block of label-free local interaction statistics on the
HEIG-Phish benchmark. It contains the frozen experiment notebooks, compact
machine-readable results, figure-generation code, and protocol records needed
to inspect the claims in the manuscript.

## Repository layout

- `code/experiments/`: six matched Baseline--Plus experiments, the aggregate
  audit, the exact-edge Random Forest ablation, and the source-feature overlap
  audit.
- `code/figures/`: scripts and source data for all manuscript figures.
- `configs/`: frozen configurations for the six matched model families.
- `results/matched/`: 20-partition metrics and corrected paired comparisons.
- `results/ablation/`: exact-edge Random Forest ablation summaries.
- `results/released_split_reference/`: descriptive results on the original
  development-used split.
- `results/source_overlap/`: post-hoc source-feature provenance audit.
- `figures/`: vector PDFs used in the manuscript and supplement.

Large datasets, checkpoints, sampled batches, and trained model archives are
not redistributed. Their provenance and required hashes are documented in
`DATA.md`.

## Main evaluation

The six model notebooks use the same 20 predetermined stratified partitions
(seeds 2001--2020). Within each model family, Baseline and Plus share the
partition, model seed, configuration, decision threshold, and materialized
sampled inputs. Plus differs only by receiving the 12 additional interaction
statistics. The primary metric is test Macro-F1 at threshold 0.5.

Run these notebooks independently:

1. `matched_logistic_regression.ipynb`
2. `matched_random_forest.ipynb`
3. `matched_lightgbm.ipynb`
4. `matched_gat.ipynb`
5. `matched_graphsage.ipynb`
6. `matched_metaifd.ipynb`

After all six outputs are available, run `matched_aggregate_audit.ipynb` to
verify split identities and recompute the corrected paired comparisons.

The exact-edge ablation is reproduced with
`exact_edge_random_forest_ablation.ipynb`. The descriptive provenance analysis
is reproduced with `source_feature_overlap_audit.ipynb` using training and
validation nodes only.

## Figure regeneration

From the repository root:

```bash
python code/figures/fig1_framework.py
python code/figures/fig2_ufe_construction.py
python code/figures/fig3_matched_effects.py
python code/figures/fig4_ablation.py
python code/figures/figS1_source_overlap.py
```

The scripts read checked-in CSV/JSON files and do not refit models.

## Integrity and anonymization

The processed `data.pt` file used by the study has SHA-256
`8cc653bb389ea1a316f72c3893d0487ab09321552ae022ceaa89cd2499f690e8`.
The master matched-comparison protocol has archived SHA-256
`3c50b13557fc897d71787171b2a98be31b8784de4be6fbfa6932ab063ebd1145`.

For double-blind review, identifying protocol prefixes, filenames, notebook
outputs, and local absolute paths were removed. These anonymity-only edits do
not change model definitions, seeds, metrics, or result files. Archived code
and protocol hashes describe the executed pre-sanitization artifacts and are
therefore not byte hashes of the sanitized notebook files in this snapshot.

## Scope

The study evaluates stability under repeated partitions of one static,
transductive benchmark. It does not establish temporal or cross-dataset
generalization. Risk scores are research outputs and are not findings of
wrongdoing.

## License

No license is assigned in this review snapshot. The repository owner should
select an appropriate license before permanent public release.
