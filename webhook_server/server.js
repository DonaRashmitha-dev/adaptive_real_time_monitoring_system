const express = require("express");
const app = express();

app.use(express.json());

app.post("/alert", (req, res) => {
    console.log("🚨 ALERT:", req.body.alert);
    res.sendStatus(200);
});

app.listen(3000, () => console.log("Server running on port 3000"));