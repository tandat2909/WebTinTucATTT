function delUser(idu, btn) {
    fetch('/admin/lock/user', {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idu": idu,
            "lock": btn.value
        })
    }).then(res => res.json()).then(data => {

        if (data.status == 200) {

            btn.innerHTML = data.data;
            btn.value = data.data;
            btn.parentElement.parentElement.parentElement.children[0].children[1].innerHTML = (data.data == "lock" ? "Active" : "InActive")
            alert(data.data + " Success");
        }


    })
}

