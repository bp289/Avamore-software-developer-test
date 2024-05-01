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

document.querySelectorAll("input").forEach((input) =>
  input.addEventListener("keypress", (event) => {
    removeAttributes(event.target);
  })
);

//dom interaction
function removeAttributes(target) {
  target.removeAttribute("has-error");
  document.getElementById(target.id + "-label").removeAttribute("data-error");
}

function paintResult({ total_interest_due, daily_data }) {
  document.getElementById("interest").textContent = `${total_interest_due}`;

  const output = document.getElementById("total-interest");
  const outputContainer = document.getElementById("output-container");
  outputContainer.classList.add("visible");
  output.classList.add("visible");
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
