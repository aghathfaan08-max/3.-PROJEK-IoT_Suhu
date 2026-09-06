const suhu = document.getElementById("suhu");
const kelembapan = document.getElementById("kelembapan");

setInterval(
    function() {
        fetch("https://iotsuhu.vercel.app/suhu", {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {suhu.textContent = "suhu : " + data.suhu + " C", 
            kelembapan.textContent = "kelembapan : " + data.kelembapan + "%"});
    },
    10000);

setInterval(
    function() {
        fetch("https://iotsuhu.vercel.app/suhu/history", {
            method: "GET"
        })
        .then(response => response.json())
        .then(history => {
            const ListSuhu = history.map(item => item.suhu).reverse();
            const ListWaktu = history.map(item => item.waktu).reverse();

            const grafik = document.getElementById("GrafikSuhu");

            new Chart(grafik, {
                type: "line",
                data: {
                    labels: ListWaktu,
                    datasets: [{
                        label: "suhu C",
                        data: ListSuhu
                    }]
                }
            });
        });
    },
    10000);