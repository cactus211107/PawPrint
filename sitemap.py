import db

db.initDB('database.db')
def generateSitemap(baseURL='https://pawprint.aisct.org',path='sitemap.xml'):
    with open(path,'w') as f:
        papers = db.execute('SELECT * FROM PAPERS').fetchall()
        xml=f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{baseURL}/add</loc></url><url><loc>{baseURL}/about</loc></url>{"".join([f"<url><loc>{baseURL}/pawprint/{paper[1]}</loc><lastmod>{paper[2]}</lastmod></url>" for paper in papers])}</urlset>"""
        f.write(xml)
generateSitemap()