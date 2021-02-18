const renderChart = (labels, data) => {
  var ctx = document.getElementById("myChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels, // varible to store
      datasets: [
        {
          label: "Last 6 month expense",
          data: data, // varible to store
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Incomes per catagory",
        fontSize: 19,
      },
      animation: {
        duration: 0, // general animation time
      },
      hover: {
        animationDuration: 0, // duration of animations when hovering an item
      },
      responsiveAnimationDuration: 0, // animation duration after a resize
    },
  });
};

const getChartData = () => {
  fetch("/income/income_source_summery")
    .then((res) => res.json())
    .then((result) => {
      // console.log("result: ", result);
      const catagory_data = result.income_source_data;
      const [label, data] = [
        Object.keys(catagory_data),
        Object.values(catagory_data),
      ];
      renderChart(label, data);
    });
};

getChartData();
