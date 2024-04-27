const URL = "/ARMresult";

async function submitCode() {
  const input = new FormData(document.getElementById("arm-form"));

  console.log(input.land_advance);
  console.log(input);
  // const data = { input: input };
  // const result = await fetch(URL, {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify(data),
  // });

  // const gaming = await result.json();
}

// Add an event listener to the submit button
document.getElementById("submit").addEventListener("click", function (event) {
  event.preventDefault();
  submitCode();
});
