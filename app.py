from flask import Flask,render_template,request,jsonify,redirect,url_for,session,flash
from flask_mysqldb import MySQL
import plotly.graph_objects as go




app=Flask(__name__)
app.secret_key = '71720a3f5af80150bd022b28bd25a1ba'

app.config['MYSQL_HOST'] = 'sql8.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql8791991'
app.config['MYSQL_PASSWORD'] = 'rmdz6bALfd'
app.config['MYSQL_DB'] = 'sql8791991'
app.config['MYSQL_CURSORCLASS']="DictCursor"
mysql=MySQL(app)

@app.route("/")

def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/logout")
def logout():
    session.clear()
    
    return render_template('home.html')

@app.route('/get_subcategories', methods=['GET'])
def get_subcategories():
    category = request.args.get('category')  # Retrieve category from query parameters

    print(f"Received category: {category}")
    
    if not category:
        return "Category is required", 400

    try:
        
        # cursor = mysql.connection.cursor()
        # cursor.execute("select * from transactions where user_id=%s",[session["id"]])
        # trans = cursor.fetchall()
        # cursor.close()
  
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("select subcat FROM category where cate = %s", [category,])
        #subcategories = [row[0] for row in cursor.fetchall()]
        subcategories = [row['subcat'] for row in cursor.fetchall()]
        #subcategories = cursor.fetchall()
        print(f"Fetched subcategories: {subcategories}")
        
        cursor.close()

        if not subcategories:
            return '<option value="">No subcategories found</option>'

        # Return HTML options as a response
        options = ''.join([f'<option value="{subcat}">{subcat}</option>' for subcat in subcategories])
        #return ''.join([f'<option value="{subcat}">{subcat}</option>' for subcat in subcategories])
        
        
        print(options)
        return options
    except Exception as e:
        print(e)
        return f"<option value=''>Error: {str(e)}</option>"
       # return f"<option value=''>Error: {str(e)}</option>"

@app.route("/register",methods=["POST","GET"])
def register():
    
    if 'submit' in request.form:
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        email=request.form.get("email")
        uname=request.form.get("uname")
        pswd=request.form.get("pswd")
        
              
        cur=mysql.connection.cursor()
        cur.execute("insert into users (fname,lname,email,uname,pswd) values (%s,%s,%s,%s,%s)",[fname,lname,email,uname,pswd])
        mysql.connection.commit()
        print("Registered")
        return render_template('home.html')
        
        
    return render_template('signup.html')

@app.route("/income",methods=["POST","GET"])
def income():
    
    if 'submit' in request.form:
        uid=session["id"]
        amount=request.form.get("txtincome","0")
        
        emi=request.form.get("emiAmount","0")
        amount1=float(amount)-float(emi)
       
              
        cur=mysql.connection.cursor()
        cur.execute("insert into incomedet (user_id,amount,emi) values (%s,%s,%s)",[uid,amount1,emi])
        mysql.connection.commit()
        flash('Income Updated successfully!', 'success')
        return render_template('usertransaction.html')
        
        
    return render_template('Addincome.html')

@app.route("/login",methods=["POST","GET"])

def login():
    
    if 'ulog' in request.form:
        uname=request.form.get("uname")
        pswd=request.form.get("pswd")
        print(uname)
        print(pswd)
       
        try:
            
            cur=mysql.connection.cursor()
            cur.execute("select * from users where uname=%s and pswd=%s",[uname,pswd] )
            res=cur.fetchone()
            
            if res:
                session["uname"]=res['uname']
                session["id"]=res['id']
                return redirect(url_for('usertransaction'))
            else:
                return render_template('home.html')
        except Exception as e:
            print(e)
        finally:
             mysql.connection.commit()
             cur.close()
      
    
    return render_template('login.html')

@app.route("/usertransaction", methods=["POST","GET"])

def usertransaction():
    
    if 'uname' not in session:
        flash('Please log in first.', 'error')
        return redirect('/login')
    
    
    
    if request.method == 'POST':
        user_id = session["id"]
        amount = request.form['amt']
        description = request.form['descr']
       # cate = request.form['category']
        cate = request.form['option']
        scate = request.form['subcategory']
       
        print(cate)
        
        # if cate:
        #     # Query the database to get the category name based on the category_id
        #     cursor = mysql.connection.cursor()
        #     cursor.execute("SELECT cate,subcat,priority FROM category WHERE id = %s", (cate,))
        #     category_name = cursor.fetchone()  # Fetch the category name
        #     category_name = category_name['cate']
            
        #     cursor.close()

        # Save transaction (example)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO transactions (user_id, amount, description,category,subcat) VALUES (%s, %s, %s, %s,%s)", 
                       (user_id , amount, description,cate,scate))
        mysql.connection.commit()
        cursor.close()

        flash('Transaction saved successfully!', 'success')
        
    
    return render_template('usertransaction.html')

    
@app.route("/viewtransactions",methods=["POST","GET"])

def viewtransactions():
    
    cursor = mysql.connection.cursor()
    cursor.execute("select * from transactions where user_id=%s  ORDER BY date DESC LIMIT 5",[session["id"]])
    trans = cursor.fetchall()
    cursor.close()
    return render_template('viewtransactions.html',trans=trans) 


@app.route("/edittransaction/<int:id>",methods=["POST","GET"])

def edittransaction(id):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from transactions where id=%s",(id,))
    trans_id = cursor.fetchone()
    cursor.close()
    
    if not trans_id:
        return "Transaction not found!"
    
    cursor1 = mysql.connection.cursor()
    cursor1.execute("select * from category where cate=%s",(trans_id['category'],))
    cat = cursor1.fetchone()
    cursor1.close()
    
    if request.method == 'POST':
        dt = request.form['dt']
        amount = request.form['amt']
        description = request.form['descr']
        
        cursor = mysql.connection.cursor()
       # cursor.execute("UPDATE transactions set (dt=%s, amount=%s, description=%s ,values (dt , amount, description,id))")
        
        cursor.execute("UPDATE transactions SET date=%s, amount=%s, description=%s WHERE id=%s",
        (dt, amount, description, id))
        mysql.connection.commit()
        cursor.close()

        flash('Transaction Updated successfully!', 'success')
  
    
    #flash(trans_id)
    return render_template('edittransaction.html',trans_id=trans_id,cat=cat)



@app.route("/deletetransaction/<int:id>",methods=["POST","GET"])

def deletetransaction(id):
    cursor = mysql.connection.cursor()
       # cursor.execute("UPDATE transactions set (dt=%s, amount=%s, description=%s ,values (dt , amount, description,id))")
        
    cursor.execute("delete from transactions WHERE id=%s",(id,))
    mysql.connection.commit()
    cursor.close()

    flash('Transaction Deleted successfully!', 'success')
    return redirect(url_for("viewtransactions"))

# @app.route("/transactionhistory/<int:id>",methods=["POST","GET"])

# def transactionhistory(id):
#    return render_template('transactionhistory.html')

#@app.route("/transactionhistory",methods=["POST","GET"])

@app.route("/transactionhistory", methods=["POST", "GET"])
def transactionhistory():
    
    totalIncome = 0  # Initialize totalIncome with a default value of 0
    totalExpenses = 0 
    emi=0
    
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        cursor = mysql.connection.cursor()
        if month != "00":  # If specific month is selected
            query = """
            SELECT SUM(amount) 
            FROM incomedet 
            WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s
            """
            cursor.execute(query, [session['id'], month, year])
        else:  # If no specific month is selected, get total income for the whole year
            query = """
            SELECT SUM(amount) 
            FROM incomedet 
            WHERE user_id = %s AND YEAR(date) = %s
            """
            cursor.execute(query, [session['id'], year])

        data = cursor.fetchone()

        # If no income data found, set totalIncome to 0
        totalIncome = data['SUM(amount)'] if data and data['SUM(amount)'] is not None else 0
        cursor.close()
       

        # Print the result or use it as needed
        print("Income:", totalIncome)
        
       
         # Create cursor for emi
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT SUM(emi) FROM incomedet WHERE user_id = %s", [session['id']])
        data = cursor.fetchone()

        emi = data['SUM(emi)'] if data and data['SUM(emi)'] is not None else 0
        

        # Create cursor for expenses
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s", [session['id']])
        data = cur.fetchone()
        totalExpenses = data['SUM(amount)'] if data and data['SUM(amount)'] else 0

        if month == "00":
            cur.execute(f"SELECT SUM(amount) FROM transactions WHERE YEAR(date) = YEAR('{year}-00-00') AND user_id = {session['id']}")
            data = cur.fetchone()
            totalExpenses = data['SUM(amount)'] if data and data['SUM(amount)'] is not None else 0
            result = cur.execute(f"SELECT * FROM transactions WHERE YEAR(date) = YEAR('{year}-00-00') AND user_id = {session['id']} ORDER BY date DESC")
        else:
            cur.execute(f"SELECT SUM(amount) FROM transactions WHERE MONTH(date) = MONTH('0000-{month}-00') AND YEAR(date) = YEAR('{year}-00-00') AND user_id = {session['id']}")
            data = cur.fetchone()
            totalExpenses = data['SUM(amount)'] if data and data['SUM(amount)'] is not None else 0
            result = cur.execute(f"SELECT * FROM transactions WHERE MONTH(date) = MONTH('0000-{month}-00') AND YEAR(date) = YEAR('{year}-00-00') AND user_id = {session['id']} ORDER BY date DESC")

        if result > 0:
            transactions = cur.fetchall()
            
            print(transactions)
            pval_poor = 0  # Total for 'Poor' priority
            pval_low = 0   # Total for 'Low' priority
            pval_medium = 0  # Total for 'Medium' priority
            msg1, msg2, msg3 = "", "", ""
                     
            for trans in transactions:
                cat = trans['category']
                scat = trans['subcat']
                amt = trans['amount']
    
            # Fetch priority from the database
                cur = mysql.connection.cursor()
                cur.execute("SELECT priority FROM category WHERE cate = %s and subcat = %s", (cat, scat))
                data = cur.fetchone()
                p = data['priority']
           
                print(p)
        
                # Perform calculations based on priority
                if (cat == "Others" and p == "Poor"):
                    adjustment = amt * 10 / 100
                    pval_poor += adjustment
                    msg1 = "You Spent " + str(pval_poor) +" "+ "for "+ scat
                    
                elif cat == "Others" and p == "Low":
                    adjustment = amt * 25 / 100
                    pval_low += adjustment
                    msg2 = "You Spent " + str(pval_low) + " "+"for "+ scat
                    
                elif cat == "Others" and p == "Medium":
                    adjustment = amt * 50 / 100
                    pval_medium += adjustment
                    msg3 = "You Spent " + str(pval_medium)+" "+ "for "+ scat
                    print("hi")
                elif cat == "Others" and p == "High":
                    a=0
                    a=a+1
            # Print summary of adjustments
           
            import random
           
                     
            if msg1:
                flash(msg1, 'success')
                poor_expense_suggestions = [
    
                "This expense may not align with your financial goals. Consider reevaluating.",
                "The current spending choice might not be optimal for your budgetary plan.",
                "This decision appears to stretch your finances. A more prudent choice might be advisable.",
                "It seems this expense could be reconsidered to ensure better financial health.",
                "This spending doesnt seem cost-effective. Lets assess more efficient alternatives."]
                flash(random.choice(poor_expense_suggestions))
                #flash("Suggestion:",sug1)
            if msg2:
                flash(msg2, 'warning')
                low_expense_suggestions = [
                    "This expense may not align with your financial objectives. A review is recommended.",
                    "This spending decision appears suboptimal and could impact your budget negatively.",
                    "The expense does not reflect prudent financial planning. Consider revising this choice.",
                    "This allocation of funds may hinder progress toward your goals. Reassessment is advised.",
                    "This spending seems inefficient. Exploring more effective options might be beneficial."
                ]
                flash(random.choice(low_expense_suggestions))
                #flash("Suggestion:",sug2)
            if msg3:
                flash(msg3, 'danger')
                medium_expense_suggestions = [
                     "This expense seems reasonable, but a review may yield better alternatives.",
                     "A moderately good choice, though some adjustments might optimize your budget.",
                     "This decision appears fair; however, reevaluating may enhance your savings.",
                     "A decent spending decision, but careful assessment could improve outcomes.",
                     "This is an acceptable expense, yet there could be a more efficient option.",
                ]
                flash(random.choice(medium_expense_suggestions))

          
                  
                
            
            for transaction in transactions:
                transaction['date'] = transaction['date'].strftime('%d %B, %Y')
                
                
                
            return render_template('transactionhistory.html', totalIncome=totalIncome, emi=emi, totalExpenses=totalExpenses, transactions=transactions)
        else:
            cur.execute(f"SELECT MONTHNAME('0000-{month}-00')")
            data = cur.fetchone()
            if month != "00":
                monthName = data[f'MONTHNAME(\'0000-{month}-00\')']
                msg = f"No Transactions Found For {monthName}, {year}"
            else:
                msg = f"No Transactions Found For {year}"
            return render_template('transactionhistory.html', result=result, msg=msg, emi=emi,totalIncome=totalIncome, totalExpenses=totalExpenses)

        # Close connection
        cur.close()
    else:
        # Create cursor for expenses
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s", [session['id']])
        data = cur.fetchone()
        totalExpenses = data['SUM(amount)']

        # Create cursor for income
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM incomedet WHERE user_id = %s", [session['id']])
        data = cursor.fetchone()

        totalIncome = data['SUM(amount)'] if data and data['SUM(amount)'] is not None else 0
        
         # Create cursor for emi
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT SUM(emi) FROM incomedet WHERE user_id = %s", [session['id']])
        data = cursor.fetchone()

        emi = data['SUM(emi)'] if data and data['SUM(emi)'] is not None else 0

        # Get Latest Transactions made by a particular user
        result = cur.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC", [session['id']])
        
        if result > 0:
            transactions = cur.fetchall()
            for transaction in transactions:
                transaction['date'] = transaction['date'].strftime('%d %B, %Y')
        
            
        
            return render_template('transactionhistory.html', totalIncome=totalIncome,emi=emi, totalExpenses=totalExpenses, transactions=transactions)
        else:
            flash('No Transactions Found', 'success')
            cur.close()
            return redirect(url_for('addTransactions'))

        # Close connection

        
    
    #return render_template('transactionhistory.html')
@app.route('/category')
def createBarCharts():
    cur = mysql.connection.cursor()
    result = cur.execute(
        f"SELECT Sum(amount) AS amount, category,subcat FROM transactions WHERE YEAR(date) = YEAR(CURRENT_DATE()) AND user_id = {session['id']} GROUP BY subcat ORDER BY subcat")
    if result > 0:
        transactions = cur.fetchall()
        values = []
        labels = []
        for transaction in transactions:
            values.append(transaction['amount'])
            labels.append(transaction['subcat'])

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(textinfo='label+value', hoverinfo='percent')
        fig.update_layout(
            title_text='Category Wise Pie Chart For Current Year')
        fig.show()
    cur.close()
    return redirect(url_for('transactionhistory'))

@app.route('/monthly_bar')
def monthlyBar():
    cur = mysql.connection.cursor()
    result = cur.execute(
        f"SELECT sum(amount) as amount, month(date) FROM transactions WHERE YEAR(date) = YEAR(CURRENT_DATE()) AND user_id = {session['id']} GROUP BY MONTH(date) ORDER BY MONTH(date)")
    if result > 0:
        transactions = cur.fetchall()
        year = []
        value = [] 
        for transaction in transactions:
            year.append(transaction['month(date)'])
            value.append(transaction['amount'])

        fig = go.Figure([go.Bar(x=year, y=value)])
        fig.update_layout(title_text='Monthly Bar Chart For Current Year')
        fig.show()
    cur.close()
    return redirect(url_for('transactionhistory'))

    
if __name__=="__main__":
    app.secret_key='71720a3f5af80150bd022b28bd25a1ba'
    app.run(debug=True)
