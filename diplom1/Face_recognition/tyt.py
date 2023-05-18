from PIL import Image
import face_recognition

import matplotlib.pyplot as plt
known_image = face_recognition.load_image_file("images/34.jpg")
unknown_image = face_recognition.load_image_file("images/31.jpg")
print(known_image)
img1 = Image.open("images/34.jpg")
plt.imshow(img1)
plt.axis('off')
plt.show()
img2 = Image.open("images/31.jpg")
plt.imshow(img2)
plt.axis('off')
plt.show()
baixiaona_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
results = face_recognition.compare_faces([baixiaona_encoding], unknown_encoding)
if results[0] == True:
    print ("Yes!")
else:
    print ("No!")

