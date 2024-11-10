from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField
import pickle
from wtforms.validators import DataRequired
import pandas as pd

with open('movie_name.pkl','rb') as f:
    dictionary = pickle.load(f)

movie = pd.DataFrame(dictionary)

class InputForm(FlaskForm):
    movies = SelectField(label='Movie Name',
                         choices=sorted(movie.original_title.unique().tolist()),
                         validators=[DataRequired()])
    
    submit = SubmitField(label='Recommend')
