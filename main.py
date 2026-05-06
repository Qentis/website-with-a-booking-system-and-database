from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/master/<int:master_id>')
def master_schedule(master_id):
    return render_template('schedule.html')
@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')
@app.route('/Booking')
def booking():
    return render_template('booking.html')