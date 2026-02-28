# analise_cenario2.py
# Cenário 2: Comparação Host x Docker
# Analisa tempos de resposta coletados no host e dentro de um container

import os
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1) CONFIGURAÇÃO
# =========================
ARQ_HOST = os.path.join("resultados", "tempos_host.txt")
ARQ_DOCKER = os.path.join("resultados", "tempos_cliente1_docker.txt")

SAIDA_BAR = os.path.join("resultados", "cenario2_barras.png")
SAIDA_BOX = os.path.join("resultados", "cenario2_boxplot.png")


# =========================
# 2) FUNÇÕES AUXILIARES
# =========================
def ler_tempos_txt(caminho):
    tempos = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip().replace(",", ".")
            if linha:
                tempos.append(float(linha))
    return np.array(tempos)


def resumo_estatistico(dados):
    return {
        "n": len(dados),
        "media": np.mean(dados),
        "mediana": np.median(dados),
        "desvio_padrao": np.std(dados, ddof=1),
        "min": np.min(dados),
        "max": np.max(dados),
        "p95": np.percentile(dados, 95),
        "p99": np.percentile(dados, 99),
    }


def imprimir(nome, stats):
    print(f"\n=== {nome} ===")
    print(f"N: {stats['n']}")
    print(f"Média: {stats['media']:.6f} s")
    print(f"Mediana: {stats['mediana']:.6f} s")
    print(f"Desvio padrão: {stats['desvio_padrao']:.6f} s")
    print(f"Mín: {stats['min']:.6f} s | Máx: {stats['max']:.6f} s")
    print(f"P95: {stats['p95']:.6f} s | P99: {stats['p99']:.6f} s")


# =========================
# 3) MAIN
# =========================
def main():
    os.makedirs("resultados", exist_ok=True)

    host = ler_tempos_txt(ARQ_HOST)
    docker = ler_tempos_txt(ARQ_DOCKER)

    stats_host = resumo_estatistico(host)
    stats_docker = resumo_estatistico(docker)

    imprimir("Host", stats_host)
    imprimir("Docker", stats_docker)

    # =========================
    # GRÁFICO 1 — BARRAS (MÉDIA)
    # =========================
    plt.figure()
    plt.bar(["Host", "Docker"],
            [stats_host["media"], stats_docker["media"]])
    plt.ylabel("Tempo de resposta (s)")
    plt.title("Cenário 2: Tempo Médio de Resposta (Host x Docker)")
    plt.savefig(SAIDA_BAR, dpi=200, bbox_inches="tight")
    plt.show()

    # =========================
    # GRÁFICO 2 — BOXPLOT
    # =========================
    plt.figure()
    plt.boxplot([host, docker],
                labels=["Host", "Docker"],
                showmeans=True)
    plt.ylabel("Tempo de resposta (s)")
    plt.title("Cenário 2: Distribuição do Tempo de Resposta")
    plt.savefig(SAIDA_BOX, dpi=200, bbox_inches="tight")
    plt.show()

    print("\nArquivos gerados:")
    print(f"- {SAIDA_BAR}")
    print(f"- {SAIDA_BOX}")


if __name__ == "__main__":
    main()
