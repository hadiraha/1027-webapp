async function loadData() {
  const token = localStorage.getItem("token");
  const res = await fetch("/companies/", {
    headers: { "Authorization": "Bearer " + token }
  });

  const data = await res.json();
  $("#tbl").DataTable({
    data,
    destroy: true,
    columns: [
      { data: "id" },
      { data: "index" },
      { data: "name_fa" },
      { data: "name_en" },
      { data: "website" },
      { data: "file_number" },
      { data: "sector" },
      { data: "country" }
    ],
    initComplete: function () {
      let api = this.api();

      api.columns().every(function (index) {
        let column = this;
        $("thead tr.filters th:eq(" + index + ") input").on("keyup change", function () {
          column.search(this.value).draw();
        });
      });
    }
  });
}


loadData();

async function uploadExcel(){
  const file = document.getElementById("file").files[0];
  const form = new FormData();
  form.append("file", file);

  const res = await fetch("/companies/upload", {
    method: "POST",
    body: form
  });

  alert("Import success, refresh dashboard");
  location.reload();
}

function logout(){
  localStorage.removeItem("token");
  window.location = "/login";
}

async function uploadExcel() {
  const fileInput = document.getElementById("file");
  if (!fileInput.files.length) return alert("Please select file");

  const form = new FormData();
  form.append("file", fileInput.files[0]);

  const token = localStorage.getItem("token");

  const res = await fetch("/companies/upload", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + token
    },
    body: form
  });

  const data = await res.json();
  alert("Imported: " + data.imported_rows + " rows");

  loadCompanies();
}
