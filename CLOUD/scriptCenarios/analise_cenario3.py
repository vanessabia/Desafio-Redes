import re
import os
import matplotlib.pyplot as plt

ARQ1 = os.path.join("resultados", "ab_bench1.txt")
ARQ2 = os.path.join("resultados", "ab_bench2.txt")

def ler_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extrair_float(texto, padrao):
    m = re.search(padrao, texto, re.MULTILINE)
    return float(m.group(1)) if m else None

def extrair_percentis_ms(texto):
    """
    Lê a seção:
    Percentage of the requests served within a certain time (ms)
      50%   5
      90%   6
      95%   6
      99%  10
    """
    percentis = {}
    # captura linhas do tipo: "  95%   6"
    linhas = re.findall(r"^\s*(\d+)%\s+(\d+)\s*$", texto, re.MULTILINE)
    for p, v in linhas:
        p = int(p)
        v = float(v)  # ms
        if p in (50, 90, 95, 99):
            percentis[p] = v
    return percentis

def extrair_metricas(texto):
    # Time per request: 6.856 [ms] (mean)
    tpr_mean = extrair_float(texto, r"Time per request:\s+([\d\.]+)\s+\[ms\]\s+\(mean\)")
    # Requests per second: 72.92 [#/sec] (mean)
    rps = extrair_float(texto, r"Requests per second:\s+([\d\.]+)\s+\[#/sec\]")
    # Transfer rate:  500.18 [Kbytes/sec] received
    transfer = extrair_float(texto, r"Transfer rate:\s+([\d\.]+)\s+\[Kbytes/sec\]\s+received")

    percentis = extrair_percentis_ms(texto)

    return {
        "time_per_request_mean_ms": tpr_mean,
        "requests_per_second": rps,
        "transfer_rate_kbytes_sec": transfer,
        "percentis_ms": percentis
    }

def plot_barras(metricas1, metricas2, saida):
    labels = ["Bench1", "Bench2"]

    rps = [metricas1["requests_per_second"], metricas2["requests_per_second"]]
    tpr = [metricas1["time_per_request_mean_ms"], metricas2["time_per_request_mean_ms"]]
    tr  = [metricas1["transfer_rate_kbytes_sec"], metricas2["transfer_rate_kbytes_sec"]]

    # 1) Requests per second
    plt.figure()
    plt.bar(labels, rps)
    plt.ylabel("Requests per second (#/s)")
    plt.title("Cenário 3: Vazão (Requests/s)")
    plt.savefig(os.path.join(saida, "cenario3_rps.png"), bbox_inches="tight")
    plt.close()

    # 2) Time per request (mean)
    plt.figure()
    plt.bar(labels, tpr)
    plt.ylabel("Time per request (mean) [ms]")
    plt.title("Cenário 3: Tempo por Requisição (médio)")
    plt.savefig(os.path.join(saida, "cenario3_time_per_request.png"), bbox_inches="tight")
    plt.close()

    # 3) Transfer rate
    plt.figure()
    plt.bar(labels, tr)
    plt.ylabel("Transfer rate [Kbytes/s]")
    plt.title("Cenário 3: Taxa de Transferência")
    plt.savefig(os.path.join(saida, "cenario3_transfer_rate.png"), bbox_inches="tight")
    plt.close()

def plot_percentis(metricas1, metricas2, saida):
    ps = [50, 90, 95, 99]
    p1 = [metricas1["percentis_ms"].get(p) for p in ps]
    p2 = [metricas2["percentis_ms"].get(p) for p in ps]

    plt.figure()
    plt.plot(ps, p1, marker="o", label="Bench1")
    plt.plot(ps, p2, marker="o", label="Bench2")
    plt.xlabel("Percentil (%)")
    plt.ylabel("Tempo (ms)")
    plt.title("Cenário 3: Percentis do Tempo de Resposta (cauda)")
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.savefig(os.path.join(saida, "cenario3_percentis.png"), bbox_inches="tight")
    plt.close()

def main():
    os.makedirs("graficos", exist_ok=True)

    t1 = ler_arquivo(ARQ1)
    t2 = ler_arquivo(ARQ2)

    m1 = extrair_metricas(t1)
    m2 = extrair_metricas(t2)

    # imprime resumo (pra você colar no relatório depois)
    print("=== Cenário 3 - Resumo (Bench1) ===")
    print(m1)
    print("\n=== Cenário 3 - Resumo (Bench2) ===")
    print(m2)

    plot_barras(m1, m2, "graficos")
    plot_percentis(m1, m2, "graficos")

    print("\n✅ Gráficos gerados na pasta: graficos/")
    print(" - cenario3_rps.png")
    print(" - cenario3_time_per_request.png")
    print(" - cenario3_transfer_rate.png")
    print(" - cenario3_percentis.png")

if __name__ == "__main__":
    main()
