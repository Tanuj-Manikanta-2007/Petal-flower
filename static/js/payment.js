// Razorpay Payment Handler
document.addEventListener('DOMContentLoaded', function() {
    var data = window.paymentData;
    
    var options = {
        "key": data.razorpay_key,
        "amount": data.amount,
        "currency": "INR",
        "name": "PetalCart 🌸",
        "description": "Thank you for your flower order!",
        "order_id": data.order_id,
        "theme": {
            "color": "#d88195"
        },
        "prefill": {
            "name": data.user_name,
            "email": data.user_email,
            "contact": document.getElementById('phone').value || ""
        },
        "handler": handlePaymentSuccess,
        "modal": {
            "ondismiss": function() {
                console.log('Payment window closed');
            }
        }
    };

    var rzp = new Razorpay(options);
    
    document.getElementById('pay-btn').onclick = function(e){
        e.preventDefault();
        rzp.open();
    }
});

function handlePaymentSuccess(response) {
    const data = window.paymentData;
    const payBtn = document.getElementById('pay-btn');
    
    // Show loading state
    payBtn.disabled = true;
    payBtn.innerHTML = '<span class="spinner"></span> Processing...';

    // Send payment details to server
    fetch("/payment-success/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": data.csrf_token
        },
        body: JSON.stringify({
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_order_id: response.razorpay_order_id,
            razorpay_signature: response.razorpay_signature
        })
    }).then(res => {
        return res.json().then(responseData => ({
            ok: res.ok,
            status: res.status,
            data: responseData
        }));
    }).then(response => {
        if (response.ok) {
            // Payment successful - redirect to order history
            window.location.href = "/order_history/";
        } else {
            // Payment verification failed
            console.error('Payment verification failed:', response.data);
            resetPaymentButton();
            const errorMsg = response.data.message || 'Payment verification failed. Please try again.';
            alert('Error: ' + errorMsg);
        }
    }).catch(error => {
        // Network or other error
        console.error('Error:', error);
        resetPaymentButton();
        alert('An error occurred: ' + error.message);
    });
}

function resetPaymentButton() {
    const payBtn = document.getElementById('pay-btn');
    const amount = window.paymentData.pay_amount;
    payBtn.disabled = false;
    payBtn.innerHTML = '<span class="btn-icon">🚀</span> Pay Securely with Razorpay <span class="btn-amount">₹' + amount + '</span>';
}
