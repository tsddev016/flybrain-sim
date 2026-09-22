# FlyBrain Simulator 2D

**TSZIN DEV** — simulador de moscas artificiais.

## Estrutura

```
FlyBrain/
├── launch/          # instalador e atalhos Windows
├── src/flybrain/    # codigo do jogo
│   ├── agents/
│   ├── simulation/
│   ├── learning/
│   ├── ui/
│   └── assets/
├── data/
├── requirements.txt
└── README.md
```

## Windows

1. Extraia o ZIP completo (FlyBrain.zip)
2. Execute `launch\\INSTALAR.bat`
3. Abra pelo atalho ou `launch\\FlyBrain.bat`

```bat
cd FlyBrain
set PYTHONPATH=src
python -m flybrain.main
```

## Licenca

Projeto experimental — TSZIN DEV.
