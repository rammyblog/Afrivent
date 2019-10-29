
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
				<p>Order id: ${element.id} Amount: ${formatter.format(element.total_cost)} 
				Ordered on: ${element.created}  </p>
				
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
	let ticketPrice = {};
	let ticketName = {}
	let eventID;
	let finalPrice;
	$('.quantity-calc').change(function(e) {	
		var type =  $(this).children('option:selected').data('type');
		var ticket_name =  $(this).children('option:selected').data('ticket_name');
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
			ticketName[type] = ticket_name 
			// console.log(ticketDetails);			
		}else{
			delete ticketDetails[type];
			delete ticketPrice[type]
			delete ticketName[type]

		}
		$('.ticketType').html('');

		for(let[ticket, value] of Object.entries(ticketDetails)){
			console.log(ticket, ticketDetails)
			let individualPrice = ticketPrice[ticket] * value;
			$('.ticketType').append(`${value}x ${ticketName[ticket]} - ₦${individualPrice} </br>`);

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



$('#addticket').on('click', function(e) {
	let ticketData = {}
	e.preventDefault();
	$('#event-ticket-form').append(`
    <div class="form-row">
        <div class="form-group col-md-6">
          <label for="ticketType">Ticket Type</label>
          <input type="text" class="form-control ticketType" name="type" placeholder="Regular..." required>
        </div>
        <div class="form-group col-md-3">
            <label for="quantity">Quantity Available</label>
            <input type="number" class="form-control quantityInput" name="quantity" required placeholder="50" id="quantity" required>
          </div>
        <div class="form-group col-md-2">
          <label for="amount">Amount</label>
          <input type="number" class="form-control amountInput" name="amount" required placeholder="50.00" id="amount" required>
        </div>
        <button type="button"  class=" close closeTicket"  aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
      </div>

	`);
	closeTicket()

	let ticketTypeInput = $('.ticketType')
	let quantityAvailableInput =  $('.quantityInput')
	let ticketAmount = $('.amountInput')
	for (let index = 0; index < ticketTypeInput.length; index++) {	
		// console.log(ticketAmount[index].value.length);
		
		if(  (ticketTypeInput[index].value.trim().length >= 1) && (ticketAmount[index].value.length >= 1) && (quantityAvailableInput[index].value.length >= 1)
		){
			let ticketType = ticketTypeInput[index].value;
			let ticketUnitAmount = ticketAmount[index].value;
			let ticketUnitQuantity = quantityAvailableInput[index].value;

			ticketData[index]= {
				'ticketType': ticketType,
				'ticketAmount': ticketUnitAmount,
				'ticketQuantity': ticketUnitQuantity
			}




		}	
		
		console.log(ticketData);
		

		

		
	}

	

		

		// for (let index = 0; index < ticketAmount.length; index++) {		
		// 	console.log(ticketAmount[index].value)
		// }

		
	

	// $('.ticketType').forEach( element => {
	// 	console.log(element);
		
	// });
	
	
	

	
})

function closeTicket(){
	$('.closeTicket').on('click', function() {
		$(this).parent().remove();
	})
}

closeTicket()

$("#createEvent").submit(function(e) {
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	e.preventDefault();
	$form = $(this)
	var formData = new FormData(this);
	$.ajax({
		url: "/new/event/created",
		type: "POST",
		data: formData,
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		success: function(response){
			console.log(window.location.host);
			toastr.success("Event Created Successfully");
			window.location.replace('http://'+window.location.host+response);
	
			
		},
		error: function(){
			toastr.error("An Error Occured");
			console.log("Error Occured");
			
		},
		cache: false,
		contentType: false,
		processData: false
		
	})
	
})


$("#orderForm").submit(function(e) {
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	e.preventDefault()
	
	// $('#ticket-modal').modal('hide');

	$('.modal-grid').html('');


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
		console.log(response);
		toastr.success("Saved Successfully");
		// $.redirect("http://127.0.0.1:8000/order/process/confirm", {"X-CSRFToken": csrf_token}, "POST" ); 
		window.location.replace('http://127.0.0.1:8000/order/process/confirm');

		// $("#orderFrom").submit();

	 },
	  error: function() {
		  console.log(data);
		  
		toastr.error("An Error Occured");
	  },
	//   cache: false,
	//   contentType: false,
	//   processData: false,
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




function startTimer(duration, display) {
	var start = Date.now(),
		diff,
        minutes,
        seconds;
    function timer() {
        // get the number of seconds that have elapsed since 
 

       // startTimer() was called
        diff = duration - (((Date.now() - start) / 1000) | 0);

        // does the same job as parseInt truncates the float
        minutes = (diff / 60) | 0;
        seconds = (diff % 60) | 0;

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds; 

        if (diff <= 0) {
            // add one second so that the count down starts at the full duration
            // example 05:00 not 04:59
            start = Date.now() + 1000;
        }
    };
    // we don't want to wait a full second before the timer starts
    timer();
    setInterval(timer, 1000);
}

window.onload = function () {
    var tenMinutes = 60 * 10,
        display = document.querySelector('#time');
    startTimer(tenMinutes, display);
};


