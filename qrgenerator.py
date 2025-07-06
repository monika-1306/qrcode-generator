import qrcode
import os
import platform
def main():
    #get qr from user
    data = input("Enter the text or URL to generate QR Code: ")
    #ask user for filename
    filename=input("Enter the filename to save the QR Code: ")
    fill_color=input("entr the color for the qr code: ")
    back_color=input("enter the background color for the qr code: ")
    #generate qr code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(filename)
    #save qr code
    print(f"QR Code generated and saved as '{filename}'")
    open_image(filename)
def open_image(filename):
    try:
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":
            os.system(f"open {filename}")
        else:
            os.system(f"xdg-open {filename}")
        print(f" Opened '{filename}' in default image viewer.")
    except Exception as e:
        print(f" Could not open the image. Error: {e}")
    
 


if __name__ == "__main__":
    main()
