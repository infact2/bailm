const cursor = "█";

window.onerror = (event) => {
    alert(event);
}

function base64ToBytes(base64) {
    const binString = atob(base64);
    return Uint8Array.from(binString, (m) => m.codePointAt(0));
}

function bytesToBase64(bytes) {
    const binString = String.fromCodePoint(...bytes);
    return btoa(binString);
}

function generate() {
    let input = document.querySelector("#input");
    if (input.disabled) return;

    document.getElementById("generate-btn").disabled = true;
    document.getElementById("generate-btn").innerHTML = "(Please Wait)";
    document.getElementById("loading").style.display = "unset";

    $.post(`/generate/${input.value.replace("/", "%2F")}/${document.getElementById("sentences").value}/${document.getElementById("training-document").value}`, async function (data, status) {
        console.log("balls2");
        await output(data);
        document.getElementById("generate-btn").disabled = false;
        document.getElementById("generate-btn").innerHTML = "Generate";
        document.getElementById("loading").style.display = "none";
    })
}

function delay(ms) { 
    return new Promise(resolve => { 
        setTimeout(() => { resolve('') }, ms); 
    }) 
}

async function output(input) {
    let output = document.querySelector("#output");
    output.innerHTML = cursor;

    for (let i = 0; i < input.length; i++) {
        output.innerHTML = output.innerHTML.replace(cursor, "");
        output.innerHTML += input[i] + cursor;
        await delay(15);
    }
    output.innerHTML = output.innerHTML.replace(cursor, "");
}

function openAsLink() {
    // window.open("https://www.google.com")
    let data = bytesToBase64(new TextEncoder().encode(document.getElementById("output").innerText));

    // let tab = window.open("about:blank");
    // tab.document.write() = data;
    // // window.location.href = data;

    window.open(`/preview/${data}`);
}