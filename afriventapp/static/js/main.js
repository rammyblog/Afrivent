
$(document).ready(function(){

	$(".orderDetails").click(function() {

		let eventId= $(this).val();
		$('.modal-body').html('');

		const formatter = new Intl.NumberFormat('en-NG', {
			style: 'currency',
			currency: 'NGN'
		  });
		  

		$.ajax({
		  url: 'http://'+window.location.host+"/event-order/details/"+eventId,
		  type: "GET",
		  contentType: "application/json;charset=UTF-8",
		  success: function(result) {
			let orderArr = result['orderDetails']
			console.log(orderArr);

			let orderTotal = 0;
			
			
			$('.modal-body').append(`
				
			<p>Total Order: ${orderArr.length}</p>
			
			`);
			
			orderArr.forEach(element => {
				orderTotal += Number(element.total_cost); 
				
				$('.modal-body').append(`
				<p>Order id: ${element.id} Amount: ${formatter.format(element.total_cost)} Ordered on: ${element.created}  </p>
				
				`)
				
				console.log(orderTotal);
			});
			$('.modal-body').append(`
			<p>Total Amount made: ${formatter.format(orderTotal)} </p>
			
			`)
			
		  },
		  error: function () {
			  console.log('failed');
			  
		  }
		});
	  });
	
	$(".dropdown, .btn-group").hover(function(){
		var dropdownMenu = $(this).children(".dropdown-menu");
		if(dropdownMenu.is(":visible")){
			dropdownMenu.parent().toggleClass("open");
		}
    });

	$('.toast').toast('show');
	
	var total = 0;
	let ticketDetails = {};
	let ticketPrice = {}
	let eventID;
	let finalPrice;
	$('.quantity-calc').change(function(e) {	
		var type =  $(this).children('option:selected').data('type');
		var quantity =  $(this).children("option:selected").data('quantity');
		let price = +$(this).children("option:selected").val()
		eventID = $(this).children("option:selected").data('event');
		let data = $('.quantity-calc').map(function() {				
			return +($(this).children("option:selected").text()) * +($(this).children("option:selected").val())
		}).get();

		for (let index = 0; index < data.length; index++) {	
			total += data[index];
			$('.total_amount').html(`₦ ${total}`);
			finalPrice = total
			

		}

		data  = [];
		total = 0;
	
		if (quantity != 0) {
			ticketDetails[type] = quantity;
			ticketPrice[type] = price;
			
			console.log(ticketDetails);			
		}else{
			delete ticketDetails[type];
			delete ticketPrice[type]
		}
		$('.ticketType').html('');

		for(let[ticket, value] of Object.entries(ticketDetails)){

			let individualPrice = ticketPrice[ticket] * value;

			$('.ticketType').append(`${value}x ${ticket} - ₦${individualPrice} </br>`);

		}


 
});



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$("#orderForm").submit(function(e) {
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	e.preventDefault();
	$.ajax({
	  url: "/order/process",
	  type: "POST",
	  beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    },
	  data: {
		 ticket :JSON.stringify(ticketDetails),
		 price: JSON.stringify(ticketPrice),
		 event : eventID,
		 total: finalPrice
		},
	  success: function(response) {
		console.log(window.location.host);
		toastr.success("Saved Successfully");
		window.location.replace('http://127.0.0.1:8000/order/payment/process');

	 },
	  error: function() {
		toastr.error("An Error Occured");
	  }
	});
  });

});



// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });


