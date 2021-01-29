from flask import Flask, render_template, request, url_for,flash,redirect
from wtforms import Form, TextField, StringField, PasswordField, validators
import csv
from datetime import datetime
app=Flask(__name__)
feedbacks=[]
@app.route('/reviews')
def reviews():
    reader=csv.DictReader(open('data.csv',encoding='utf-8-sig'))
    l=[]
    for raw in reader:
        raw=dict(raw)
        raw['Rating']=int(raw['Rating'])
        l.append(raw)
    return render_template('feedback2.html',feedbacks=l)
def Feedback(username,product,rating,review):
    dt_string = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    feedback={
        'User Name':username,
        'Product Name':product,
        'Rating':int(rating),
        'Review':review,
        'Time':dt_string,
    }
    return feedback
def write_feedback(feedback):
    csv_columns = ['User Name','Product Name','Rating','Review','Time']
    with open('data.csv','a') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
        writer.writerow(feedback)
class reviewForm(Form):
    username = TextField('User Name', [validators.Length(min=3, max=25),validators.DataRequired()])
    product = StringField('product', [validators.Length(min=3, max=25),validators.DataRequired()])
    review=StringField('review',[validators.DataRequired()])
    rating=StringField('rating',[validators.DataRequired()])
@app.route('/')
def form():
    return render_template('forms.html',form={'username':'','product':'','review':'','rating':''})
@app.route('/feedback',methods=['POST','GET'])
def feedback():
    form=reviewForm(request.form)
    print(form.validate())
    if request.method=='POST' and form.validate():
        feedback=Feedback(form.username.data,form.product.data,form.rating.data,form.review.data)
        write_feedback(feedback)
        return redirect(url_for('reviews'))
    else:
        return render_template('forms.html',form=form)
app.run(debug=True)