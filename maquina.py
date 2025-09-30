from json import load
import sys

resultado = 0
posi_atual = 0

# tenta pegar da linha de comando, se não conseguir, usa valores padrão
if len(sys.argv) < 4:
    spec_file = "especificacao.json"
    input_file = "entrada.txt"
    output_file = "saida.txt"
else:
    spec_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

with open(spec_file, "r", encoding="utf-8") as instrucao:
    especific = load(instrucao)

estado_atual = especific["initial"]

with open(input_file, "r", encoding="utf-8") as texto:
    problema = list(texto.read().strip())
    if not problema:
        problema = [especific["white"]]
    else:
        problema.append(especific["white"])

while True:
    encontrou_func = False
    for i in especific["transitions"]:
        if estado_atual == i["from"] and problema[posi_atual] == i["read"]:
            problema[posi_atual] = i["write"]

            if i["dir"] == "R":
                posi_atual += 1
            elif i["dir"] == "L":
                posi_atual -= 1

            # se sair dos limites, expande a fita
            if posi_atual < 0:
                problema.insert(0, especific["white"])
                posi_atual = 0
            elif posi_atual >= len(problema):
                problema.append(especific["white"])

            estado_atual = i["to"]
            encontrou_func = True
            break

    if not encontrou_func:  # rejeita
        resultado = 0
        break
    
    if estado_atual in especific["final"]:  # aceita
        resultado = 1
        break

# grava fita final
with open(output_file, "w", encoding="utf-8") as saida:
    saida.write("".join(problema).rstrip(especific["white"]) + "\n")

# imprime 1 ou 0 no terminal
print(resultado)
