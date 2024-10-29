## Program

```bash
cd program
cargo build-bpf
solana program deploy target/deploy/pda_local.so
```

## App

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```