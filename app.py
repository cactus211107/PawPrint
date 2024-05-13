from flask import *
from bs4 import BeautifulSoup as Soup
import requests,re,os,db,bs4.element,datetime

app = Flask(__name__)
os.environ['PASSWORD']='AISCT_PAW_PRINT_ADMIN'
app.secret_key='just a random key i ate for breakfast today' # look... I had to think of something

db.initDB('database.db')
db.executeFile('.sql')


def downloadSlideshow(id,path):
    slides=[]
    page=requests.get(f'https://docs.google.com/presentation/d/{id}/edit').text
    with open('html.html','w') as f:f.write(page)
    page=Soup(page,features='html.parser')
    scripts:list[bs4.element.Tag]=page.find_all('script',{"type":"text/javascript"})[3:-1:2]
    for script in scripts:
        try:
            text=script.text
            pos=re.search(r'"([A-z]|_|[0-9]|-)*:notes"',text).span()
            slides.append(text[pos[0]+1:pos[1]-7])
        except:0
    os.makedirs(path)
    for i,slide in enumerate(slides):
        r=requests.get(f'https://docs.google.com/presentation/d/{id}/export/svg?id={id}&pageid={slide}')
        name=os.path.join(path,f'slide_{i}.svg')
        with open(name,'w') as f:
            f.write(r.text)
    return slides
def getSlideshowIDFromURL(url):return url.split('/')[-2]
def addPost(title,slide_url):
    url_safe_title=re.sub("[^a-z0-9-]", "", title.lower().replace(" ", "-"))
    gid=getSlideshowIDFromURL(slide_url)
    date = datetime.datetime.now()
    s=downloadSlideshow(gid,f'slides/{url_safe_title}')
    if len(s)==0:return None
    db.execute('INSERT INTO PAPERS VALUES (?,?,?,?)',(title,url_safe_title,date,slide_url))
    return url_safe_title
def getMostRecentPost(p='URL_SAFE_TITLE',n=1):
    return db.execute(f'SELECT {p} FROM PAPERS ORDER BY PUBLISH_DATE DESC LIMIT {n}').fetchall()
def getPostByUST(ust): #UST==UrlSafeTitle
    return db.execute(f'SELECT * FROM PAPERS WHERE URL_SAFE_TITLE="{ust}"').fetchone()
def dateToTextDate(date):
    date = date.split('-')
    year = date[0]
    m=["January","February","March","April","May","June","July","August","September","October","November","December"]
    month = m[int(date[1])-1]
    day = date[2].split(' ')[0]
    return f'{month} {day}, {year}'



@app.route('/')
def index():
    try:recent=getMostRecentPost('*');title,id=recent[0][:2]
    except Exception as e:print(e);title,id='',''
    try:articles=getMostRecentPost('*',4)[1:] # gets the 3 articles after the first one
    except Exception as e:print(e);articles=[]
    return render_template('index.html',title=title,id=id,articles=articles,date=dateToTextDate)

@app.route('/pw',methods=['GET','POST'])
def pw():
    if session.get('entered_password')=='yes i have':return redirect('/add')
    if request.method=='POST':
        if request.form.get('pw')==os.environ['PASSWORD']:
            session['entered_password']='yes i have'
            return redirect('/add')
    return render_template('pw.html')
@app.route('/add',methods=['GET','POST'])
def add():
    if session.get('entered_password')!='yes i have':return redirect('/pw')
    if request.method=='POST':
        url=request.form.get('url')
        title=request.form.get('title')
        url_safe_title=addPost(title,url)
        if url_safe_title:return redirect(f'/pawprint/{url_safe_title}')
    return render_template('add.html')
@app.route('/pawprint/<title>')
def paw_print_page(title):
    paper = getPostByUST(title)
    if not paper:return redirect('/')
    path=f'slides/{title}'
    slides = os.listdir(path)[::-1]
    return render_template('pawprint.html',title=paper[0],publish_date=dateToTextDate(paper[2]),slides=slides,slides_url=paper[3],id=title)
@app.route('/slides/<id>/<slide>')
def slide(id,slide):
    with open(os.path.join('slides',id,slide),'r') as f:
        r=Response(f.read(), mimetype='image/svg+xml');r.headers['Cache-Control']='max-age=31536000'
        return r
@app.route('/recent')
def recent_page_redirect():
    try:return redirect('/pawprint/'+getMostRecentPost()[0][0])
    except:return redirect('/')


def run(online=True):app.run(host='0.0.0.0'if online else None,port=8881)
run()