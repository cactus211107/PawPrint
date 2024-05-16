import db

db.initDB('database.db')
BASE_URL='https://pawprint.aisct.org' # I dont have the url. so this is just what it could look like


def generateSitemap(path='sitemap.xml'):
    with open(path,'w') as f:
        papers = db.execute('SELECT * FROM PAPERS').fetchall()
        xml=f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE_URL}/add</loc></url><url><loc>{BASE_URL}/about</loc></url>{"".join([f"<url><loc>{BASE_URL}/pawprint/{paper[1]}</loc><lastmod>{paper[2]}</lastmod></url>" for paper in papers])}</urlset>"""
        f.write(xml)
generateSitemap()