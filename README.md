# Emb2Emb Client

Labelist client for emb2emb dataset manipulation.

## Deploy

**Requirements** 
- a embedding model like `bert` already downloaded and configured in .env 
- python runtime
- preferably conda

**With Venv**

```sh
conda create -n emb2emb-client
conda activate emb2emb-client
pip install -r requirements.txt
python main.py
```

**Without Venv**
```sh
pip3 install -r requirements.txt --break-system-packages
python3 main.py
```

## Commands

Run command help for more info.
