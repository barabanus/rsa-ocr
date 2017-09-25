# Read RSA SecurID token from image — proof of concept
The goal of this project is to show that [RSA SecurID token](https://en.wikipedia.org/wiki/RSA_SecurID) codes can be read automatically.

This key fob had been put into a shoe box with webcam. The program runs web server to read digits from this particular setup:

![RSA SecurID token](https://raw.githubusercontent.com/barabanus/rsa-ocr/master/samples/011937.jpg "RSA SecurID token")

# Installation instructions
In order to run the program you need:
- Python 2.7
- [NumPy](http://www.numpy.org/) library
- [OpenCV](http://opencv.org/) library with Python 2 bindings
- [The Pyramid Web Framework](https://docs.pylonsproject.org/projects/pyramid/en/latest) v1.9.1

For MacOS you may install [Homebrew](https://brew.sh/) and run the following commands:
```
brew install numpy
brew install opencv3
sudo pip install "pyramid==1.9.1"
```

# Running the program
You can start the web server from the root of the project:
```
python main.py
```
Now you can open your browser and visit home page of the project at http://localhost:8080

You may feed images from [samples](https://github.com/barabanus/rsa-ocr/tree/master/samples) directory to read digits from images. The program is tuned to recognize only this particular setup, so it probably won't work for images taken from other RSA token setups.

In order to read other images you need to change global constants within [ocr.py](https://github.com/barabanus/rsa-ocr/blob/master/ocr.py) and update [digits.png](https://github.com/barabanus/rsa-ocr/blob/master/digits.png) for your scale.
