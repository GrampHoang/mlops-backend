// const modelURL = "http://localhost:5000/model";
// const predURL  = "http://localhost:5000/predict";
const modelURL = "model";
const predURL  = "predict";

 // make the API call to fetch the list of models
 fetch(modelURL)
    .then(response => response.json())
    .then(data => {
    // update the options of the select element with the fetched data
    const selectElement = document.getElementById('model_choice');
    data.forEach(model => {
        const optionElement = document.createElement('option');
        optionElement.textContent = model;
        selectElement.appendChild(optionElement);
    });
    }, { mode: 'no-cors' })
    .catch(error => console.error(error));

document.addEventListener("DOMContentLoaded", function(event) {
    document.querySelectorAll('img').forEach(function(img){
        img.onerror = function(){this.style.display='none';};
    })
    });

    const form = document.querySelector('#myform');
    const submitBtn = document.querySelector('#submit-btn');
    const jsonOutput = document.getElementById('jsoninfo');
    const stringOutput = document.getElementById('outstr');
    // const modelSelect = document.getElementById('model_choice');
    // const selectedModel = "no";
    // modelSelect.addEventListener('change', (event) => {
    // 	const selectedModel = event.target.value;
    // });

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = document.querySelector('#inputfile').files[0];
    const modelSelect = document.getElementById('model_choice');
    const selectedModel = modelSelect.value;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model', selectedModel);

    const response = await fetch(predURL, {
        method: 'POST',
        body: formData
        });
    const jsonres = await response.json();

    const resultImgData = jsonres.result_img;
    const resultImg = document.getElementById('ItemPreview');
    resultImg.src = 'data:image/png;base64,' + resultImgData;
    
    console.log(resultImg);
    console.log(jsonOutput);
    
    jsonOutput.innerHTML = jsonres.results;
    stringOutput.innerHTML = jsonres.result_str;
    
    document.getElementById("jsoninfo").style.display = "block";
    document.getElementById("outstr").style.display = "block";
    document.getElementById("ItemPreview").style.display = "block";
});