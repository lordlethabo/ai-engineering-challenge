let scene, camera, renderer, controls, currentModel;

init();

// ---------- INIT ----------
function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x111111);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / 500, 0.1, 1000);

    renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById("canvas"),
        antialias: true
    });

    renderer.setSize(window.innerWidth * 0.8, 400);

    camera.position.set(0, 1, 5);

    // 🔥 Orbit Controls (INTERACTIVITY)
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Lighting
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(3, 3, 3);
    scene.add(light);

    scene.add(new THREE.AmbientLight(0xffffff, 0.4));

    animate();
}

// ---------- LOOP ----------
function animate() {
    requestAnimationFrame(animate);

    if (currentModel) {
        currentModel.rotation.y += 0.005;
    }

    controls.update();
    renderer.render(scene, camera);
}

// ---------- GENERATE ----------
async function generate() {
    const text = document.getElementById("inputText").value;
    const status = document.getElementById("status");

    if (!text) {
        alert("Enter something.");
        return;
    }

    status.innerText = "⚡ Generating...";

    try {
        const res = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text })
        });

        const data = await res.json();

        if (data.error) {
            status.innerText = "❌ Error";
            return;
        }

        document.getElementById("explanation").innerText = data.explanation;

        loadModel(data.model_url);

        status.innerText = "✅ Model Loaded";

    } catch (e) {
        console.error(e);
        status.innerText = "❌ Backend error";
    }
}

// ---------- LOAD MODEL ----------
function loadModel(url) {
    const loader = new THREE.GLTFLoader();

    if (currentModel) scene.remove(currentModel);

    loader.load(url, (gltf) => {
        currentModel = gltf.scene;

        // 🔥 AUTO SCALE + CENTER (IMPORTANT FOR TEST)
        const box = new THREE.Box3().setFromObject(currentModel);
        const size = box.getSize(new THREE.Vector3()).length();
        const center = box.getCenter(new THREE.Vector3());

        currentModel.position.sub(center);
        currentModel.scale.multiplyScalar(2 / size);

        scene.add(currentModel);

    }, undefined, (err) => {
        console.error(err);
        alert("Model failed to load");
    });
}

// ---------- AVATAR ----------
async function controlAvatar() {
    const text = document.getElementById("avatarCommand").value;
    const status = document.getElementById("avatarStatus");

    if (!text) {
        alert("Enter command");
        return;
    }

    status.innerText = "⚡ Thinking...";

    try {
        const res = await fetch("http://127.0.0.1:5000/animate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text })
        });

        const data = await res.json();

        document.getElementById("avatarExplanation").innerText = data.explanation;

        playAnimation(data.action);

        status.innerText = "✅ Done";

    } catch (e) {
        console.error(e);
        status.innerText = "❌ Error";
    }
}

// ---------- FAKE ANIMATION (for now) ----------
function playAnimation(action) {
    const map = {
        walk: "🚶 Walking",
        wave: "👋 Waving",
        point: "👉 Pointing",
        idle: "🧍 Idle"
    };

    alert(map[action] || "Unknown action");
}
