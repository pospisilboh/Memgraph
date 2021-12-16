from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired

class RecommendationForm(FlaskForm):

    choices = ['compareStr','levenshteinSimilarity', 'jaroDistance', 'jaroWinklerDistance']

    forename = StringField('Forename', validators=[DataRequired()])
    method = RadioField('Method', choices=choices, default='compareStr', validators=[DataRequired()])
    similarityMin = FloatField('Similarity Minimum', default=0.7, validators=[DataRequired()])

    submit = SubmitField('Submit')