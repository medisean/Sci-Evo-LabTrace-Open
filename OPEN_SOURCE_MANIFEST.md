# Open Source Manifest

## Scope

This repository contains the Sci-Evo-LabTrace dataset, code, documentation, quality reports, open-license source papers, and redacted MinerU parsing artifacts needed to reproduce and extend the dataset.

Dataset page: https://opendatalab.com/medimedi/Sci-Evo-LabTrace

## Included

- `data/processed/scievo_gold.jsonl`: 25 gold Sci-Evo cases.
- `data/processed/scievo_eval_tasks.jsonl`: 363 generated evaluation tasks.
- `data/processed/baseline_results.json`: reproducible baseline results for structured evaluation tasks.
- `data/curated/cases/`: manually curated case source files.
- `schemas/`: Sci-Evo case schema.
- `scripts/`: dataset build, validation, evaluation-task generation, source vetting, quality reporting, and MinerU parsing scripts.
- `docs/`: technical report, dataset card, and annotation guidelines.
- `reports/`: quality report, MinerU run report, readiness report, case-depth audit, and vetted source queue.
- `source_papers/`: 4 open-license paper PDFs used for cases `SELT-PROT-0002` to `SELT-PROT-0005`.
- `mineru_artifacts/`: redacted MinerU structured outputs for the 4 open-license paper PDFs. Author contact fields and raw model outputs with embedded image payloads are not included.

## License

Original dataset annotations, scripts, and documentation are released under CC-BY-4.0 unless otherwise stated. Third-party paper PDFs and parsed artifacts remain under their original source licenses, recorded in `source_papers/README.md` and per-case `source.license_status` fields.
