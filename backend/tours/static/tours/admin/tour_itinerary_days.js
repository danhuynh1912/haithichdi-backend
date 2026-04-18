(function () {
  const START_DATE_INPUT_ID = "id_start_date";
  const END_DATE_INPUT_ID = "id_end_date";

  function parseDateFromInput(value) {
    if (!value) return null;
    const parts = value.split("-").map(Number);
    if (parts.length !== 3) return null;
    const [year, month, day] = parts;
    if (!year || !month || !day) return null;
    return new Date(year, month - 1, day);
  }

  function getInlineGroup() {
    return (
      document.querySelector("#touritineraryday_set-group") ||
      document.querySelector("#itinerary_days-group")
    );
  }

  function getRows(group) {
    return Array.from(group.querySelectorAll(".inline-related")).filter((row) => {
      if (row.classList.contains("empty-form")) return false;
      return !!row.querySelector('input[name$="-day_number"]');
    });
  }

  function getActiveRows(group) {
    return getRows(group).filter((row) => {
      const deleteInput = row.querySelector('input[name$="-DELETE"]');
      return !(deleteInput && deleteInput.checked);
    });
  }

  function addRow(group) {
    const addButton = group.querySelector(".add-row a");
    if (!addButton) return false;
    addButton.click();
    return true;
  }

  function formatDate(dateValue) {
    const day = String(dateValue.getDate()).padStart(2, "0");
    const month = String(dateValue.getMonth() + 1).padStart(2, "0");
    const year = dateValue.getFullYear();
    return `${day}/${month}/${year}`;
  }

  function titleForDay(dayNumber, startDate) {
    const dayDate = new Date(startDate.getTime());
    dayDate.setDate(dayDate.getDate() + dayNumber - 1);
    return `Day ${dayNumber} - ${formatDate(dayDate)}`;
  }

  function markRowsOutOfRange(rows, requiredCount) {
    for (let index = requiredCount; index < rows.length; index += 1) {
      const row = rows[index];
      const deleteInput = row.querySelector('input[name$="-DELETE"]');
      if (deleteInput && !deleteInput.checked) {
        deleteInput.checked = true;
        deleteInput.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }
  }

  function syncItineraryRows() {
    const group = getInlineGroup();
    if (!group) return;

    const startInput = document.getElementById(START_DATE_INPUT_ID);
    const endInput = document.getElementById(END_DATE_INPUT_ID);
    if (!startInput || !endInput) return;

    const startDate = parseDateFromInput(startInput.value);
    const endDate = parseDateFromInput(endInput.value);
    if (!startDate || !endDate || endDate < startDate) return;

    const diffMs = endDate.getTime() - startDate.getTime();
    const totalDays = Math.floor(diffMs / (24 * 60 * 60 * 1000)) + 2;
    if (totalDays <= 0) return;

    let activeRows = getActiveRows(group);
    while (activeRows.length < totalDays) {
      const added = addRow(group);
      if (!added) break;
      activeRows = getActiveRows(group);
    }

    activeRows.slice(0, totalDays).forEach((row, index) => {
      const dayInput = row.querySelector('input[name$="-day_number"]');
      const titleInput = row.querySelector('input[name$="-title"]');

      if (dayInput) {
        dayInput.value = String(index);
        dayInput.readOnly = true;
      }
      if (titleInput && !titleInput.value.trim()) {
        titleInput.value = titleForDay(index, startDate);
      }
    });

    markRowsOutOfRange(activeRows, totalDays);
  }

  function bindEvents() {
    const startInput = document.getElementById(START_DATE_INPUT_ID);
    const endInput = document.getElementById(END_DATE_INPUT_ID);
    if (!startInput || !endInput) return;

    startInput.addEventListener("change", syncItineraryRows);
    endInput.addEventListener("change", syncItineraryRows);
    startInput.addEventListener("input", syncItineraryRows);
    endInput.addEventListener("input", syncItineraryRows);
  }

  window.addEventListener("load", function () {
    bindEvents();
    syncItineraryRows();
  });
})();
