from flask import Flask, jsonify, request, redirect
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from flask_cors import CORS
import os   

app = Flask(__name__)
CORS(app)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

@app.route('/api/v1/filmes', methods=['GET'])
def filmes():
    URL = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/"
    req = Request(URL, headers={'User-Agent': user_agent})
    html_doc = urlopen(req).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for dataBox in soup.find_all("div", class_="card entity-card entity-card-list cf"):
        titleObj = dataBox.find("a", class_="meta-title-link")
        imgObj = dataBox.find("img",class_="thumbnail-img")
        sinopseObj = dataBox.find("div", class_="synopsis")
        dateObj = soup.find_all("span", class_="date")
        movieLinkObj = dataBox.find("a", class_="meta-title-link")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        req2 = Request(detailsLink, headers={'User-Agent': user_agent})
        htmldocMovieDetail = urlopen(req2).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="content-txt")     
        fullImgObj = soupMovieDetail.find("meta",  property="og:image")   

        data.append({'titulo': titleObj.text.strip(),
                    'poster' : fullImgObj["content"], 
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj[0].text.strip(),
                    'link' : detailsLink,
                    'sinopseFull': fullSinopse.text
                    })
                
    return jsonify({'filmes': data})  

@app.route('/api/v1/filmes/<page_id>', methods=['GET'])
def NotasEspectadores(page_id):
    URL = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/?page={}".format(page_id)
    req = Request(URL, headers={'User-Agent': user_agent})
    html_doc = urlopen(req).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for dataBox in soup.find_all("div", class_="card entity-card entity-card-list cf"):
        titleObj = dataBox.find("a", class_="meta-title-link")
        sinopseObj = dataBox.find("div", class_="synopsis")
        dateObj = soup.find_all("span", class_="date")
        movieLinkObj = dataBox.find("a", class_="meta-title-link")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        req2 = Request(detailsLink, headers={'User-Agent': user_agent})
        htmldocMovieDetail = urlopen(req2).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="content-txt")        
        fullImgObj = soupMovieDetail.find("meta",  property="og:image")   

        data.append({'titulo': titleObj.text.strip(),
                    'poster' : fullImgObj["content"], 
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj[0].text.strip(),
                    'link' : detailsLink,
                    'sinopseFull': fullSinopse.text
                    })
                
    return jsonify({'filmes': data})    

@app.route('/api/v1/filmes/emcartaz', methods=['GET'])
def EmCartaz():
    URL="http://www.adorocinema.com/filmes/numero-cinemas/"
    req = Request(URL, headers={'User-Agent': user_agent})
    html_doc = urlopen(req).read()
    soup = BeautifulSoup(html_doc, "html.parser")

    data = []
    for dataBox in soup.find_all("div", class_="card card-entity card-entity-list cf"):
        nomeObj = dataBox.find("h2", class_="meta-title")
        imgObj = dataBox.find(class_="thumbnail ")
        sinopseObj = dataBox.find("div", class_="synopsis")
        dataObj = dataBox.find(class_="meta-body").find(class_="meta-body-item meta-body-info")
        movieLinkObj = dataBox.find(class_="meta-title-link")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="content-txt")        

        data.append({   'nome': nomeObj.text.strip(),
                        'poster' : imgObj.img['data-src'].strip(),
                        'sinopse' : sinopseObj.text.strip(),
                        'data' :  dataObj.text[1:23].strip().replace('/',' '),
                        'link' : detailsLink,
                        'sinopseFull': fullSinopse.text})
                
    return jsonify({'filmes': data})
    
@app.route('/api/v1/filmes/<page_id>')
def filmes_api_page(page_id):
    
    if int(page_id) > 6:
        return redirect("http://python--bergpb.c9users.io/api/v1/filmes", code=200)
        
    else:
        url = "http://www.adorocinema.com/filmes/numero-cinemas/?page={}".format(page_id)
        req = Request(URL, headers={'User-Agent': user_agent})
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc, "html.parser")
    
        data = []
        for dataBox in soup.find_all("div", class_="card card-entity card-entity-list cf"):
            nomeObj = dataBox.find("h2", class_="meta-title")
            imgObj = dataBox.find(class_="thumbnail ")
            sinopseObj = dataBox.find("div", class_="synopsis")
            dataObj = dataBox.find(class_="meta-body").find(class_="meta-body-item meta-body-info")
    
            data.append({   'nome': nomeObj.text.strip(),
                            'poster' : imgObj.img['data-src'].strip(),
                            'sinopse' : sinopseObj.text.strip(),
                            'data' :  dataObj.text[1:23].strip().replace('/',' ')})
                    
        return jsonify({'filmes': data})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
