document.querySelector('.warning-alert').onclick = function () {

            swal({
                    title: "Are you sure?",
                    text: "You will not be able to recover this imaginary file!",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: "Lock it!",
                    closeOnConfirm: false,
                    inputType: "text",
                    inputPlaceholder: "sssssss",
                    inputValue: "id",
                    showLoaderOnConfirm: false,
                },
                function () {
                    swal("Lock!", "Your imaginary file has been deleted!", "success"),
                    document.querySelector("#test").innerHTML = "Unclock"
                });
         };