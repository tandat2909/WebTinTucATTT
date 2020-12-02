images = $('.img_blog')
images.remove()

function delblog(btn) {
    let url = '/api/delete/blog'
    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idblog": btn.value,

        })
    }).then(res => res.json()).then(data => {
        if (data.status == 200 && data.data == true) {
            btn.parentElement.parentElement.parentElement.remove()
            alert("Delete blog success")
        }
    })
}



