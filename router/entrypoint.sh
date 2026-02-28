#!/bin/bash
set -e

# 1) Ativa roteamento (IP forwarding) dentro do container
sysctl -w net.ipv4.ip_forward=1 >/dev/null

# 2) Libera o encaminhamento entre interfaces (eth0 <-> eth1)
iptables -P FORWARD ACCEPT

echo "[ROTEADOR] IP forwarding habilitado e FORWARD liberado."
echo "[ROTEADOR] Interfaces:"
ip -br a

# Mantém o container vivo
sleep infinity
