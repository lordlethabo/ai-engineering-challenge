let scene, camera, renderer, currentModel;

init();

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, 600/400, 0.1, 1000);

    renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById("canvas")
    });

    renderer.setSize(600, 400);

    camera.position.z = 5;

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(1,1,1).normalize();
    scene.add(light);

    animate();
}

function animate() {
    requestAnimationFrame(animate);

    if (currentModel) {
        currentModel.rotation.y += 0.01;
    }

    renderer.render(scene, camera);
}


// -------- SYSTEM 1 --------
async function generate() {
    const text = document.getElementById("inputText").value;

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
}

function loadModel(url) {
    const loader = new THREE.GLTFLoader();

    if (currentModel) {
        scene.remove(currentModel);
    }

    loader.load(url, function (gltf) {
        currentModel = gltf.scene;
        scene.add(currentModel);
    });
}


// -------- SYSTEM 2 --------
async function controlAvatar() {
    const text = document.getElementById("avatarCommand").value;

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
}

function playAnimation(action) {
    alert("Avatar action: " + action);
}
