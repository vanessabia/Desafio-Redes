# analise_cenario1.py
# Cenário 1: Comparação de tempo de resposta com 1 cliente vs 2 clientes (Docker -> Docker)
# Lê arquivos .txt com tempos (em segundos), calcula estatísticas e gera gráficos.

import os
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1) CONFIGURAÇÃO (mude aqui se seus nomes forem outros)
# =========================
ARQ_1_CLIENTE = os.path.join("resultados", "tempos_cliente1_docker.txt")
ARQ_2_CLIENTES = os.path.join("resultados", "tempos_cliente2_docker.txt")

SAIDA_BAR = os.path.join("resultados", "cenario1_barras.png")
SAIDA_BOX = os.path.join("resultados", "cenario1_boxplot.png")


# =========================
# 2) FUNÇÕES AUXILIARES
# =========================
def ler_tempos_txt(caminho: str) -> np.ndarray:
    """
    Lê um arquivo TXT contendo um tempo por linha.
    Aceita vírgula ou ponto como separador decimal.
    Retorna np.array de floats.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    tempos = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            linha = linha.replace(",", ".")
            try:
                tempos.append(float(linha))
            except ValueError:
                # Se tiver alguma sujeira no arquivo, ignora a linha
                continue

    if len(tempos) == 0:
        raise ValueError(f"Nenhum valor numérico foi lido em: {caminho}")

    return np.array(tempos, dtype=float)


def resumo_estatistico(amostra: np.ndarray) -> dict:
    """
    Retorna estatísticas descritivas da amostra:
    média, mediana, desvio padrão, mínimo, máximo, p95 e p99.
    """
    return {
        "n": int(amostra.size),
        "media": float(np.mean(amostra)),
        "mediana": float(np.median(amostra)),
        "desvio_padrao": float(np.std(amostra, ddof=1)) if amostra.size > 1 else 0.0,
        "min": float(np.min(amostra)),
        "max": float(np.max(amostra)),
        "p95": float(np.percentile(amostra, 95)),
        "p99": float(np.percentile(amostra, 99)),
    }


def imprimir_resumo(nome: str, stats: dict) -> None:
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

    # 3.1) Ler dados
    t1 = ler_tempos_txt(ARQ_1_CLIENTE)
    t2 = ler_tempos_txt(ARQ_2_CLIENTES)

    # 3.2) Estatísticas
    s1 = resumo_estatistico(t1)
    s2 = resumo_estatistico(t2)

    imprimir_resumo("Cenário 1 - 1 Cliente", s1)
    imprimir_resumo("Cenário 1 - 2 Clientes", s2)

    # =========================
    # 4) GRÁFICO 1: Barras (Média)
    # =========================
    plt.figure()
    categorias = ["1 Cliente", "2 Clientes"]
    medias = [s1["media"], s2["media"]]

    plt.bar(categorias, medias)
    plt.ylabel("Tempo de resposta (s)")
    plt.title("Cenário 1: Tempo Médio de Resposta (1 vs 2 Clientes)")
    plt.savefig(SAIDA_BAR, dpi=200, bbox_inches="tight")
    plt.show()

    # =========================
    # 5) GRÁFICO 2: Boxplot (Distribuição)
    # =========================
    plt.figure()
    plt.boxplot([t1, t2], labels=categorias, vert=True, showmeans=True)
    plt.ylabel("Tempo de resposta (s)")
    plt.title("Cenário 1: Distribuição do Tempo de Resposta")
    plt.savefig(SAIDA_BOX, dpi=200, bbox_inches="tight")
    plt.show()

    print("\nArquivos gerados:")
    print(f"- {SAIDA_BAR}")
    print(f"- {SAIDA_BOX}")


if __name__ == "__main__":
    main()
