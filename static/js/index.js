
let lastSensorsData = [];
let autoModeEnabled = false;
let autoUpdateEnabled = true;
let updateInterval = null;
let autoModeInterval = null;

const toggleButton = document.getElementById("toggle_update");

let selectedThing = null;
let lastThingsData = [];

const container = document.getElementById("things_container");

const autoModeButton = document.getElementById("toggle_auto_mode");
const autoModeResult = document.getElementById("auto_mode_result");

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

        const controls = card.querySelector(".thing-controls");

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
            if (thing.status !== "online") {
                renderInactiveMessage(thing, details);
            } else {
                renderDetails(thing, details);
                renderControls(thing, controls);
            }
            details.style.display = "block";
            controls.style.display = "block";
        } else {
            details.style.display = "none";
            controls.style.display = "none";
        }

        container.appendChild(card);
    });
}
function renderDetails(thing, detailsContainer) {
    detailsContainer.innerHTML = "";
        Object.entries(thing).forEach(([key, value]) => {
            if (key === "deviceName") {
                return;
            }
            const p = document.createElement("p");
            p.textContent = `${key}: ${formatValue(value)}`;
            detailsContainer.appendChild(p);
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
function updateAutoRally() {
    $.ajax({
        type: "GET",
        url: "/auto_rally",
        dataType: "json",
        success: function (response) {
            console.log(response);

            autoModeResult.innerHTML = `
                <strong>Результат автоматического режима:</strong><br>
                event: ${response.event || "-"}<br>
                point_to: ${response.point_to || "-"}<br>
                result: ${response.result || "-"}<br>
                message: ${response.message || "-"}
            `;

            const thingsFromAutoMode = [];

            if (response.camera) {
                response.camera.deviceName = "camera";
                thingsFromAutoMode.push(response.camera);
            }

            if (response.line_sensor) {
                response.line_sensor.deviceName = "line_sensor";
                thingsFromAutoMode.push(response.line_sensor);
            }

            if (response.net_sensor) {
                response.net_sensor.deviceName = "net_sensor";
                thingsFromAutoMode.push(response.net_sensor);
            }

            if (response.scoreboard) {
                response.scoreboard.deviceName = "scoreboard";
                thingsFromAutoMode.push(response.scoreboard);
            }

            if (response.speaker) {
                response.speaker.deviceName = "speaker";
                thingsFromAutoMode.push(response.speaker);
            }

            lastThingsData = thingsFromAutoMode;
            renderThings(lastThingsData);
        },
        error: function () {
            autoModeResult.textContent = "Ошибка при выполнении автоматического режима";
        }
    });
}

function startAutoUpdate() {
    updateData();

    updateInterval = setInterval(updateData, 3000);
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
    if (autoModeEnabled) {
        alert("Автообновление недоступно в автоматическом режиме");
        return;
    }

    if (autoUpdateEnabled) {
        stopAutoUpdate();
    } else {
        startAutoUpdate();
    }
}
function startAutoMode() {
    if (autoUpdateEnabled) {
        stopAutoUpdate();
    }

    autoModeEnabled = true;
    autoModeButton.textContent = "Автоматический режим: включен";

    updateAutoRally();
    autoModeInterval = setInterval(updateAutoRally, 3000);

    renderThings(lastThingsData);
}


function stopAutoMode() {
    clearInterval(autoModeInterval);
    autoModeInterval = null;

    autoModeEnabled = false;
    autoModeButton.textContent = "Автоматический режим: выключен";

    autoModeResult.textContent = "Автоматический режим не запущен";

    renderThings(lastThingsData);
}


function toggleAutoMode() {
    if (autoModeEnabled) {
        stopAutoMode();
    } else {
        startAutoMode();
    }
}


toggleButton.onclick = toggleAutoUpdate;
autoModeButton.onclick = toggleAutoMode;

startAutoUpdate();
stopAutoUpdate();

// Блок управления
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
// Отображение блока управления для динамиков и табло
function renderControls(thing, controlsContainer) {
    controlsContainer.innerHTML = "";

    if (autoModeEnabled) {
        const p = document.createElement("p");
        p.className = "auto-mode-note";
        p.textContent = "Ручное управление скрыто: устройство управляется главным контроллером.";
        controlsContainer.appendChild(p);
        return;
    }

    if (thing.deviceName === "speaker") {
        renderSpeakerControls(controlsContainer);
    }

    if (thing.deviceName === "scoreboard") {
        renderScoreboardControls(controlsContainer);
    }
}
function renderSpeakerControls(controlsContainer) {
    const template = document.getElementById("speaker_controls_template");
    const controls = template.content.cloneNode(true);

    const soundTypeInput = controls.querySelector(".speaker-sound-type");
    const durationInput = controls.querySelector(".speaker-duration");
    const playButton = controls.querySelector(".speaker-play-btn");

    const volumeInput = controls.querySelector(".speaker-volume");
    const volumeButton = controls.querySelector(".speaker-volume-btn");

    playButton.onclick = function () {
        controlSpeaker({
            command: "play_signal",
            sound_type: soundTypeInput.value,
            duration: durationInput.value
        });
    };

    volumeButton.onclick = function () {
        controlSpeaker({
            command: "set_volume",
            volume: volumeInput.value
        });
    };

    controlsContainer.appendChild(controls);
}
function controlSpeaker(data) {
    $.ajax({
        type: "GET",
        url: "/control_speaker",
        dataType: "json",
        data: data,
        success: function (response) {
            console.log(response);
            updateData();
        },
        error: function () {
            alert("Ошибка при отправке команды звуковой системе");
        }
    });
}
function renderScoreboardControls(controlsContainer) {
    const template = document.getElementById("scoreboard_controls_template");
    const controls = template.content.cloneNode(true);

    const scoreTypeInput = controls.querySelector(".score-type");
    const player1ScoreInput = controls.querySelector(".player1-score");
    const player2ScoreInput = controls.querySelector(".player2-score");
    const updateScoreButton = controls.querySelector(".score-update-btn");

    const matchStatusInput = controls.querySelector(".match-status");
    const matchStatusButton = controls.querySelector(".match-status-btn");
    const resetScoreButton = controls.querySelector(".score-reset-btn");

    updateScoreButton.onclick = function () {
        controlScoreboard({
            command: "update_score",
            score_type: scoreTypeInput.value,
            player1_score: player1ScoreInput.value,
            player2_score: player2ScoreInput.value
        });
    };

    matchStatusButton.onclick = function () {
        controlScoreboard({
            command: "set_match_status",
            match_status: matchStatusInput.value
        });
    };

    resetScoreButton.onclick = function () {
        controlScoreboard({
            command: "reset_score"
        });
    };

    controlsContainer.appendChild(controls);
}


function controlScoreboard(data) {
    $.ajax({
        type: "GET",
        url: "/control_scoreboard",
        dataType: "json",
        data: data,
        success: function (response) {
            console.log(response);
            updateData();
        },
        error: function () {
            alert("Ошибка при отправке команды табло");
        }
    });
}
function renderInactiveMessage(thing, container) {
    container.innerHTML = "";

    const p = document.createElement("p");

    if (thing.status === "offline") {
        p.textContent = "Устройство отключено. Для просмотра данных и управления включите его.";
    } else if (thing.status === "maintenance") {
        p.textContent = "Устройство находится на обслуживании. Управление временно недоступно.";
    } else {
        p.textContent = "Устройство недоступно.";
    }

    container.appendChild(p);
}