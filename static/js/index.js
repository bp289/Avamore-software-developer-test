const URL = "/ARMresult";

//extra validation in case of unsupported browser (when the html validation isnt for the browser in use.)
const validation = {
  validateLandAdvance: (landAdvance) => {
    if (!isNaN(landAdvance)) {
      throw new Error("land-advance;value needs to be a number");
    }
    if (parseFloat(monthRate) < 0) {
      throw new Error(
        "contractual-monthly-rate;land advance needs to be a positive"
      );
    }
  },
  validateMonthlyRate: (monthRate) => {
    if (!isNaN(monthRate)) {
      throw new Error("contractual-monthly-rate;value needs to be a number");
    }
    if (parseFloat(monthRate) < 0) {
      throw new Error(
        "contractual-monthly-rate;monthly rate needs to be a positive"
      );
    }
  },
  validateDates: (date1, date2) => {
    if (new Date(date1) > new Date(date2)) {
      throw new Error(
        "beginning-of-default-period;Beginning of default period must be before the end of default period"
      );
    }
  },
};

async function submitCode() {
  const input = new FormData(document.getElementById("arm-form"));

  console.log(input);

  try {
    validation.validateMonthlyRate(input.get("contractual-monthly-rate"));
    validation.validateDates(
      input.get("beginning-of-default-period"),
      input.get("end-of-default-period")
    );
  } catch (e) {
    [field, message] = e.message.split(";");
    document.getElementById;
  }

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
