const orginal_tbody = document.querySelector("#table-tbody-data");

searchField.addEventListener("keyup", (e) => {
  const searchData = e.target.value;
  if (searchData.trim().length > 0) {
    fetch("/income/search_income", {
      body: JSON.stringify({ searchText: searchData }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        deleteSearch();
        hide_table();
        searchFill(data);
      });
  } else {
    deleteSearch();
    show_table();
  }
});

function searchFill(dataList) {
  let tbody = document.createElement("tbody");
  tbody.setAttribute("id", "table-tbody");
  dataList.forEach((data) => {
    let tr = document.createElement("tr");
    let th1 = document.createElement("th");
    th1.append(data["amount"]);
    tr.append(th1);
    let th2 = document.createElement("th");
    th2.append(data["source"]);
    tr.append(th2);
    let th3 = document.createElement("th");
    th3.append(data["description"]);
    tr.append(th3);
    let th4 = document.createElement("th");
    th4.append(data["date"]);
    tr.append(th4);
    let th5 = document.createElement("th");
    let a1 = document.createElement("a");
    a1.setAttribute("href", "edit_income/" + data["id"] + "/");
    a1.setAttribute("class", "link-primary");
    a1.append("edit");
    th5.append(a1);
    tr.append(th5);
    let th6 = document.createElement("th");
    let a2 = document.createElement("a");
    a2.setAttribute("href", "delete_income/" + data["id"] + "/");
    a2.setAttribute("class", "link-danger");
    a2.append("delete");
    th6.append(a2);
    tr.append(th6);
    tbody.append(tr);
  });
  deleteSearch();
  const table = document.querySelector("#table-data");
  table.append(tbody);
}

function deleteSearch() {
  let tbody1 = document.querySelector("#table-tbody");
  if (tbody1) {
    tbody1.remove();
  }
}

function hide_table() {
  orginal_tbody.classList.add("visually-hidden");
}

function show_table() {
  orginal_tbody.classList.remove("visually-hidden");
}
