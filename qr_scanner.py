#input->qr code generated ->output->qrcode image file
import qrcode
from PIL import Image

def main():
  print("enter the data to encode in the qrcode:")
  data=input("Data:")
  data=data.strip()

  if not data:
    print("no data entered")
    return
  file_name=input("enter the file name:")
  if not file_name.strip():
    file_name="qr_code"
  
  #logic to generate qrcode
  qr_code = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=15,
    border=2,
  )
  qr_code.add_data(data)
  qr_code.make(fit=True)

  output_image=qr_code.make_image(fill_color="red",back_color="white")
  output_image.save(file_name+".png")

if __name__=="__main__":
  main()