# 🌐 Desafio Lab de Redes

Projeto de laboratório para simulação de rede utilizando **Docker Compose**, com duas sub-redes conectadas por um container roteador e um servidor web Nginx.

## 📌 Objetivo

Simular o tráfego entre clientes e servidor em redes diferentes, utilizando um roteador intermediário, permitindo realizar testes de conectividade e desempenho.

---

## 🏗️ Topologia

- 🔵 rede_clientes → 172.22.0.0/24  
- 🟢 rede_servidor → 172.21.0.0/24  

Containers principais:

- cliente1  
- cliente2  
- cliente_teste  
- bench1  
- bench2  
- roteador  
- servidor_web (Nginx)

O roteador conecta as duas redes e permite a comunicação entre elas.

---

## 🚀 Como executar

### Subir o ambiente
  ```bash
         docker compose up -d --build
  ```
### Ver containers ativos
  ```bash
         docker ps
  ```
## Configuração de Rotas

### Nos clientes
```bash
docker exec -it cliente_teste bash
ip route add default via 172.22.0.254
```

### No servidor web
```bash
docker exec -it servidor_web sh
ip route add 172.22.0.0/24 via 172.21.0.254
```

## 🧪 Testes

✅ Ping
```bash
ping -c 4 172.21.0.10
```
✅ Curl
```bash
curl http://172.21.0.10/
```
Resposta esperada:
```bash
Servidor Web OK
```

✅ ApacheBench
``` bash
docker exec -it bench1 sh
ab -n 1000 -c 50 http://172.21.0.10/
```

### 🌍 Acesso via navegador
```bash
http://localhost:8080
```

### 🧹 Parar o ambiente
```bash
docker compose down
````
### 👩‍💻 Autora

Vanessa Beatriz
