let skins = [];
for (let i = 0; i < 64; i++) {
  skins.push('../skins/' + i + '.png');
}

let caption = null;
let xmlhttp = new XMLHttpRequest();
xmlhttp.open("GET", '../skins/caption.txt', false);
xmlhttp.send();
if (xmlhttp.status==200) {
  caption = xmlhttp.responseText;
}

document.getElementById('caption').appendChild(document.createTextNode(caption));

// MAIN CANVAS
if (skins.length === 0) {
  console.log('No skins found');
  process.exit(1);
}
let skinViewer = new skinview3d.SkinViewer({
  canvas: document.getElementById('main-canvas'),
  width: 400,
  height: 600,
  skin: skins[0]
});

skinViewer.fov = 70;
skinViewer.zoom = 0.5;

let control = skinview3d.createOrbitControls(skinViewer);
control.enableRotate = true;
control.enableZoom = true;
control.enablePan = false;

// SKIN SELECTOR
let skinSelector = document.getElementById('offscreen-skins-container');

(async function () {
  const offscreenSkinViewer = new skinview3d.FXAASkinViewer({
      width: 200,
      height: 300,
      renderPaused: true
  });
  
  offscreenSkinViewer.camera.rotation.x = -0.620;
  offscreenSkinViewer.camera.rotation.y = 0.534;
  offscreenSkinViewer.camera.rotation.z = 0.348;
  offscreenSkinViewer.camera.position.x = 30.5;
  offscreenSkinViewer.camera.position.y = 22.0;
  offscreenSkinViewer.camera.position.z = 42.0;

  for (const skin of skins) {
    await Promise.all([
        offscreenSkinViewer.loadSkin(skin)
    ]);
    offscreenSkinViewer.render();
    const image = offscreenSkinViewer.canvas.toDataURL();
    const imgElement = document.createElement("img");
    imgElement.src = image;
    imgElement.width = offscreenSkinViewer.width;
    imgElement.height = offscreenSkinViewer.height;
    imgElement.classList.add('offscreen-skin');
    imgElement.addEventListener('click', () => {
      skinViewer.loadSkin(skin);
    });
    document.getElementById("offscreen-skins-container").appendChild(imgElement);
  }
  offscreenSkinViewer.dispose();
})();