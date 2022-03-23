import datetime
import logging as lg
import csv
import difflib as dif


# class Candidacy(db.Model):
#     """Create a table Candidacy on the candidature database

#     Args:
#         db.Model: Generates columns for the table

#     """

#     id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),nullable=False)
#     entreprise = db.Column(db.String(), nullable=True)
#     ville_entreprise = db.Column(db.String(), nullable=True)
#     contact_full_name = db.Column(db.String(length=50), nullable=False)
#     contact_email = db.Column(db.String(length=50), nullable=True)
#     contact_mobilephone = db.Column(db.String(length=50), nullable=True)
#     date = db.Column(db.String(), nullable=True, default= datetime.date.today())
#     status = db.Column(db.String(), nullable=True, default="En cours")
#     comment = db.Column(db.String(), nullable=True)
#     relance = db.Column(db.Boolean,nullable=False, default=False)
#     date_last_relance = db.Column(db.String(), nullable=False, default=datetime.date.today())

#     def __repr__(self):
#         return f' Candidat id : {self.user_id}'

#     def json(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'entreprise': self.entreprise,
#             'ville_entreprise': self.ville_entreprise,
#             'contact_full_name': self.contact_full_name,
#             'contact_email': self.contact_email,
#             'contact_mobilephone': self.contact_mobilephone,
#             'date': self.date,
#             'status': self.status,
#             'comment': self.comment
#         }
        
        
#     def json_board(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'entreprise': self.entreprise,
#             'ville_entreprise': self.ville_entreprise,
#             'contact_full_name': self.contact_full_name,
#             'contact_email': self.contact_email,
#             'contact_mobilephone': self.contact_mobilephone,
#             'date': self.date,
#             'status': self.status,
#             'comment': self.comment,
#             'date_last_relance' : self.date_last_relance,
#             'relance' : self.relance
#         }

#     def json_test(self):
#         return {

#             'entreprise': self.entreprise,
#             'contact_full_name': self.contact_full_name,
#             'contact_email': self.contact_email,
#             'status': self.status
#         }

#     @classmethod
#     def find_by_user_id(self, cls, user_id):
#         candidacy_list = []
#         for candidacy in cls.query.filter_by(user_id=user_id).all():
#             candidacy_list.append(candidacy.json())
#         return candidacy_list
    
#     @classmethod
#     def find_by_user_id_relance(self, cls, user_id):
#         candidacy_list = []
#         for candidacy in cls.query.filter_by(user_id=user_id).all():
#             candidacy_list.append(candidacy.json_board())
#         return candidacy_list
    
#     @classmethod
#     def check_entreprise_exist(cls,entreprise):
#         entreprise_commune = []
#         for candidacy in cls.query.group_by(cls.entreprise).with_entities(cls.entreprise):
#             ratio = dif.SequenceMatcher(a=candidacy.entreprise, b=entreprise).ratio()
#             if ratio > 0.75 and ratio < 1:
#                 entreprise_commune.append('- ' + candidacy.entreprise)
#         return entreprise_commune
        

#     @classmethod
#     def get_all_in_list_with_user_name(cls):
#         candidacy_list = []
#         for candidacy in cls.query.join(Users).with_entities(Users.first_name, cls.id, cls.entreprise, cls.contact_full_name, cls.contact_email, cls.contact_mobilephone, cls.date, cls.status).all():
#             candidacy_list.append(candidacy)
#         return candidacy_list

#     @classmethod
#     def get_all_in_list_entreprise(cls):
#         entreprise_list=[]
#         # for entreprise_info in cls.query.join(Users).with_entities(Users.first_name, Users.last_name, cls.user_id ,cls.entreprise,cls.entreprise_ville, cls.contact_full_name, cls.contact_email, cls.contact_mobilephone).all():
#         for entreprise_info in cls.query.join(Users).with_entities(cls.user_id ,cls.entreprise,cls.ville_entreprise, cls.contact_full_name, cls.contact_email, cls.contact_mobilephone).all():
#             entreprise_list.append(entreprise_info)
#         return entreprise_list

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
