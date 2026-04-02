let scene, camera, renderer, currentModel;

init();

// ---------- INITIALIZE 3D ----------
function init() {
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, 600 / 400, 0.1, 1000);

    renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById("canvas"),
        antialias: true
    });

    renderer.setSize(600, 400);

    camera.position.z = 5;

    // Lighting
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(1, 1, 1).normalize();
    scene.add(light);

    const ambient = new THREE.AmbientLight(0x404040);
    scene.add(ambient);

    animate();
}

function animate() {
    requestAnimationFrame(animate);

    if (currentModel) {
        currentModel.rotation.y += 0.01;
    }

    renderer.render(scene, camera);
}


// ---------- SYSTEM 1: GENERATE ----------
async function generate() {
    const text = document.getElementById("inputText").value;

    if (!text) {
        alert("Please enter an object.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        document.getElementById("explanation").innerText = data.explanation;

        loadModel(data.model_url);

    } catch (error) {
        console.error(error);
        alert("Error connecting to backend.");
    }
}


// ---------- LOAD 3D MODEL ----------
function loadModel(url) {
    const loader = new THREE.GLTFLoader();

    if (currentModel) {
        scene.remove(currentModel);
    }

    loader.load(
        url,
        function (gltf) {
            currentModel = gltf.scene;

            // Center model
            currentModel.position.set(0, 0, 0);

            scene.add(currentModel);
        },
        undefined,
        function (error) {
            console.error("Error loading model:", error);
        }
    );
}


// ---------- SYSTEM 2: AVATAR ----------
async function controlAvatar() {
    const text = document.getElementById("avatarCommand").value;

    if (!text) {
        alert("Enter a command.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/animate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        document.getElementById("avatarExplanation").innerText = data.explanation;

        playAnimation(data.action);

    } catch (error) {
        console.error(error);
        alert("Error connecting to backend.");
    }
}


// ---------- ANIMATION ----------
function playAnimation(action) {
    console.log("Avatar action:", action);

    // Simulated animation feedback
    alert("Avatar performs: " + action);

    // Future upgrade:
    // 👉 Here you can connect real GLTF animations
}
