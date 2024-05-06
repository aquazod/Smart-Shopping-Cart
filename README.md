Aim
--------------
This project aims to create a smart shopping cart, inspired by Amazon Smart Shopping Cart. The Smart Shopping Cart provides a full digital shopping process for the customers, starting from the moment they enter the market till they leave the market.

Abstract
-----------
When the customer enters, they need to have the Smart cart mobile application on their phones. They pick a smart shopping cart from the market and scan the QR code on the card so they are connected to this specific cart.
During the shopping process, any product the customer puts inside the cart will be detected and the item will appear in the cart content inside the mobile application with the item specifications. In case the customer removed any product, it would be removed from the cart content.
At the end of the shopping process, the customer could pay for the bill from the payment methods provided in the mobile application and then they would get disconnected from the cart and leave the store.


Used Technologies
  -----------------
  - Artificial Intelligence
    -------------
    - Computer Vision: Used to create a deep learning model using YOLOv8 algorithm, the model is used to detect any product leaving or entering the cart in a live stream. The Model was trained on Google Colab.
    - TensorFlow: Used to deploy the YOLO model into the Python program which has the live stream.
    - Python: Loads the trained YOLO model and opens the live camera stream running on it from the cameras connected to the cart.
  - Web Server
    --------------
    - ASP.NET, C#
    - Swagger
    - Microsoft Azure
  - Database
    ---------
    - Microsoft SQL Server
  - Mobile Application
    ------------------------
    - Flutter: Creates the mobile application, built on Dart Programming language.
  - Embedded System
    ----------
    - Arduino
- Implementation
  --------------------
First, we collected the dataset and uploaded it to Roboflow.com to deal with the dataset and apply the pre-training required processes, such as: Annotation, Augmentation, and Splitting the dataset into three sets, Training, Validation, and Testing sets.

Then the dataset was imported to Google Colab to train the model using YOLOv8 algorithm, [here](https://colab.research.google.com/drive/1Yfh5XloQpOrFUVu3oZuvqSApRYeSgfm4#scrollTo=8O5kU26s2gIG) is the link for the codes and the training results.

Then the model was imported to the Python program to be used for the object detection process.


The connected cart to a customer had camera sensors that were running a live stream, the python program on the system was using the trained AI model on that live stream. Once a product was detected, an API POST request was sent to the web server with the product ID, the API then sends a GET request to the database with the ID and receive another request with the item details, and then sends a POST request to the mobile application to show the item in the cart content. The reverse steps would happen if the product was detected leaving the cart.

How did we detect if the product is entering or leaving the cart?

By creating a virtual line in the middle of the live stream. If the product's bounding box coordinations on the frame were getting reduced vertically, then the producted was entering the cart. However, if the vertical coordinations were increasing, then the product is leaving the cart.

Fraud Detection System
---------------
There were some cases where the customer tried to put their hands on the camera and at the same time put a product inside the cart, so they were deciding to dodge the product detection, which would give them a free item since the item was not detected and then it was not included in the final bill.

What was done to handle this?

All the weights of the products in the market were saved in the database, and a weight scale was integrated to the cart which was continuously measuring the weight of the cart content. Whenever a weight difference is detected, the system checks if this weight difference is concurrent with a product detection in the live stream or not, in case there was no product detection, then it was a fraud attempt. Immediately a POST request was sent to the API to set the "fraud flag" in the database as true, which resulted in locking the application with a message that "There is an undetected product, please remove it from the cart". When the customer removed the product from the cart the "fraud flag" was set the false and the application continued working.

The project was finished at June 2023.
