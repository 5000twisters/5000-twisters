from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace 'your-secret-key' with a real secret key

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_preference = SelectField('Contact Preference', choices=[('email', 'Email'), ('phone', 'Phone')])
    contact_info = StringField('Contact Info', validators=[DataRequired(), Email()])
    commitment_level = SelectField('Are you in?', choices=[('in', "I'm in!"), ('try', "I'll try"), ('maybe', 'Maybe...'), ('spread', "Nah, but I'll spread the word"), ('nothing', 'I want nothing to do with this')])
    update_preferences = SelectField('Update Preferences', choices=[('goal', 'Tell me when you reach your goal'), ('updates', 'Send me occasional progress updates'), ('never', 'Never contact me')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
        db = client['event_db']  # Replace 'event_db' with your database name
        collection = db['registrations']  # Replace 'registrations' with your collection name

        # Check if email/phone number already exists
        if collection.find_one({'contact_info': form.contact_info.data}):
            return 'This contact info has already been used.'
        
        # Insert the new registration into the database
        registration = {
            'name': form.name.data,
            'contact_preference': form.contact_preference.data,
            'contact_info': form.contact_info.data,
            'commitment_level': form.commitment_level.data,
            'update_preferences': form.update_preferences.data
        }
        collection.insert_one(registration)

        # Update the counter and progress bar
        all_in_count = collection.count_documents({'commitment_level': 'in'})
        progress = (all_in_count / 5000) * 100

        return render_template('thank_you.html', progress=progress)
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
