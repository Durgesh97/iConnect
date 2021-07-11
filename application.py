import os
import uuid
from flask import Flask,render_template,request, Response, redirect
from werkzeug.utils import secure_filename
from db import db_init, db
from models import   Product
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


#static file path
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

# ROWS_PER_PAGE = 2
@app.route("/")
def index():
	page= request.args.get('page',1, type=int)
	# posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
	# rows = Product.query.paginate(page,per_page=ROWS_PER_PAGE)
	rows=Product.query.all()
	return render_template("index.html", rows=rows)

#merchant home page to add new products and edit existing products
@app.route("/add", methods=["GET", "POST"], endpoint='add')
def home():
	if request.method == "POST":
		image = request.files['image']
		filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
		image.save(os.path.join("static/images", filename))
		name = request.form.get("name")
		description = request.form.get("desc")
		price = request.form.get("price")
		new_pro = Product(name=name,description=description,price=price, filename=filename)
		db.session.add(new_pro)
		db.session.commit()
		all_prod = Product.query.all()
		return render_template("home.html", all_prod=all_prod, message="Product added")
	
	all_prod = Product.query.all()
	return render_template("home.html", all_prod=all_prod)


@app.route('/edit')
def products():
    rows = Product.query.all()
    return render_template("edit.html", rows=rows)
    
@app.route('/delete/<int:pro_id>')
def delete(pro_id):
    prod = Product.query.filter_by(pro_id=pro_id).first()
    db.session.delete(prod)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:pro_id>", methods=["GET", "POST"], endpoint='update')
def edit(pro_id):
	#select only the editing product from db
	result = Product.query.filter_by(pro_id = pro_id).first()
	if request.method == "POST":
		name = request.form.get("name")
		description = request.form.get("description")
		price= request.form.get("price")
		result.name = name
		result.description = description
		result.price= price
		db.session.commit()
		rows = Product.query.filter_by(pro_id=pro_id).first()
		return redirect("/")
	return render_template("update.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)