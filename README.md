# FlyBrain Simulator 2D

Prototipo experimental de uma mosca artificial com sensores limitados, memoria de curto prazo e tomada de decisao inspirada em principios de comportamento de insetos.

> O arquivo anatomico (OBJ/NRRD do Virtual Fly Brain) **nao** e usado como modelo executavel. Serve apenas como referencia de inspiracao.

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

## Controles

| Tecla | Acao |
|-------|------|
| SPACE | Pausar / continuar |
| R | Resetar a mosca |
| D | Ligar/desligar raios sensoriais |
| + / - | Acelerar / desacelerar |
| ESC / Q | Sair |

## O que a mosca ve

Ela **nao** recebe coordenadas absolutas. Recebe apenas:

- distancia + angulo relativo + intensidade de comida e agua
- multiplos raios de parede (frente, esquerda, direita)
- obstaculos proximos
- **ameaca da aranha** (predador que gera medo)
- estado interno (energia, fome, sede, medo)

## Arquitetura

```
Ambiente (World)
       |
   Sensores          <- FOV limitado, cheiro, raycast, ameaca
       |
  FlyBrain Core
    - Reflexos (evitar parede/obstaculo, fugir da aranha, descansar)
    - Motivacao (fome, sede, medo, curiosidade)
    - Selecao de objetivo
    - Comando motor
       |
   Motor + metabolismo
       |
  Memoria (curto prazo + landmarks)
```

## Estrutura

```
flybrain_sim/
├── main.py
├── requirements.txt
├── simulator/
│   └── world.py
├── fly/
│   ├── sensors.py
│   ├── memory.py
│   ├── brain.py
│   └── fly.py
└── learning/
    ├── reward.py
    └── replay.py
```

## Proximos passos

1. Aprendizado por recompensa (RL)
2. Multiplas moscas
3. Ambiente 3D com a mesma interface Sensors -> Brain -> Motor
