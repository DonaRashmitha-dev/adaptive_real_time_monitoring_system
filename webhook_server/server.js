const express = require("express");
const path    = require("path");
const app     = express();

// Serve dashboard FIRST — before any other middleware
app.use(express.static(path.join("/app", "dashboard")));
app.use(express.json());

const MAX_ALERTS  = 100;
const MAX_METRICS = 50;
const alertStore  = [];
const metricStore = [];

let redisConnected = false;
try {
    const { createClient } = require("redis");
    const subscriber = createClient({ url: process.env.REDIS_URL || "redis://redis:6379" });
    subscriber.on("error", (e) => console.error("[redis] error:", e.message));
    (async () => {
        await subscriber.connect();
        await subscriber.subscribe("alerts", (message) => {
            try {
                const alert = JSON.parse(message);
                alertStore.push(alert);
                if (alertStore.length > MAX_ALERTS) alertStore.shift();
                console.log(`[${alert.severity}] ${alert.alert} | value=${alert.value} threshold=${alert.threshold_at_time}`);
            } catch (e) { console.error("[redis] parse error:", e.message); }
        });
        redisConnected = true;
        console.log("Redis subscriber connected");
    })();
} catch (e) {
    console.warn("[redis] not available:", e.message);
}

app.post("/alert", (req, res) => {
    const alert = {
        timestamp:         req.body.timestamp         || new Date().toISOString(),
        alert:             req.body.alert             || "unknown",
        type:              req.body.type              || "unknown",
        severity:          req.body.severity          || "INFO",
        value:             req.body.value             ?? 0,
        threshold_at_time: req.body.threshold_at_time ?? 0,
    };
    alertStore.push(alert);
    if (alertStore.length > MAX_ALERTS) alertStore.shift();
    console.log(`[${alert.severity}] ${alert.alert} | value=${alert.value} threshold=${alert.threshold_at_time}`);
    res.sendStatus(200);
});

app.post("/metric", (req, res) => {
    const metric = {
        timestamp: new Date().toISOString(),
        cpu:       req.body.cpu     ?? 0,
        memory:    req.body.memory  ?? 0,
        latency:   req.body.latency ?? 0,
    };
    metricStore.push(metric);
    if (metricStore.length > MAX_METRICS) metricStore.shift();
    res.sendStatus(200);
});

app.get("/alerts",     (req, res) => res.json(alertStore));
app.get("/metrics",    (req, res) => res.json(metricStore));
app.get("/health",     (req, res) => res.json({ status: "ok", alerts: alertStore.length, metrics: metricStore.length, redis: redisConnected }));
app.get("/prometheus", (req, res) => {
    res.set("Content-Type", "text/plain");
    res.send([
        `alerts_total ${alertStore.length}`,
        `redis_connected ${redisConnected ? 1 : 0}`,
    ].join("\n"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Webhook server running on port ${PORT}`));
