
container = document.getElementById("mainbox")

var role = {
    dragItem: document.getElementById("role"),
    header: document.getElementById("roleheader"),
    text: document.getElementById("roletext"),
    active: false,
    xOffset: 0,
    yOffset: 0
}
var description ={
    dragItem: document.getElementById("description"),
    header: document.getElementById("descriptionheader"),
    text: document.getElementById("descriptiontext"),
    active: false,
    xOffset: 0,
    yOffset: 0
}

var moveables = {
    descx: description,
    rolex: role
}

container.addEventListener("mousedown", dragStart, false);
container.addEventListener("mouseup", dragEnd, false);
container.addEventListener("mousemove", drag, false);

function dragStart(e) {
    for (const [k, v] of Object.entries(moveables)) {
        v.initialX = e.clientX - v.xOffset;
        v.initialY = e.clientY - v.yOffset;
        if (v.active == true) {
            return
        }
        if (e.target === v.dragItem || e.target === v.header || e.target === v.text) {
            v.active = true;
        }
    }
}

function dragEnd(e) {
    for (const [k, v] of Object.entries(moveables)) {
        v.initialX = v.currentX
        v.initialY = v.currentY
        v.active = false
      }
}

function findObjFromElement(e) {
    for (const [k, v] of Object.entries(moveables)) {
        if (e === v.dragItem || e === v.header || e === v.text) {
            return v
        }
    }
    return NaN
}

function drag(e) {
    for (const [k, v] of Object.entries(moveables)) {
        if (v.active) {
            e.preventDefault();
        
            v.currentX = e.clientX - v.initialX;
            v.currentY = e.clientY - v.initialY;

            v.xOffset = v.currentX;
            v.yOffset = v.currentY;

            setTranslate(v.currentX, v.currentY, v.dragItem);
        }
    }
}

function setTranslate(xPos, yPos, el) {
    el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
}