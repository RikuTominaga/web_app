from flask import Flask, redirect, render_template, request, session, url_for


import sqlite3

db = sqlite3.connect(
    "./com_info.db",
    isolation_level = None,
)

sql = """
    create table if not exists COM_INFO (    
    id  INTEGER PRIMARY KEY autoincrement,
    ComName1 text, TheName1 text, ComName2 text,TheName2 text, cos_sim_fin text
    )
"""

db.execute(sql)
db.close()


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        

        from langchain.embeddings import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
        from selenium import webdriver

        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By

        num1 = request.form['num1']
        num2 = request.form['num2']

        URL1= 'https://info.gbiz.go.jp/hojin/ichiran?hojinBango='
        URL1= URL1 + num1
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 
        options.add_argument('--disable-dev-shm-usage') 
        options.add_argument("--no-sandbox") 

        driver = webdriver.Chrome(
            options=options
        )

        driver.get(URL1)

        # driver.find_element(by=By.XPATH, value="//タグ名[@属性名=属性値]")
        xpath='/html/body/div[2]/div[2]/div/div[2]/dl/dd[2]'
        ComName1=driver.find_element(By.XPATH,value=xpath).text
        xpath='//*[@id="collapse7"]/dl/dd[8]/span'
        TheName1=driver.find_element(By.XPATH,value=xpath).text

        URL2= 'https://info.gbiz.go.jp/hojin/ichiran?hojinBango='
        URL2 = URL2 + num2
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-dev-shm-usage') 
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            options=options
        )

        driver.get(URL2)

        # driver.find_element(by=By.XPATH, value="//タグ名[@属性名=属性値]")
        xpath='/html/body/div[2]/div[2]/div/div[2]/dl/dd[2]'
        ComName2=driver.find_element(By.XPATH,value=xpath).text
        xpath='//*[@id="collapse7"]/dl/dd[8]/span'
        TheName2=driver.find_element(By.XPATH,value=xpath).text

        driver.close()

        print(ComName1, TheName1)

        print(ComName2,TheName2)

        doc_result1= embeddings.embed_documents([TheName1])
        doc_result2= embeddings.embed_documents([TheName2])
        from sklearn.metrics.pairwise import cosine_similarity
        cos_sim=cosine_similarity(doc_result1, doc_result2)

        cos_sim_fin=cos_sim[0][0]
        print(cos_sim_fin,type(cos_sim_fin))

        print(num1, num2)

        session["num1"] = num1
        session["num2"] = num2
        session['name1'] = ComName1      
        session['name2'] = ComName2
        session['info1'] = TheName1
        session['info2'] = TheName2
        session['cos_sim_fin'] = float(cos_sim_fin)


        table_name = "COM_INFO"
        con = sqlite3.connect("./com_info.db")
        cur = con.cursor()
        data = (ComName1, TheName1, ComName2, TheName2, cos_sim_fin)

        sql = f"insert into {table_name} (ComName1, TheName1, ComName2, TheName2, cos_sim_fin) values (?,?,?,?,?)"
        cur.execute(sql, data)
        con.commit()
        con.close()

        con = sqlite3.connect('./com_info.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM COM_INFO")
        rows = cur.fetchall()
        print("ROWS", rows)
        for row in rows:
            print(row[5])
        con.close()

        return redirect(url_for('output'))
    return render_template('input.html')

@app.route('/output')
def output():
    return render_template('output.html')

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
        
