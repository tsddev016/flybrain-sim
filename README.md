# FlyBrain Simulator 2D

Simulador experimental de moscas artificiais com sensores limitados, memoria, motivacao, acasalamento, ninhos, ovos e predadores (aranhas).

## Como executar

### Windows (recomendado)

1. Extraia o projeto.
2. Execute **INSTALAR.bat** uma vez (instala dependencias e cria atalho).
3. Abra pelo atalho **FlyBrain Simulator** na area de trabalho.

### Manual

```bash
pip install -r requirements.txt
python main.py
```

## Controles

| Tecla | Acao |
|-------|------|
| SPACE | Pausar / continuar |
| R | Reiniciar moscas |
| D | Liga/desliga raios de sensores |
| TAB | Alternar painel entre as moscas |
| + / - | Velocidade da simulacao |
| ESC / Q | Sair |

## Recursos

- Mapa amplo com paredes, comida, agua e pedras
- Moscas macho e femea (sprites distintos)
- Sono em ninhos quando a fadiga sobe
- Acasalamento e ovos (eclodem em novas moscas)
- Aranhas com fome, sede, energia, caca, ninhos e ovos
- Sons procedurais de insetos e eventos
- Interface em portugues

## Licenca

Projeto experimental educacional.
