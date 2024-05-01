function applyErrorAttribute(id, msg) {
  const field = document.getElementById(id);
  const errorInput = document.createAttribute("data-error");
  errorInput.value = msg;
  field.setAttributeNode(errorInput);
}

const validation = {
  validateLandAdvance: (landAdvance) => {
    if (!isNaN(landAdvance)) {
      applyErrorAttribute("land-advance", "value needs to be a number");
    }
    if (parseFloat(landAdvance) < 0) {
      applyErrorAttribute(
        "land-advance",
        "land advance needs to be a positive"
      );
    }
  },
  validateMonthlyRate: (monthRate) => {
    if (!isNaN(monthRate)) {
      applyErrorAttribute(
        "contractual-monthly-rate",
        "value needs to be a number"
      );
    }
    if (parseFloat(monthRate) < 0) {
      applyErrorAttribute(
        "contractual-monthly-rate",
        "monthly rate needs to be a positive"
      );
    }
  },
  validateDates: (date1, date2) => {
    if (new Date(date1) > new Date(date2)) {
      const message =
        "Beginning of default period must be before the end of default period";
      applyErrorAttribute("beginning-of-default-period", message);
      applyErrorAttribute("end-of-default-period", message);
    }
  },
};

export default validation;
