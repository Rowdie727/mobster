from flask import render_template
from mobster import app

@app.errorhandler(404)
def handle_error_404(error):
    return render_template('error_templates/error_404.html'), 404

@app.errorhandler(403)
def handle_error_403(error):
    return render_template('error_templates/error_403.html'), 403

@app.errorhandler(500)
def handle_error_500(error):
    return render_template('error_templates/error_500.html'), 500