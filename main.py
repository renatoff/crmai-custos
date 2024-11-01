# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
# dist prob duracao

distribuicao_duracao_reunioes = {
    0: 0,
    15: 0.1,
    30: 0.2,
    45: 0.4,
    60: 0.2,
    75: 0.1,
    90: 0,
}

# Plot the distribution
plt.bar(
    distribuicao_duracao_reunioes.keys(),
    distribuicao_duracao_reunioes.values(),
)
plt.title("Distribution of Meeting Durations")
plt.show()

# Distribution for meeting start times
# Generate times from 8:00 to 20:00 in 15-minute intervals (0.25 in hour increments)
distribuicao_horario_inicio = {
    8.0 + 0.25 * i: 5
    for i in range(
        49
    )  # 49 intervals from 8:00 to 20:00 (inclusive)
}

# Adjust the probability values for specific times
adjustments = {
    12.0: 2,
    12.25: 2,
    12.5: 2,
    12.75: 2,
    13.0: 2,
    19.0: 1,
    19.25: 1,
    19.5: 1,
    19.75: 1,
    20.0: 1,
}

# Apply the adjustments
for time, prob in adjustments.items():
    distribuicao_horario_inicio[time] = prob

# Normalize to create a probability distribution
total = sum(distribuicao_horario_inicio.values())
distribuicao_horario_inicio = {
    key: value / total
    for key, value in distribuicao_horario_inicio.items()
}

assert sum(distribuicao_horario_inicio.values()) == 1.0

# Plot the distribution
plt.bar(
    distribuicao_horario_inicio.keys(),
    distribuicao_horario_inicio.values(),
)
plt.title("Distribution of Meeting Start Times")

# %%

multiplicador_reunioes_por_dia = (
    7  # gera 5.357 reunioes por dia em media
)
numero_usuarios_por_dia = 30
numero_dias_random_walks = 1000

horas_dia = []
for dia in range(numero_dias_random_walks):
    usuarios = []
    for usuario in range(numero_usuarios_por_dia):
        hora = list(distribuicao_horario_inicio.keys())[0]
        reunioes = []
        while (
            hora < list(distribuicao_horario_inicio.keys())[-1]
        ):
            # print("Hora:", hora)
            probabilidade_ter_reuniao_nesse_horario = (
                distribuicao_horario_inicio[hora]
            ) * multiplicador_reunioes_por_dia
            # print(
            #     "Probabilidade:",
            #     probabilidade_ter_reuniao_nesse_horario,
            # )
            tem_reuniao = np.random.choice(
                [True, False],
                p=[
                    probabilidade_ter_reuniao_nesse_horario,
                    1 - probabilidade_ter_reuniao_nesse_horario,
                ],
            )
            # print("Tem reuniao:", tem_reuniao)
            if tem_reuniao:
                duracao_reuniao = (
                    np.random.choice(
                        list(
                            distribuicao_duracao_reunioes.keys()
                        ),
                        p=list(
                            distribuicao_duracao_reunioes.values()
                        ),
                    )
                    / 60
                )
                # print("Duracao:", duracao_reuniao)
                reunioes.append(
                    {"hora": hora, "duracao": duracao_reuniao}
                )

            # print("---------------")
            if tem_reuniao:
                hora += duracao_reuniao
            else:
                hora += 0.25
        usuarios.append(reunioes)

    horas = 0
    for hora in distribuicao_horario_inicio.keys():
        tem_reuniao = False
        for usuario in usuarios:
            for reuniao in usuario:

                if (
                    hora >= reuniao["hora"]
                    and hora
                    <= reuniao["hora"] + reuniao["duracao"]
                ):
                    tem_reuniao = True
                    break

            if tem_reuniao:
                horas += 0.25
                break
        hora += 0.25

    horas_dia.append(horas)

np.mean(horas_dia)
# %%
