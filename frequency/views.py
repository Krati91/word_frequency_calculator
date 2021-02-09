from django.shortcuts import render
from django.http import HttpResponse
from frequency.models import Url


from bs4 import BeautifulSoup
from urllib.request import urlopen
import more_itertools
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import json

# Create your views here.

def frequency(request):
    return render(request,'frequency.html')


def result(request):
    url = request.POST["url"]
    frequency_list = {}
    db_data = ''
    if not  Url.objects.filter(url = url):   
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        for script in soup(["script","style"]):
            script.extract()
    
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        text = text.lower()
        text = text.replace('\n',' ')
        text = text.split(' ')
        text = sorted(text)
        #print(text)

        text = [word for word in text if word not in stopwords.words()]

        frequency = {}
        for word in text:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1   
    
        sorted_frequency = {}
        sorted_keys = sorted(frequency, key=frequency.get, reverse=True)         

        for w in sorted_keys:
            sorted_frequency[w] = frequency[w]       

        frequency_list = more_itertools.take(10,sorted_frequency.items())

        #saving data in database
        saverecord = Url()
        saverecord.url = url
        saverecord.frequency_list = json.dumps(frequency_list)
        saverecord.save()
    else:
        db_data = Url.objects.filter(url = url).values_list('frequency_list')
        #db_data = serializers.serialize('json',list(db_data))
        db_data = json.loads(db_data[0][0])

    return render(request,'result.html',{"frequency":frequency_list,"db_data":db_data})
