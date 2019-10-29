import pyqrcode
import png
from datetime import date



def barcodeGenerator(order_id, event_name, ref_code, order_uuid, user_order):
    today_date = date.today()

    order_details = "AFRIVENT  \
                    \n ORDER {0} CONFIRMED For {1}, \
                    \n Payment ID: {2} \
                    \n Unique Order Id: {3} \
                    \n Ordered By: {4} On {5}".format(order_id, event_name, ref_code, order_uuid, user_order, today_date )
    url = pyqrcode.create(order_details)
    image_as_str = url.png_as_base64_str(scale=5)
    image_as_str = "data:image/png;base64,{}".format(image_as_str)
    # url.png('{}.png'.format(order_id), scale=4)
    print("Printing QR code")
    # print(url.terminal(quiet_zone=1))
    return image_as_str