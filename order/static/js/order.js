// function payWithPaystack() {

//     var handler = PaystackPop.setup({ 
//         key: 'pk_test_66242613f73c8034560a3eecf9d248787f776bdb', //put your public key here
//         email: 'onasanyatunde67@@gmail.com', //put your customer's email here
//         amount: 370000, //amount the customer is supposed to pay
//         metadata: {
//             custom_fields: [
//                 {
//                     display_name: "Mobile Number",
//                     variable_name: "mobile_number",
//                     value: "+2348012345678" //customer's mobile number
//                 }
//             ]
//         },
//         callback: function (response) {
//             //after the transaction have been completed
//             //make post call  to the server with to verify payment 
//             //using transaction reference as post data
//             $.post("verify.php", {reference:response.reference}, function(status){
//                 if(status == "success")
//                     //successful transaction
//                     alert('Transaction was successful');
//                 else
//                     //transaction failed
//                     alert(response);
//             });
//         },
//         onClose: function () {
//             //when the user close the payment modal
//             alert('Transaction cancelled');
//         }
//     });
//     handler.openIframe(); //open the paystack's payment modal
// }



$("#printTicketBtn").click(function(e){
    e.preventDefault();
    printJS({ printable: 'ticket', type: 'html', header: 'AFRIVENT!' })
})