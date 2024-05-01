import validation from "./validation.js";

const URL = "/ARMresult";

//extra validation in case of unsupported browser (when the html validation isnt for the browser in use.)

async function submitData() {
  const input = new FormData(document.getElementById("arm-form"));
  console.log(input);
  validation.validateLandAdvance(input.get("land-advance"));

  validation.validateMonthlyRate(input.get("contractual-monthly-rate"));
  validation.validateDates(
    input.get("beginning-of-default-period"),
    input.get("end-of-default-period")
  );

  //const result = await getARMresult(input);
}

async function getARMresult(input) {
  const data = { input: input };
  const result = await fetch(URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return await result.json();
}

// Add an event listener to the submit button
document.getElementById("submit").addEventListener("click", (event) => {
  event.preventDefault();

  submitData();
});
