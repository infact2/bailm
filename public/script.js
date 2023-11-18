const cursor = "█";

function generate() {
    let input = document.querySelector("#input");
    if (input.disabled) return;

    document.getElementById("generate-btn").disabled = true;

    $.post(`/generate/${input.value.replace("/", "%2F")}`, async function (data, status) {
        console.log("balls2");
        await output(data);
        document.getElementById("generate-btn").disabled = false;
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
        await delay(50);
    }
    output.innerHTML = output.innerHTML.replace(cursor, "");
}