# Distinctive News Feed System

### Natural Language Processing and machine learning is used for this project. Django is used as Backend

Trending news topic will be provided by extracting the trending tweets from
twitter. **TWEEPY API IS USED TO GET TRENDING TWEETS FROM TWITTER AND WOE_ID IS USED TO GET PLACE INFROMATION**

Language detection of tweets will be done. **PYTHON LANGDETECT LIBRARY IS USED TO DETECT TEXT LANGUAGE** If text language is not English, then the news will be converted to English Language.**PYTHON LIBRARY GOOGLETRANS IS USED TO TRANSLATE LANGUAGE**

Emotion Analysis ( Joy, Anger, Fear, Sadness, Disgust, Shame and Guilt )**(WE HAVE TRAINED MACHINE LEARNING MODEL AND THAT MODEL IS USED)** and
Sentiment Analysis (Positive, Negative, Neutral) **(PYTHON NLTK LIBRARY USE FOR SENTIMENT ANALYSIS)** of the text will be shown

## NOTE 
Install all Libraries require for this project
```python
from django.shortcuts import render
import requests
import os
from django.conf import settings
import sys
import pickle
import re
from collections import Counter
import tweepy
import json
import nltk
import string
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np
import random
import string 
import wordninja #split tag
from textblob import TextBlob
from langdetect import detect
from translate import Translator
import re
from profanityfilter import ProfanityFilter
```

## How to run a Project
Download this zip file or clone it. Open in any IDE and add following command

```python
python manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Kuldeep](https://github.com/kuldeep1007)
