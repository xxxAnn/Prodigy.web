
container = document.getElementById("mainbox")
var elements = document.getElementsByClassName("draggable");
var moveables = {};

for (i=0; i < elements.length; i++) {
    moveables[elements[i].id] = createMoveable(elements[i])
}

function createMoveable(elemn) {
    let result = {
        main: elemn,
        active: false,
        xOffset: 0,
        yOffset: 0
    }
    for (i = 0; i < elemn.children.length; i++) {
        let v = elemn.children[i];
        console.log(v);
        result[v.id] = v;
    }
    return result
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

        for (const [k1, v1] of Object.entries(v)) {
            if (e.target == v1) {
                v.active = true;
            }
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
        for (const [k1, v1] of Object.entries(v)) {
            if (e.target == v1) {
                return v
            }
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

            setTranslate(v.currentX, v.currentY, v.main);
        }
    }
}

function setTranslate(xPos, yPos, el) {
    el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
}