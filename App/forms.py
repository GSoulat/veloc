from logging import PlaceHolder
from flask_wtf import FlaskForm

from wtforms import PasswordField, EmailField, SubmitField, StringField, TextAreaField, FileField, BooleanField
from wtforms.fields import DateField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from .models import Users

# class AddCandidacy(FlaskForm):
#     """[Form to add candidacy]
#     """
#     entreprise = StringField(label='Entreprise', validators=[DataRequired(),Length(max=50)])
#     ville_entreprise = StringField(label='Ville de l\'entreprise', validators=[DataRequired(),Length(max=50)])
#     contact_full_name = StringField(label='Nom du contact', validators=[DataRequired(),Length(max=50)])
#     contact_email = EmailField(label='Email du contact', validators=[Length(max=50)])
#     contact_mobilephone = StringField(label='Téléphone du contact',validators=[Length(max=20)])
#     comment = TextAreaField(label='Commentaire',validators=[Length(max=500)])
#     status = SelectField(label='Statut',choices=[
#                          'En cours', 'Refusée', 'Acceptée en alternance', 'Besoin d\'aide'], validators=[DataRequired()])
#     date = DateField(label='Date de la candidature',validators=[DataRequired()],format='%Y-%m-%d')
#     print("En cours d'ajout")
#     submit = SubmitField(label='Ajouter')
