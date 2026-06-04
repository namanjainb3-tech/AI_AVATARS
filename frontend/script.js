console.log("SCRIPT LOADED");

// ==========================
// IMAGE PREVIEW
// ==========================
document
    .getElementById("image")
    .addEventListener("change", function(e){

    const file = e.target.files[0];

    const preview =
        document.getElementById("preview");

    if(file){

        preview.src =
            URL.createObjectURL(file);

        preview.classList.remove("hidden");
    }
});

// ==========================
// VOICE PREVIEW TEXT
// ==========================
document
    .getElementById("voice")
    .addEventListener("change", function(e){

    const file = e.target.files[0];

    const labels =
        document.querySelectorAll(".upload-box span");

    if(file){

        labels[1].innerHTML =
            `✅ ${file.name}`;
    }
});

// ==========================
// GENERATE AVATAR
// ==========================
async function generateAvatar(){

    console.log("BUTTON CLICKED");

    const result =
        document.getElementById("result");

    try{

        // ==========================
        // INPUTS
        // ==========================
        const image =
            document
            .getElementById("image")
            .files[0];

        const voice =
            document
            .getElementById("voice")
            .files[0];

        const text =
            document
            .getElementById("text")
            .value
            .trim();

        // ==========================
        // VALIDATION
        // ==========================
        if(!image || !voice || !text){

            result.innerHTML = `
                <div class="error-box">
                    Please upload:
                    <br><br>
                    📸 Face Image
                    <br>
                    🎙 Voice Sample
                    <br>
                    ✍ Script
                </div>
            `;

            return;
        }

        // ==========================
        // FORM DATA
        // ==========================
        const formData = new FormData();

        formData.append("image", image);

        formData.append("voice", voice);

        formData.append("text", text);

        // ==========================
        // MODERN LOADING UI
        // ==========================
        result.innerHTML = `

        <div class="progress-card">

            <div class="live-header">

                <div class="live-dot"></div>

                <span>
                    AI Engine Active
                </span>

            </div>

            <div class="progress-top">

                <p id="stepText">
                    Uploading assets...
                </p>

                <span id="percentText">
                    0%
                </span>

            </div>

            <div class="bar">

                <div id="fill"></div>

            </div>

            <div class="eta">

                ⏳ Estimated time remaining:
                <span id="etaText">
                    ~2 min
                </span>

            </div>

            <div class="steps">

                <div class="step active" id="s1">

                    <div class="step-left">
                        📤 Uploading assets
                    </div>

                    <div class="step-status">
                        ACTIVE
                    </div>

                </div>

                <div class="step" id="s2">

                    <div class="step-left">
                        🖼 Enhancing portrait
                    </div>

                    <div class="step-status">
                        WAITING
                    </div>

                </div>

                <div class="step" id="s3">

                    <div class="step-left">
                        🎙 Cloning realistic voice
                    </div>

                    <div class="step-status">
                        WAITING
                    </div>

                </div>

                <div class="step" id="s4">

                    <div class="step-left">
                        🧠 Initializing AI presenter
                    </div>

                    <div class="step-status">
                        WAITING
                    </div>

                </div>

                <div class="step" id="s5">

                    <div class="step-left">
                        🎬 Rendering final avatar
                    </div>

                    <div class="step-status">
                        WAITING
                    </div>

                </div>

            </div>

        </div>
        `;

        // ==========================
        // SEND REQUEST
        // ==========================
        const res = await fetch(
            "http://localhost:8000/generate-avatar",
            {
                method: "POST",
                body: formData
            }
        );

        if(!res.ok){

            throw new Error(
                `HTTP Error: ${res.status}`
            );
        }

        const data = await res.json();

        console.log("JOB:", data);

        // ==========================
        // START LIVE STATUS
        // ==========================
        checkJobStatus(
            data.job_id,
            text
        );

    }catch(error){

        console.error(error);

        result.innerHTML = `

            <div class="error-box">

                ❌ ${error}

            </div>
        `;
    }
}

// ==========================
// LIVE STATUS SYSTEM
// ==========================
async function checkJobStatus(
    jobId,
    text
){

    const interval =
        setInterval(async () => {

        try{

            const res = await fetch(
                `http://localhost:8000/job-status/${jobId}`
            );

            const data =
                await res.json();

            console.log(data);

            const status =
                data.status;

            updateUI(status);

            // ==========================
            // COMPLETED
            // ==========================
            if(status === "completed"){

                clearInterval(interval);

                document
                    .getElementById("fill")
                    .style.width = "100%";

                document
                    .getElementById("percentText")
                    .innerText = "100%";

                document
                    .getElementById("etaText")
                    .innerText = "Completed";

                document
                    .querySelectorAll(".step")
                    .forEach(el => {

                    el.classList.add("done");

                    const badge =
                        el.querySelector(
                            ".step-status"
                        );

                    badge.innerHTML =
                        "DONE";
                });

                document
                    .getElementById("result")
                    .innerHTML = `

                    <div class="premium-box">

                        <div class="success-badge">

                            ✨ GENERATED SUCCESSFULLY

                        </div>

                        <h3 class="success-title">

                            Premium AI Avatar Ready

                        </h3>

                        <video
                            controls
                            autoplay
                            class="final-video"
                        >

                            <source
                                src="${data.video_url}"
                                type="video/mp4"
                            >

                        </video>

                        <div class="caption-box">

                            <span id="captionText"></span>

                        </div>

                    </div>
                `;

                typeCaptions(text);
            }

            // ==========================
            // FAILED
            // ==========================
            if(status === "failed"){

                clearInterval(interval);

                document
                    .getElementById("result")
                    .innerHTML = `

                    <div class="error-box">

                        ❌ Avatar generation failed

                    </div>
                `;
            }

        }catch(err){

            console.log(err);

        }

    }, 3000);
}

// ==========================
// UPDATE UI
// ==========================
function updateUI(status){

    const fill =
        document.getElementById("fill");

    const percentText =
        document.getElementById("percentText");

    const stepText =
        document.getElementById("stepText");

    const etaText =
        document.getElementById("etaText");

    const map = {

        pending: {
            progress:15,
            text:"Uploading assets...",
            eta:"~2 min",
            step:"s1"
        },

        enhancing: {
            progress:35,
            text:"Enhancing portrait...",
            eta:"~90 sec",
            step:"s2"
        },

        voice_generation: {
            progress:55,
            text:"Generating cloned voice...",
            eta:"~60 sec",
            step:"s3"
        },

        animation: {
            progress:78,
            text:"Initializing AI presenter...",
            eta:"~35 sec",
            step:"s4"
        },

        rendering: {
            progress:92,
            text:"Rendering final avatar...",
            eta:"~10 sec",
            step:"s5"
        }
    };

    const current =
        map[status];

    if(!current) return;

    fill.style.width =
        current.progress + "%";

    percentText.innerText =
        current.progress + "%";

    stepText.innerText =
        current.text;

    etaText.innerText =
        current.eta;

    document
        .querySelectorAll(".step")
        .forEach(el => {

        el.classList.remove("active");
    });

    const activeStep =
        document.getElementById(
            current.step
        );

    activeStep.classList.add(
        "active"
    );

    // MARK PREVIOUS AS DONE
    const order = [
        "s1",
        "s2",
        "s3",
        "s4",
        "s5"
    ];

    const currentIndex =
        order.indexOf(current.step);

    order.forEach((id, index) => {

        const step =
            document.getElementById(id);

        const badge =
            step.querySelector(
                ".step-status"
            );

        if(index < currentIndex){

            step.classList.add("done");

            badge.innerHTML = "DONE";
        }

        else if(index === currentIndex){

            badge.innerHTML = "ACTIVE";
        }

        else{

            badge.innerHTML = "WAITING";
        }
    });
}

// ==========================
// TYPEWRITER
// ==========================
function typeCaptions(text){

    const target =
        document.getElementById(
            "captionText"
        );

    if(!target) return;

    target.innerHTML = "";

    let i = 0;

    const typer =
        setInterval(() => {

        target.innerHTML +=
            text.charAt(i);

        i++;

        if(i >= text.length){

            clearInterval(typer);
        }

    }, 25);
}

// ==========================
// GLOBAL
// ==========================
window.generateAvatar =
    generateAvatar;