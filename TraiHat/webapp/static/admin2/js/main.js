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

            btn.innerHTML = data.data + " Account";
            btn.value = data.data.toLowerCase();
            btn.parentElement.parentElement.parentElement.children[0].children[1].innerHTML = (data.data.toLowerCase() == "lock" ? "Active" : "InActive")

            alert((data.data.toLowerCase() == "lock" ? 'UnLock' : 'Lock') + " Success");
        }


    })
}

