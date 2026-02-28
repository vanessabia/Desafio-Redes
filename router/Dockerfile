FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    iproute2 iptables iputils-ping curl \
 && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
