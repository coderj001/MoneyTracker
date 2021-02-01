const searchField = document.querySelector('#searchField');

searchField.addEventListener("keyup", (e) => {
    const searchData = e.target.value;
    if (searchData.trim().length > 0) {
        fetch("/search_expenses", {
            body: JSON.stringify({searchText: searchData}),
            method: "POST",
        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
            })
    } else {

    }
})

function searchFill(dataList) {
    // TODO:  <01-02-21, coderj001> // create tbody
}
