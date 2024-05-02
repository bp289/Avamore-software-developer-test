import { validInputs } from "./validation.js"; //extra validation in case of unsupported browser (when the html validation isnt for the browser in use.)

const URL = "/ARMresult";

// event listeners to interact with inputs and
document.getElementById("submit").addEventListener("click", (event) => {
  event.preventDefault();
  submitData();
});

document.querySelectorAll("input").forEach((input) =>
  input.addEventListener("change", (event) => {
    removeAttributes(event.target);
  })
);

document.getElementById("reset").addEventListener("click", (event) => {
  event.preventDefault();
  clearFields();
});

document.querySelectorAll("input").forEach((input) =>
  input.addEventListener("keypress", (event) => {
    removeAttributes(event.target);
  })
);

//document interaction functions
function removeAttributes(target) {
  target.removeAttribute("has-error");
  document.getElementById(target.id + "-label").removeAttribute("data-error");
}

function paintResult({
  total_interest_due,
  implied_daily_default_rate,
  implied_daily_regular_rate,
  implied_regular_annual_rate,
}) {
  document.getElementById(
    "interest-value"
  ).textContent = `${total_interest_due}`;
  document.getElementById(
    "daily-default-rate-value"
  ).textContent = `${implied_daily_default_rate} %`;
  document.getElementById(
    "daily-regular-rate-value"
  ).textContent = `${implied_daily_regular_rate} %`;
  document.getElementById(
    "regular-annual-rate-value"
  ).textContent = `${implied_regular_annual_rate} %`;

  showOutputs();
}

//querying and running python script with inputs
async function submitData() {
  const input = new FormData(document.getElementById("arm-form"));

  if (validInputs(input)) {
    getARMresult(input);
  }
}

async function getARMresult(input) {
  const data = { input: Object.fromEntries(input) };

  const response = await fetch(URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const result = await response.json();

  paintResult(result);
}

function clearFields() {
  const inputs = document.querySelectorAll("input, textarea");
  inputs.forEach((input) => {
    input.value = "";
  });
  hideOutputs();

  document
    .querySelectorAll("input")
    .forEach((input) => removeAttributes(input));
}

function hideOutputs() {
  const output = document.querySelectorAll(".output");
  const outputContainer = document.getElementById("output-container");
  outputContainer.classList.remove("expand");
  output.forEach((node) => node.classList.remove("visible"));
}

function showOutputs() {
  const output = document.querySelectorAll(".output");
  const outputContainer = document.getElementById("output-container");
  outputContainer.classList.add("expand");
  output.forEach((node) => node.classList.add("visible"));
}
