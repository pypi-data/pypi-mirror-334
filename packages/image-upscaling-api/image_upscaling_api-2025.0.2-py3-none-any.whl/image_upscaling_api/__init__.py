import requests
import json


def upload_image(path, client_id, use_face_enhance = False, use_large_model = True, use_repair_mode = False):
  # URL to the PHP script
  url = "https://image-upscaling.net/upload.php"

  # Additional POST parameters (checkboxes, etc.)
  data = {}
  if(use_face_enhance):
    data["fx"] = ""
  if(use_large_model):
    data["lm"] = ""
  if(use_repair_mode):
    data["rm"] = ""

  # Cookie with a valid 32-digit hexadecimal client_id
  cookies = {
      "client_id": client_id
  }

  # Open the image file in binary mode
  files = {
      "image": open(path, "rb")
  }

  # Send the POST request
  response = requests.post(url, data=data, files=files, cookies=cookies)

  # Print the response from the server
  return response.text



def get_uploaded_images(client_id):

  # URL to the PHP script
  url = "https://image-upscaling.net/get_images_client.php"

  # Cookie with a valid 32-digit hexadecimal client_id
  cookies = {
      "client_id": client_id
  }


  # Send the POST request
  response = requests.get(url, cookies=cookies)

  # Print the response from the server
  data = json.loads(response.text)

  # Access the arrays (lists)
  waiting = data["images1"]
  completed = data["images2"]
  in_progress = data["images3"]

  return waiting, completed, in_progress
  
  

# example:
# upload_image("1.jpg", "019f39ec588eb795679598bdbee0493c", use_repair_mode=True, use_large_model = True, use_face_enhance= True)
# waiting, completed, in_progress = get_uploaded_images("019f39ec588eb795679598bdbee0493c")