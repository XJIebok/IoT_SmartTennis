let selectedThing = null;
let lastSensorsData = [];
let autoUpdateEnabled = true;
let updateInterval = null;

const container = document.getElementById("sensors_container");
const toggleButton = document.getElementById("toggle_update");

const sensorUrls = [
    "/connect_camera",
    "/connect_line_sensor",
    "/connect_net_sensor"
];


function formatValue(value) {
    if (value === null || value === undefined) {
        return "-";
    }

    if (Array.isArray(value)) {
        return "(" + value.join(", ") + ")";
    }

    if (typeof value === "boolean") {
        return value ? "да" : "нет";
    }

    return value;
}


function getSensorData(dataUrl) {
    return $.ajax({
        type: "GET",
        url: dataUrl,
        dataType: "json"
    });
}


function renderSensors(sensors) {
    container.innerHTML = "";

    sensors.forEach((sensor) => {
        const sensorBlock = document.createElement("div");
        sensorBlock.className = "sensor-block";

        const button = document.createElement("button");
        button.className = "sensor-button";
        button.innerText = sensor.name;

        button.onclick = function () {
            if (selectedThing === sensor.id) {
                selectedThing = null;
            } else {
                selectedThing = sensor.id;
            }

            renderSensors(lastSensorsData);
        };

        sensorBlock.appendChild(button);

        if (selectedThing === sensor.id) {
            const details = document.createElement("div");
            details.className = "sensor-details";

            Object.entries(sensor).forEach(([key, value]) => {
                const p = document.createElement("p");
                p.innerText = `${key}: ${formatValue(value)}`;
                details.appendChild(p);
            });

            sensorBlock.appendChild(details);
        }

        container.appendChild(sensorBlock);
    });
}


function updateData() {
    const requests = sensorUrls.map((url) => getSensorData(url));

    Promise.all(requests).then((responses) => {
        lastSensorsData = responses;
        renderSensors(lastSensorsData);
    });
}


function startAutoUpdate() {
    updateData();

    updateInterval = setInterval(updateData, 1000);
    autoUpdateEnabled = true;

    toggleButton.innerText = "Автообновление: включено";
}


function stopAutoUpdate() {
    clearInterval(updateInterval);
    updateInterval = null;
    autoUpdateEnabled = false;

    toggleButton.innerText = "Автообновление: выключено";
}


function toggleAutoUpdate() {
    if (autoUpdateEnabled) {
        stopAutoUpdate();
    } else {
        startAutoUpdate();
    }
}


toggleButton.onclick = toggleAutoUpdate;

startAutoUpdate();