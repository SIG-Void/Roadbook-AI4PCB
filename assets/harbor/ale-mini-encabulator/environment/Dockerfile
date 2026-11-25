FROM --platform=linux/amd64 kicad/kicad:10.0.0@sha256:9549d3a08e0822f9434a9eda0782c812451ab4a733c73535f9e8beed42039bc3
USER root
ENV HOME=/root LC_ALL=C.UTF-8
RUN mkdir -p /root/.config/kicad/10.0 /app/output \
    && cp /usr/share/kicad/template/fp-lib-table /usr/share/kicad/template/sym-lib-table /root/.config/kicad/10.0/ \
    && kicad-cli version
COPY input/ /app/input/
WORKDIR /app
CMD ["sleep", "infinity"]
