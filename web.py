from flask import Flask, jsonify, request, redirect
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from flask_cors import CORS
#from urllib2 import urlopen
import os   

app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={
#     r"/*":{
#         "origins:" "*"
#     }
# })

@app.route('/api/v1/filmes', methods=['GET'])
def filmes():
    URL = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/"
    
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for dataBox in soup.find_all("div", class_="data_box"):
        titleObj = dataBox.find("a", class_="no_underline")
        imgObj = dataBox.find(class_="img_side_content").find_all(class_="acLnk")[0]
        sinopseObj = dataBox.find("div", class_="content").find_all("p")[0]
        dateObj = dataBox.find("div", class_="content").find("div", class_="oflow_a")
        movieLinkObj = dataBox.find(class_="img_side_content").find_all("a")[0]
        generoObj = dataBox.find("div", class_="content").find_all('li')[3].find('div',class_="oflow_a")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="content-txt")     
        fullImgObj = soupMovieDetail.find("meta",  property="og:image")   

        data.append({'titulo': titleObj.text.strip(),
                    'genero': generoObj.text.replace('\n','').strip(),
                    'poster' : fullImgObj["content"], 
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj.text[0:11].strip(),
                    'link' : detailsLink,
                    'sinopseFull': fullSinopse.text})
                
    return jsonify({'filmes': data})  

@app.route('/api/v1/filmes/<page_id>', methods=['GET'])
def NotasEspectadores(page_id):
    URL = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/?page={}".format(page_id)
    
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for dataBox in soup.find_all("div", class_="data_box"):
        titleObj = dataBox.find("a", class_="no_underline")
        # imgObj = dataBox.find(class_="img_side_content").find_all(class_="acLnk")[0]
        sinopseObj = dataBox.find("div", class_="content").find_all("p")[0]
        dateObj = dataBox.find("div", class_="content").find("div", class_="oflow_a")
        movieLinkObj = dataBox.find(class_="img_side_content").find_all("a")[0]
        generoObj = dataBox.find("div", class_="content").find_all('li')[3].find('div',class_="oflow_a")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="content-txt")        
        fullImgObj = soupMovieDetail.find("meta",  property="og:image")   

        data.append({'titulo': titleObj.text.strip(),
                    'genero': generoObj.text.replace('\n','').strip(),
                    'poster' : fullImgObj["content"], 
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj.text[0:11].strip(),
                    'link' : detailsLink,
                    'sinopseFull': fullSinopse.text})
                
    return jsonify({'filmes': data})    

@app.route('/api/v1/filmes/emcartaz', methods=['GET'])
def EmCartaz():
    html_doc = urlopen("http://www.adorocinema.com/filmes/numero-cinemas/").read()
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
        
        html_doc = urlopen(url).read()
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
