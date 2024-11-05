function downloadReport(careerId) {
    var semesterId = document.getElementById('semester_id_' + careerId).value;
    var url = '/api/v1/account/career/' + careerId + '/attendees/excel/' + semesterId + '/';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob'; 

    xhr.onload = function () {
        if (this.status === 200) {
            var blob = new Blob([this.response], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
            var contentDisposition = xhr.getResponseHeader('Content-Disposition');
            var filename = "download.xlsx"; 
            if (contentDisposition) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(contentDisposition);
                if (matches != null && matches[1]) { 
                    filename = matches[1].replace(/['"]/g, '');  
                }
            }

            var downloadUrl = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    };

    xhr.send(); 
}
