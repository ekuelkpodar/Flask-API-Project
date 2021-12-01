from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "torAPI"

DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "admin"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM recipes"
    cur.execute(s) # Execute the SQLpip
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)

@app.route('/add_recipes', methods=['POST'])
def add_recipes():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        category = request.form['category']
        country = request.form['country']
        cur.execute("INSERT INTO recipes (fname, category, country) VALUES (%s,%s,%s)", (fname, category, country))
        conn.commit()
        flash('recipes Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM recipes WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', recipes = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_recipes(id):
    if request.method == 'POST':
        fname = request.form['fname']
        category = request.form['category']
        country = request.form['country']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE recipes
            SET fname = %s,
                category = %s,
                country = %s
            WHERE id = %s
        """, (fname, category, country, id))
        flash('recipes Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_recipes(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM recipes WHERE id = {0}'.format(id))
    conn.commit()
    flash('recipes Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)
