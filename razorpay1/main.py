
import razorpay
client = razorpay.Client(auth=("rzp_test_ju3EIJ0EQ97kW8", "hYPTFb12GGfHCD7oNO3Ngwuy"))

data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
payment = client.order.create(data=data)
