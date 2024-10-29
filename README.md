## Program

```bash
cd program
cargo build-bpf
solana program deploy target/deploy/pda_local.so
```

## App

- set `PROGRAM_ID` in `movie_review.py`
- store solana private key `wallet-keypair.json` in directory outside root dir

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install solders solana borsh-construct
python movie_review.py
```