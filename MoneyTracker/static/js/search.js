const searchField = document.querySelector('#searchField');
const orginal_tbody = document.querySelector('#table-tbody-data');

searchField.addEventListener("keyup", (e) => {
    const searchData = e.target.value;
    if (searchData.trim().length > 0) {
        fetch("/search_expenses", {
            body: JSON.stringify({searchText: searchData}),
            method: "POST",
        })
            .then(res => res.json())
            .then(data => {
                // console.log(data);
                deleteSearch()
                hide_table()
                searchFill(data)
            })
    } else {
        deleteSearch()
        show_table()

    }
})

function searchFill(dataList) {
    let tbody = document.createElement('tbody');
    tbody.setAttribute("id", "table-tbody");
    dataList.forEach((data) => {
        let tr = document.createElement("tr");
        let th1 = document.createElement("th");
        th1.append(data['amount'])
        tr.append(th1)
        let th2 = document.createElement("th");
        th2.append(data['category'])
        tr.append(th2)
        let th3 = document.createElement("th");
        th3.append(data['description'])
        tr.append(th3)
        let th4 = document.createElement("th");
        th4.append(data['date'])
        tr.append(th4)
        tbody.append(tr)
    })
    deleteSearch()
    const table = document.querySelector('#table-data');
    table.append(tbody)
}

function deleteSearch() {
    let tbody1 = document.querySelector('#table-tbody')
    if (tbody1) {
        tbody1.remove()
    }
}

function hide_table() {
    orginal_tbody.classList.add("visually-hidden")
}

function show_table() {
    orginal_tbody.classList.remove("visually-hidden")
}
