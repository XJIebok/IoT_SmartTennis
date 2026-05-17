
let lastSensorsData = [];
let autoUpdateEnabled = true;
let updateInterval = null;

const toggleButton = document.getElementById("toggle_update");

let selectedThing = null;
let lastThingsData = [];

const container = document.getElementById("things_container");

const things = [
    { deviceName: "camera", url: "/connect_camera" },
    { deviceName: "line_sensor", url: "/connect_line_sensor" },
    { deviceName: "net_sensor", url: "/connect_net_sensor" },
    { deviceName: "scoreboard", url: "/connect_scoreboard" },
    { deviceName: "speaker", url: "/connect_speaker" }
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

    if (typeof value === "object") {
        return JSON.stringify(value);
    }

    return value;
}

// Отрисовка данных с датчиков
function renderThings(thingsData) {
    container.innerHTML = "";

    const template = document.getElementById("thing_card_template");

    thingsData.forEach((thing) => {
        const card = template.content.cloneNode(true);

        const thingCard = card.querySelector(".thing-card");
        const header = card.querySelector(".thing-header");
        const idElement = card.querySelector(".thing-id");
        const nameElement = card.querySelector(".thing-name");
        const statusElement = card.querySelector(".thing-status");
        const powerButton = card.querySelector(".power-btn");
        const details = card.querySelector(".thing-details");

        idElement.textContent = thing.id;
        nameElement.textContent = thing.name;
        statusElement.textContent = thing.status;

        statusElement.className = "thing-status";

        if (thing.status === "online") {
            statusElement.classList.add("status-online");
        } else if (thing.status === "offline") {
            statusElement.classList.add("status-offline");
        } else {
            statusElement.classList.add("status-maintenance");
        }

        powerButton.onclick = function (event) {
            event.stopPropagation();

            const newStatus = thing.status === "online" ? "offline" : "online";
            setDeviceStatus(thing.deviceName, newStatus);
        };

        header.onclick = function () {
            if (selectedThing === thing.id) {
                selectedThing = null;
            } else {
                selectedThing = thing.id;
            }

            renderThings(lastThingsData);
        };

        if (selectedThing === thing.id) {
            details.innerHTML = "";

            Object.entries(thing).forEach(([key, value]) => {
                if (key === "deviceName") {
                    return;
                }

                const p = document.createElement("p");
                p.textContent = `${key}: ${formatValue(value)}`;
                details.appendChild(p);
            });

            details.style.display = "block";
        } else {
            details.style.display = "none";
        }

        container.appendChild(card);
    });
}

function getThingData(url) {
    return $.ajax({
        type: "GET",
        url: url,
        dataType: "json"
    });
}


function updateData() {
    const requests = things.map((thing) => {
        return getThingData(thing.url).then((response) => {
            response.deviceName = thing.deviceName;
            return response;
        });
    });

    Promise.all(requests).then((responses) => {
        lastThingsData = responses;
        renderThings(lastThingsData);
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

function setDeviceStatus(deviceName, newStatus) {
    $.ajax({
        type: "GET",
        url: "/set_status",
        dataType: "json",
        data: {
            device: deviceName,
            status: newStatus
        },
        success: function (response) {
            console.log(response);
            updateData();
        },
        error: function () {
            alert("Ошибка при отправке команды на сервер");
        }
    });
}