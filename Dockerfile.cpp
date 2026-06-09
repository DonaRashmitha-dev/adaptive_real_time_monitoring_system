FROM gcc:13 AS builder
WORKDIR /build
COPY metrics_cpp/metrics.cpp .
RUN g++ -O2 -static -o metrics metrics.cpp

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /build/metrics ./metrics_cpp/metrics
CMD ["./metrics_cpp/metrics"]
