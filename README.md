# Urban dictionary.
This is an applications developed with [Python](https://www.python.org/ "Python"), [Tesseract](https://tesseract-ocr.github.io/tessdoc/Home.html "Tesseract"), [OpenCv](https://opencv.org/ "OpenCv"), [Urban Dictionary API](https://www.urbandictionary.com/ "Urban Dictionary API") (or [the API library for Python](https://pypi.org/project/urbandictionary/#description "the API library for Python")) and an OCR API.
## About the app
#### The input
It recieves an image which has urban terms inside.
#### The output
It create an .txt file which has the definitions from the word (the urban term).
### Process
- The app starts with the processing of the image with OpenCv.
- Then it follows with the text recognation using Tesseract.
- After that it takes all the words recognized and uses the API "Urban Dictionart" (or the library) to search the terms and get the definitions.
In case of use the API, the definitions are a JSON object so the app takes just the definitions array.
- Finally, the app save the definitions for each word in a text file.
