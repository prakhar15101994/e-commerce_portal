$('.plus-cart').click(function () { 
    // console.log("plus cliked")
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type:"GET",
        url:'/pluscart/',
        data:{
            prod_id:id
        },
        success: function (data) {
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            // console.log(data)
        }
    })
  })

$('.minus-cart').click(function () { 
    // console.log("minus cliked")
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type:"GET",
        url:'/minuscart/',
        data:{
            prod_id:id
        },
        success: function (data) {
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            // console.log(data)
        }
    })
  })

$('.remove-cart').click(function () { 
    // console.log("minus cliked")
    var id=$(this).attr("pid").toString();
    var eml=this
    // console.log(id)
    $.ajax({
        type:"GET",
        url:'/removecart/',
        data:{
            prod_id:id
        },
        success: function (data) {
            
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            // console.log(data)
        }
    })
  })