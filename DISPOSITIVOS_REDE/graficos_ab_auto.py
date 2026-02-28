import re
import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG: nomes dos arquivos
# =========================
FILES = [
    ("0 - Baseline",        "cenario0_ab.txt"),
    ("1 - Latencia 100ms",  "cenario1_ab_latencia.txt"),
    ("2 - Banda 1Mbit",     "cenario2_ab_banda.txt"),
]

# =========================
# Funções de extração
# =========================
def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_float(pattern: str, text: str, field_name: str) -> float:
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        raise ValueError(f"Não encontrei '{field_name}' no arquivo (pattern falhou).")
    return float(m.group(1))

def extract_int(pattern: str, text: str, field_name: str) -> int:
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        raise ValueError(f"Não encontrei '{field_name}' no arquivo (pattern falhou).")
    return int(m.group(1))

def parse_ab_output(text: str) -> dict:
    # Requests per second: 3288.32 [#/sec] (mean)
    rps = extract_float(r"Requests per second:\s+([0-9.]+)", text, "Requests per second")

    # Time per request: 15.205 [ms] (mean)
    # OBS: o AB imprime duas linhas de Time per request.
    # A primeira é (mean), a segunda é (mean, across all concurrent requests).
    # Vamos pegar a primeira linha (mean) que termina com '(mean)'
    mean_ms = extract_float(
        r"Time per request:\s+([0-9.]+)\s+\[ms\]\s+\(mean\)\s*$",
        text,
        "Time per request (mean)"
    )

    # Transfer rate: 510.59 [Kbytes/sec] received
    transfer_kbps = extract_float(r"Transfer rate:\s+([0-9.]+)\s+\[Kbytes/sec\]", text, "Transfer rate")

    # Percentil 95:
    # 95%  17
    p95 = extract_int(r"^\s*95%\s+(\d+)\s*$", text, "p95")

    return {
        "RPS": rps,
        "Mean_ms": mean_ms,
        "Transfer_KBps": transfer_kbps,
        "P95_ms": p95
    }

# =========================
# Leitura e parsing
# =========================
rows = []
errors = []

for label, filename in FILES:
    if not os.path.exists(filename):
        errors.append(f"Arquivo não encontrado: {filename}")
        continue

    try:
        txt = read_text(filename)
        metrics = parse_ab_output(txt)
        rows.append({"Cenario": label, **metrics})
    except Exception as e:
        errors.append(f"Erro ao processar {filename}: {e}")

if errors:
    print("⚠️ Problemas encontrados:")
    for e in errors:
        print(" -", e)

if not rows:
    raise SystemExit("Nenhum arquivo foi processado. Verifique os nomes e rode novamente.")

df = pd.DataFrame(rows)

# Ordenar por número do cenário (pega o primeiro dígito antes do " - ")
df["ord"] = df["Cenario"].str.extract(r"^(\d+)").astype(int)
df = df.sort_values("ord").drop(columns=["ord"])

# Salvar CSV para o relatório
df.to_csv("resultados_ab.csv", index=False, encoding="utf-8")
print("\n✅ CSV gerado: resultados_ab.csv")
print(df)

# =========================
# GRÁFICOS
# =========================

# 1) Throughput
plt.figure()
plt.bar(df["Cenario"], df["RPS"])
plt.ylabel("Requests por segundo (req/s)")
plt.title("Throughput por cenário (ApacheBench)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("grafico_requests_por_segundo.png", dpi=200)
plt.close()
print("✅ Gerado: grafico_requests_por_segundo.png")

# 2) Transfer rate
plt.figure()
plt.bar(df["Cenario"], df["Transfer_KBps"])
plt.ylabel("Taxa de transferência (KB/s)")
plt.title("Transfer rate por cenário (ApacheBench)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("grafico_transfer_rate_kbps.png", dpi=200)
plt.close()
print("✅ Gerado: grafico_transfer_rate_kbps.png")

# 3) Latência combinada (mean + p95)
plt.figure()
plt.plot(df["Cenario"], df["Mean_ms"], marker="o", label="Tempo médio (ms)")
plt.plot(df["Cenario"], df["P95_ms"], marker="o", label="p95 (ms)")
plt.ylabel("Tempo (ms)")
plt.title("Latência: tempo médio vs p95 (ApacheBench)")
plt.xticks(rotation=20, ha="right")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_latencia_medio_vs_p95.png", dpi=200)
plt.close()
print("✅ Gerado: grafico_latencia_medio_vs_p95.png")

print("\n🎉 Tudo pronto! Arquivos finais:")
print("- resultados_ab.csv")
print("- grafico_requests_por_segundo.png")
print("- grafico_transfer_rate_kbps.png")
print("- grafico_latencia_medio_vs_p95.png")
