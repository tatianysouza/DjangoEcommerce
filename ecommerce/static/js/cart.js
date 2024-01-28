var updateBtns = document.getElementsByClassName("update-cart")

for(i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var sizeElement = document.querySelector('input[name="size"]:checked');
        var size = sizeElement ? sizeElement.value : this.dataset.size;  
        console.log("productId:", productId, "Action:", action, "Size:", size);
      
        console.log("USER:", user);
        if(user === "AnonymousUser"){
            addCookieItem(productId, action, size)
        }
        else{
            updateUserOrder(productId, action, size)
        }
    })
}

function addCookieItem(productId, action, size){
    console.log("Not logged in...");

    var productKey = productId + '-' + size;

    if (cart[productKey] == undefined){
        cart[productKey] = {"quantity":1, "size": size, "productId": productId}; 
    } else {
        if (action == "add"){
            cart[productKey]["quantity"] += 1;
        }

        if (action == "remove"){
            cart[productKey]["quantity"] -= 1;

            if (cart[productKey]["quantity"] <= 0){
                console.log("Item should be deleted");
                delete cart[productKey];
            }
        }
    }

    console.log("Cart:", cart);
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

function updateUserOrder(productId, action, size) {
    console.log("User is authenticated, sending data...");

    var url = "/update_item/";

    fetch(url, {
        method: "POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify({"productId":productId, "action":action, "size":size})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log("Data:", data);
        location.reload();
    });
}