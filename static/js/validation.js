export function applyErrorAttribute(id, msg) {
  const field = document.getElementById(id);
  const fieldLabel = document.getElementById(id + "-label");
  const labelAttribute = document.createAttribute("data-error");
  const inputAttribute = document.createAttribute("has-error");

  labelAttribute.value = msg;
  inputAttribute.value = "true";
  field.setAttributeNode(inputAttribute);
  fieldLabel.setAttributeNode(labelAttribute);
}

export const validation = {
  validateLandAdvance: (landAdvance) => {
    let valid = true;
    if (isNaN(landAdvance) || landAdvance === "") {
      applyErrorAttribute("land-advance", "please enter a number");
      valid = false;
    } else if (parseFloat(landAdvance) < 0) {
      applyErrorAttribute(
        "land-advance",
        "land advance needs to be a positive"
      );
      valid = false;
    }

    return valid;
  },
  validateMonthlyRate: (monthRate) => {
    let valid = true;
    if (isNaN(monthRate) || monthRate === "") {
      applyErrorAttribute("contractual-monthly-rate", "please enter a number");
      valid = false;
    } else if (parseFloat(monthRate) < 0) {
      applyErrorAttribute(
        "contractual-monthly-rate",
        "monthly rate needs to be a positive"
      );
      valid = false;
    }

    return valid;
  },
  validateDates: (date1, date2) => {
    let valid = true;
    if (date1 === "") {
      const message = "please enter a date";
      applyErrorAttribute("beginning-of-default-period", message);
      valid = false;
    }

    if (date2 === "") {
      const message = "please enter a date";
      applyErrorAttribute("end-of-default-period", message);
      valid = false;
    }

    if (date !== "" && date !== "" && new Date(date1) > new Date(date2)) {
      const message =
        "Beginning of default period must be before the end of default period";
      applyErrorAttribute("beginning-of-default-period", message);
      applyErrorAttribute("end-of-default-period", message);
      valid = false;
    }

    return valid;
  },
};
