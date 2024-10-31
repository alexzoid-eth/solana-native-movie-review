Example from Solana [Native Onchain Development](https://solana.com/developers/courses/native-onchain-development) course.

## Program

```bash
cd program
cargo build-bpf
solana program deploy target/deploy/pda_local.so
```

## App

- set `PROGRAM_ID` in `movie_review.py`

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install solders solana borsh-construct
python movie_review.py
```