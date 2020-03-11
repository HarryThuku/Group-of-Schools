from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager
from flask import jsonify


class Roles(db.Model):
    '''
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    role_detail = db.Column(db.String(100), unique = True, index = True)
    role_description = db.Column(db.Text, nullable = False)
    activate = db.Column(db.Boolean)
    activation_status = db.Column(db.String(300))
    time_stamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, role_data, role_desc, activation):
        '''
        '''
        self.role_detail = str(role_data).strip().title()
        self.role_description = role_desc
        self.activate = activation
        self.activation_status = self.statusGenerator(activation, role_data)
        self.time_stamp = datetime.utcnow().strftime('%H:%m')

    def statusGenerator(self, validation, role_data):
        '''
        '''
        if validation:
            return f'role {role_data} is currently legible.'.capitalize()
        return f'role {role_data} currently NOT legible'.capitalize()

    # read method
    @classmethod
    def find_by_id(cls, id):
        '''
        '''
        return cls.query.filter_by(id = id).first()

    # read method
    @classmethod
    def list_all_roles(cls):
        '''
        '''
        return cls.query.all()

    # create method
    @classmethod
    def create_role(cls, role):
        '''
        '''
        db.session.add(role)
        db.session.commit()
        return True

    # update method
    @classmethod
    def update_role(cls, r_id, role_data):
        '''
        '''
        if r_id and role_data:
            for item in list( role_data ):
                cls.query.filter_by(id = int(r_id)).update({f'{list(item.keys())[0]}' : f'{list(item.values())[0]}'})
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_teacher(cls, r_id):
        '''
        '''
        role = cls.query.filter_by(id = r_id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        roles_list = cls.query.all()
        if roles_list:
            for role in roles_list:
                db.session.delete(role)
            db.session.commit()
            return True
        return False


    def __repr__(self):
        '''
        '''
        return f'Role : {self.role_detail}.'



@login_manager.user_loader
def load_teacher(teacher_id):
    '''
    '''
    return Teachers.query.get(int(teacher_id))


class SchoolCategory(db.Model):
    '''
    '''
    __tablename__ = 'school_categories'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(255), unique = True)
    category_initials = db.Column(db.String(50), unique = True)
    category_desc = db.Column(db.String(300))
    valid = db.Column(db.Boolean)
    validation_status = db.Column(db.String(200))
    time_stamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    schools_cat_rship = db.relationship('Schools', backref = 'school_category', lazy = "dynamic")

    def __init__(self, cat_data, cat_initials, cat_desc, validated):
        '''
        '''
        self.category = str(cat_data).strip().title()
        self.category_initials = str(cat_initials).strip().upper()
        self.category_desc = str(cat_desc).strip().capitalize()
        self.valid = validated
        self.validation_status = self.statusGenerator(cat_data, validated)
        self.time_stamp = datetime.utcnow().strftime("%H:%M")

    @classmethod
    def statusGenerator(cls, cat_data, validated):
        '''
        '''
        if validated:
            return f'{cat_data} is a valid registration category.'
        return f'{cat_data} is currently not a valid school registration category.'

    @classmethod
    def create_category(cls, instance):
        '''
        '''
        db.session.add(instance)
        db.session.commit()
        return True


class SchoolStudentsGender(db.Model):
    '''
    '''
    __tablename__ = 'school_students_gender'
    id = db.Column(db.Integer, primary_key = True)
    gender = db.Column(db.String(50), unique = True, index = True)
    gender_initials = db.Column(db.String(50), unique = True, index = True)
    description = db.Column(db.String(200))
    validated = db.Column(db.Boolean)
    validation_status = db.Column(db.String(200))
    time_stamp = db.Column(db.String(50))
    schools_gen_rship = db.relationship('Schools', backref = 'school_gender', lazy = "dynamic")

    def __init__(self, gender_data, gender_intls, desc, validation):
        '''
        '''
        self.gender = str(gender_data).strip().title()
        self.gender_initials = str(gender_intls).strip().upper()
        self.description = str(desc).strip().capitalize()
        self.validated = validation
        self.validation_status = self.statusGenerator(gender_data, validation)
        self.time_stamp = datetime.utcnow().strftime("%H:%M")

    @classmethod
    def statusGenerator(cls, gender_data, validation):
        '''
        '''
        if validation:
            return f'{gender_data} is a valid sex for registration.'
        return f'{gender_data} is not a valid sex for registration.'

    @classmethod
    def create_sch_stdnt_sex(cls, instance):
        '''
        '''
        db.session.add(instance)
        db.session.commit()
        return True


class AmenityCategories(db.Model):
    '''
    '''
    __tablename__ = 'amenity_categories'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(50), index = True, unique = True)
    description = db.Column(db.String(200))
    validated = db.Column(db.Boolean)
    validation_status = db.Column(db.String(200))
    time_stamp = db.Column(db.String(50))
    amenity_rship = db.relationship('Amenities', backref = 'sch_amenity_rship', lazy = "dynamic")

    def __init__(self, category_data, desc, valid):
        '''
        '''
        self.category = str(category_data).strip().title()
        self.description = ' '.join([x.strip().capitalize() for x in str(desc).strip().split(' ') if x])
        self.validated = valid
        self.validation_status = self.statusGenerator(category_data, valid)
        self.time_stamp = datetime.utcnow().strftime("%D - %H:%M:%S")

    @classmethod
    def create_amenity_cat(cls, instance):
        '''
        '''
        db.session.add(instance)
        db.session.commit()
        return True

class Amenities(db.Model):
    '''
    '''
    __tablename__ = 'amenities'
    id = db.Column(db.Integer, primary_key = True)
    amenity = db.Column(db.String(50), unique = True, index = True)
    category_id = db.Column(db.Integer, db.ForeignKey('amenity_categories.id'))
    description = db.Column(db.String(200))
    validated = db.Column(db.Boolean)
    validation_status = db.Column(db.String(200))
    time_stamp = db.Column(db.String(50))
    school_amenity_rship = db.relationship('SchoolAmenities', backref = 'sch_amenity', lazy = "dynamic")


class SchoolAmenities(db.Model):
    '''
    '''
    __tablename__ = 'school_amenities'
    id = db.Column(db.Integer, primary_key = True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenities.id'))

    def init(self, s_id, a_id):
        '''
        '''
        self.school_id = s_id
        self.amenity_id = a_id
    
    @classmethod
    def create_Sch_Amenity(cls, instance):
        '''
        '''
        db.session.add(instance)
        db.session.commit()
        return True


class Schools(db.Model):
    '''
    '''
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key = True)
    school_name = db.Column(db.String(200))
    school_initials = db.Column(db.String(50))
    school_motto = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('school_categories.id'))
    gender_id = db.Column(db.Integer, db.ForeignKey('school_students_gender.id'))
    location = db.Column(db.String(200))
    time_stamp = db.Column(db.String(50))
    amenity = db.relationship('SchoolAmenities', backref = 'school', lazy = "dynamic")

    def __init__(self, name, initials, motto, category, admitted_gender, location):
        '''
        '''
        self.school_name = str(name).strip().title()
        self.school_initials = str(initials).strip().upper()
        self.school_motto = ('. '.join( [ item.strip().capitalize() for x in str(motto).split(".")  ] )).strip(' ')
        self.category_id = int(category)
        self.gender_id = int(admitted_gender)
        self.location = str(location)
        self.time_stamp = datetime.utcnow().strptime()

    @classmethod
    def create_school(cls, instance):
        '''
        '''
        db.session.add(instance)
        db.session.commit()
        return True


class Teachers(UserMixin, db.Model):
    '''
    '''
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    surName = db.Column(db.String(200))
    portal_handle = db.Column(db.String(50))
    nationalId = db.Column(db.Integer, unique = True, index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    bio = db.Column(db.String(255))
    reg_date = db.Column(db.String())
    TSC_No = db.Column(db.Integer, unique = True, index = True)
    pass_secure = db.Column(db.String(255))

    def __init__(self, first_Name, last_Name, sur_Name, national_ID, Email, Bio, Tsc_No, password):
        '''
        '''
        self.firstName = str(first_Name).strip().capitalize()
        self.lastName = str(last_Name).strip().capitalize()
        self.surName = str(sur_Name).strip().capitalize()
        self.nationalId = int(national_ID)
        self.email = str(Email).strip()
        self.bio = str(Bio)
        self.TSC_No = int(Tsc_No)
        self.reg_date = datetime.utcnow().strftime("%D - %H:%M:%S")
        self.pass_secure = generate_password_hash(password)

    # read method
    @classmethod
    def find_by_email(cls, email_addr):
        '''
        '''
        return cls.query.filter_by(email = email_addr).first()

    # read method
    @classmethod
    def find_by_tscno(cls, tscno):
        '''
        '''
        return cls.query.filter_by(TSC_No = tscno).first()

    # read method
    @classmethod
    def find_by_id(cls, ID):
        '''
        '''
        return cls.query.filter_by(id = ID).first()

    @classmethod
    def find_by_names(cls, name):
        search_key_words = [ x.title() for x in str(name).strip().split(' ') ]
        teachers_list = cls.query.all()
        results = []
        if len(search_key_words)>1:
            '''
            find by matching first name and last name patterns
            '''
            for curr_teacher in teachers_list:
                if len(search_key_words[0]) >= len(curr_teacher.firstName):
                    first_name = curr_teacher.firstName
                    last_name = curr_teacher.lastName
                    if first_name == search_key_words[0][:len(curr_teacher.firstName)] and last_name[:len(search_key_words[1])] == search_key_words[1]:
                        results.append(curr_teacher)
                elif len(search_key_words[0]) < len(curr_teacher.firstName):
                    first_name = curr_teacher.firstName
                    last_name = curr_teacher.lastName
                    if first_name[:len(search_key_words[0])] == search_key_words[0] and last_name[:len(search_key_words[1])] == search_key_words[1]:
                        results.append(curr_teacher)
        else:
            '''
            Find only by first name or last name patterns.
            '''
            for curr_teacher in teachers_list:
                if len(search_key_words[0]) >= len(curr_teacher.firstName) or len(search_key_words[0]) >= len(curr_teacher.lastName):
                    first_name = curr_teacher.firstName
                    last_name = curr_teacher.lastName
                    if first_name == search_key_words[0][:len(curr_teacher.firstName)] or last_name == search_key_words[0][:len(curr_teacher.lastName)]:
                        results.append(curr_teacher)
                elif len(search_key_words[0]) < len(curr_teacher.firstName) or len(search_key_words[0]) < len(curr_teacher.lastName):
                    first_name = curr_teacher.firstName
                    last_name = curr_teacher.lastName
                    if first_name[:len(search_key_words[0])] == search_key_words[0] or last_name[:len(search_key_words[0])] == search_key_words[0]:
                        results.append(curr_teacher)
        return results

    # read method
    @classmethod
    def list_all_teachers(cls):
        '''
        '''
        return cls.query.all()

    # create method
    @classmethod
    def create_teacher(cls, user):
        '''
        '''
        db.session.add(user)
        db.session.commit()
        return True

    # update method
    @classmethod
    def update_teacher(cls, t_id, teacher_data):
        '''
        '''
        if t_id and teacher_data:
            for item in list( teacher_data ):
                cls.query.filter_by(id = int(t_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_teacher(cls, t_id):
        '''
        '''
        teacher = cls.query.filter_by(id = t_id).first()
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        to_delete = cls.query.all()
        if to_delete:
            for teacher in to_delete:
                db.session.delete(teacher)
            db.session.commit()
            return True
        return False

    @property
    def password(self):
        '''
        '''
        raise AttributeError('-- You cannot read the password attribute. --')

    @password.setter
    def hash_password(self, password_data):
        '''
        '''
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, trial_password):
        '''
        '''
        return check_password_hash(self.pass_secure, trial_password)

    def __repr__(self):
        '''
        '''
        return f'User : {self.firstName} - {self.lastName}.'


class Streams(db.Model):
    '''
    '''
    __tablename__ = 'streams'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True, index = True)
    initals = db.Column(db.String(4), unique = True, index = True)
    reg_date = db.Column(db.String())
    valid = db.Column(db.Boolean)
    validation_status = db.Column(db.String(255))

    def __init__(self, strm_name, strm_initials, validated):
        '''
        '''
        self.name = str(strm_name).strip().title()
        self.initals = str(strm_initials).strip().upper()
        self.reg_date = datetime.utcnow().strftime("%H:%M")
        self.valid = validated
        self.validation_status = statusGenerator(validated, strm_name)

    def statusGenerator(self, validation, strm_name):
        '''
        '''
        if validation:
            return f'subjects under {strm_name} category are legible.'.capitalize()
        return f'subjects under {strm_name} category are NOT legible'.capitalize()

    @classmethod
    def find_by_name(cls, str_name):
        '''
        '''
        return cls.query.filter_by(name = str_name).first()

    @classmethod
    def find_by_id(cls, str_id):
        '''
        '''
        return cls.query.filter_by(id = str_id).first()

    @classmethod
    def list_all_streams(cls):
        '''
        '''
        return cls.query.all()

    @classmethod
    def create_stream(cls):
        '''
        '''
        db.session.add(cls)
        db.session.commit()
        return True

    @classmethod
    def delete_stream(cls, s_id):
        '''
        '''
        strm = cls.query.filter_by(id = s_id).first()
        if strm:
            db.session.delete(strm)
            return True
        return False

    @classmethod
    def delete_all(cls):
        '''
        '''
        strms = cls.query.all()
        if strms:
            for item in strms:
                db.session.delete(item)
            db.session.commit()
            return True
        return False

    @classmethod
    def update_stream(cls, str_id, str_data):
        '''
        '''
        if str_id and str_data:
            for item in list( str_data ):
                cls.query.filter_by(id = int(str_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
            db.session.commit()
            if cls.valid:
                cls.statusGenerator(cls.valid, cls.name)
                db.session.commit()
            return True
        return False

    # debug stream data
    def __repr__(self):
        '''
        '''
        return f'Stream : {self.name}.'


# @stdt_login_manager.user_loader
# def load_student(student_id):
#     '''
#     '''
#     return Students.query.get(int(student_id))

class Students(db.Model):
    '''
    '''
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    surName = db.Column(db.String(200))
    NEMIS_No = db.Column(db.Integer, unique = True, index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    reg_date = db.Column(db.String())

    def __init__(self, first_Name, last_Name, sur_Name, Nemis_No, email):
        '''
        '''
        self.firstName = str(first_Name).strip().capitalize()
        self.lastName = str(last_Name).strip().capitalize()
        self.surName = str(sur_Name).strip().capitalize()
        self.NEMIS_No = int(Nemis_No)
        self.email = str(email).strip()
        self.reg_date = datetime.utcnow().strftime("%H:%M")

    @classmethod
    def create_student(cls):
        '''
        '''
        db.session.add(cls)
        db.session.commit()
        return True

    @classmethod
    def list_all_students(cls):
        '''
        '''
        return cls.query.all()

    @classmethod
    def find_student_by_id(cls, s_id):
        '''
        '''
        return cls.query.filter_by(id = s_id)

    @classmethod
    def find_by_names(cls, name):
        search_key_words = [ x.title() for x in str(name).strip().split(' ')]
        students_list = cls.query.all()
        results = []
        if len(search_key_words)>1:
            '''
            find by matching first name and last name patterns.
            '''
            for curr_stud in students_list:
                if len(search_key_words[0]) >= len(curr_stud.firstName):
                    first_name = curr_stud.firstName
                    last_name = curr_stud.lastName
                    if first_name == search_key_words[0][:len(curr_stud.firstName)] and last_name[:len(search_key_words[1])] == search_key_words[1]:
                        results.append(curr_stud)
                elif len(search_key_words[0]) < len(curr_stud.firstName):
                    first_name = curr_stud.firstName
                    last_name = curr_stud.lastName
                    if first_name[:len(search_key_words[0])] == search_key_words[0] and last_name[:len(search_key_words[1])] == search_key_words[1]:
                        results.append(curr_stud)
        else:
            '''
            Find only by first name or last name patterns.
            '''
            for curr_stud in students_list:
                if len(search_key_words[0]) >= len(curr_stud.firstName) or len(search_key_words[0]) >= len(curr_stud.lastName):
                    first_name = curr_stud.firstName
                    last_name = curr_stud.lastName
                    if first_name == search_key_words[0][:len(curr_stud.firstName)] or last_name == search_key_words[0][:len(curr_stud.lastName)]:
                        results.append(curr_stud)
                elif len(search_key_words[0]) < len(curr_stud.firstName) or len(search_key_words[0]) < len(curr_stud.lastName):
                    first_name = curr_stud.firstName
                    last_name = curr_stud.lastName
                    if first_name[:len(search_key_words[0])] == search_key_words[0] or last_name[:len(search_key_words[0])] == search_key_words[0]:
                        results.append(curr_stud)
        return results

    @classmethod
    def update_student(cls, s_id, student_data):
        '''
        '''
        if s_id and student_data:
            for item in list( student_data ):
                cls.query.filter_by(id = int(s_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_student(cls, t_id):
        '''
        '''
        student = cls.query.filter_by(id = t_id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        all_students = cls.query.all()
        if all_students:
            for student in all_students:
                db.session.delete(student)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return f'Student : {self.firstName} - {self.lastName}.'



class SubjectCategories(db.Model):
    '''
    '''
    __tablename__ = 'subjectCategories'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(250), unique = True, index = True)
    initials = db.Column(db.String(205), unique = True, index = True)
    valid = db.Column(db.Boolean)
    validation_status = db.Column(db.String(255))

    def __init__(self, subject_category, category_initials, validation_data):
        '''
        '''
        self.category = str(subject_category).strip().title()
        self.initials = str(category_initials).strip().upper()
        self.valid = str(validation_data).strip().title()
        self.validation_status = self.statusGenerator(validation_data, subject_category)

    def statusGenerator(self, validation_data, subject_category):
        '''
        '''
        if validation_data:
            return f'subjects under {subject_category} category are legible.'.capitalize()
        return f'subjects under {subject_category} category are NOT legible'.capitalize()

    @classmethod
    def find_by_id(cls, sc_id):
        '''
        '''
        return cls.query.filter_by(id = sc_id).first()

    @classmethod
    def find_by_name(cls, name):
        '''
        '''
        return cls.query.filter_by(category = str(name).strip().title()).first()

    @classmethod
    def find_by_initials(cls, intls):
        '''
        '''
        return cls.query.filter_by(initials = str(intls).strip().upper()).first()

    @classmethod
    def update_subj_cat(cls, sc_id, sc_data):
        '''
        '''
        if sc_id and sc_data:
            for item in list(sc_data):
                cls.query.filter_by(id = int(sc_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
            db.session.commit()
            if cls.valid:
                cls.statusGenerator(cls.valid, cls.category)
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_subj_cat(cls, sc_id):
        '''
        '''
        subject_category = cls.query.filter_by(id = sc_id).first()
        if subject_category:
            db.session.delete(subject_category)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        all_subj_cat = cls.query.all()
        if all_subj_cat:
            for teacher in all_subj_cat:
                db.session.delete(teacher)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        '''
        '''
        return f'Subject category : {self.category} - {self.initials}.'


class Subjects(db.Model):
    '''
    '''
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(255), unique = True, index = True)
    initials = db.Column(db.String(), unique = True, index = True)
    # category = db.Column(db.ForeignKey(''))#foreignKey to category
    valid = db.Column(db.Boolean)
    validationStatus = db.Column(db.String(255))

    def __init__(self, subject_name, subject_initials, validation):
        '''
        '''
        self.subject = str(subject_name).strip().title()
        self.initials = str(subject_initials).strip().upper()
        self.valid = str(validation).strip().title()
        self.validationStatus = self.statusGenerator(validation, subject_name)

    def statusGenerator(self, validation, subject_name):
        '''
        Generates a status for a subject by checking if it has been marked as offered.
        '''
        if validation:
            return f'{subject_name} is Offered under our curriculum, and is registered.'.capitalize()
        return f'{subject_name} has NOT been cleared to curriculum but is registered.'.capitalize()

    @classmethod
    def find_by_id(cls, s_id):
        '''
        '''
        return cls.query.filter_by(id = s_id).first()

    @classmethod
    def find_by_name(cls, subj):
        '''
        '''
        return cls.query.filter_by(subject = str(subj).strip().title()).first()

    @classmethod
    def find_by_initials(cls, intls):
        '''
        '''
        return cls.query.filter_by(initials = str(intls).strip().upper()).first()


    @classmethod
    def update_subj_cat(cls, subject_id, subject_data):
        '''
        '''
        if subject_id and sc_data:
            for item in list(sc_data):
                cls.query.filter_by(id = int(subject_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
            db.session.commit()
            if cls.valid:
                cls.statusGenerator(cls.valid, cls.subject)
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_subj(cls, sc_id):
        '''
        '''
        subject = cls.query.filter_by(id = sc_id).first()
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        all_subjects = cls.query.all()
        if all_subjects:
            for subject in all_subjects:
                db.session.delete(subject)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        '''
        '''
        return f'Subject : {self.subject} - {self.initials}.'


class Relationships(db.Model):
    '''
    '''
    __tablename__ = 'relationships'
    id = db.Column(db.Integer, primary_key = True)
    relation = db.Column(db.String(), unique = True, index = True)
    valid = db.Column(db.Boolean)
    validationStatus = db.Column(db.String())

    def __init__(self, parental_realation, validation):
        '''
        '''
        self.relation = str(parental_realation).strip().title()
        self.valid = str(validation).strip().title()
        self.validationStatus = self.statusGenerator(validation, parental_realation)

    def statusGenerator(validation, parental_realation):
        '''
        '''
        if validation:
            return f'{parental_realation} relation is legible as a student representative.'.capitalize()
        return f'{parental_realation} relation is NOT legible as a student representative.'.capitalize()

    @classmethod
    def find_by_id(cls, rship_id):
        '''
        '''
        return cls.query.filter_by(id = rship_id).first()

    @classmethod
    def find_by_name(cls, rship):
        '''
        '''
        return cls.query.filter_by(category = str(rship).strip().title()).first()

    @classmethod
    def update_relationship(cls, rship_id, rship_data):
        '''
        '''
        if rship_id and rship_data:
            for item in list(rship_data):
                cls.query.filter_by(id = int(rship_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
            db.session.commit()
            if cls.valid:
                cls.statusGenerator(cls.valid, cls.relation)
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_relationship(cls, rship_id):
        '''
        '''
        relationship = cls.query.filter_by(id = rship_id).first()
        if relationship:
            db.session.delete(relationship)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        all_relations = cls.query.all()
        if all_relations:
            for relation in all_relations:
                db.session.delete(relation)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        '''
        '''
        return f'Relationship : {self.relation}.'


class PhoneNumbers(db.Model):
    '''
    '''
    __tablename__ = 'phoneNumber'
    id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.Integer, unique = True, index = True)
    primary = db.Column(db.Boolean)
    owner = db.Column(db.Integer, db.ForeignKey('parents.id'))

    def __init__(self, phone_number, is_primary_phone, phone_owner):
        '''
        '''
        self.phone = str(phone_number).strip()
        self.primary = self.set_primary(is_primary_phone, phone_owner)
        self.owner = int(phone_owner)

    @classmethod
    def set_primary(cls, is_primary_phone, phone_owner):
        '''
        '''
        primary_p = is_primary_phone.strip().title()
        if primary_p:
            owners_contacts = cls.query.filter_by(id = phone_owner).all()
            for contact in owners_contacts:
                contact.update({'phone' : 'False'})
            db.session.commit()
            cls.primary = primary_p

    def __repr__(self):
        '''
        '''
        return f'Phone number : {self.phone}.'


class Parents(db.Model):
    '''
    '''
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(55))
    lastName = db.Column(db.String(55))
    surName = db.Column(db.String(55))
    email = db.Column(db.String(50), unique = True, index = True)
    password_secure = db.Column(db.String(30))
    phone = db.relationship(PhoneNumbers, backref = 'phone_number', lazy = 'dynamic')

    def __init__(self, first_Name, last_Name, sur_Name, email_addr, password_data):
        '''
        '''
        self.firstName = str(first_Name).strip().capitalize()
        self.lastName = str(last_Name).strip().capitalize()
        self.surName = str(sur_Name).strip().capitalize()
        self.email = str(email_addr).strip()
        self.password_secure = str(password_data)

    # read method
    @classmethod
    def find_by_email(cls, email_addr):
        '''
        '''
        return cls.query.filter_by(email = email_addr).first()

    # read method
    @classmethod
    def find_by_id(cls, ID):
        '''
        '''
        return cls.query.filter_by(id = ID).first()

    @classmethod
    def find_by_names(cls, name):
        search_key_words = [ x.title() for x in str(name).strip().split(' ')]
        parents_list = cls.query.all()
        results = []
        if len(search_key_words)>1:
            '''
            find by matching first name and last name patterns
            '''
            for curr_parent in parents_list:
                if len(search_key_words[0]) >= len(curr_parent.firstName):
                    first_name = curr_parent.firstName
                    last_name = curr_parent.lastName
                    if first_name == search_key_words[0][:len(curr_parent.firstName)] and last_name[:len(search_key_words[1])] == search_key_words[1]:
                        results.append(curr_parent)
                elif len(search_key_words[0]) < len(curr_parent.firstName):
                    first_name = curr_parent.firstName
                    last_name = curr_parent.lastName
                    if first_name[:len(search_key_words[0])] == search_key_words[0] and last_name[:len(search_key_words[1])] == search_key_words[1]:
                        results.append(curr_parent)
        else:
            '''
            Find only by first name or last name patterns.
            '''
            for curr_parent in parents_list:
                if len(search_key_words[0]) >= len(curr_parent.firstName) or len(search_key_words[0]) >= len(curr_parent.lastName):
                    first_name = curr_parent.firstName
                    last_name = curr_parent.lastName
                    if first_name == search_key_words[0][:len(curr_parent.firstName)] or last_name == search_key_words[0][:len(curr_parent.lastName)]:
                        results.append(curr_parent)
                elif len(search_key_words[0]) < len(curr_parent.firstName) or len(search_key_words[0]) < len(curr_parent.lastName):
                    first_name = curr_parent.firstName
                    last_name = curr_parent.lastName
                    if first_name[:len(search_key_words[0])] == search_key_words[0] or last_name[:len(search_key_words[0])] == search_key_words[0]:
                        results.append(curr_parent)
        return {'results' : [ {'first_name' : item.firstName, 'last_name' : item.lastName, 'sur_name' : item.surName, 'email' : item.email, 'phone' : item.phone.filter(PhoneNumbers.id==item.id).all()} for item in list(results)], "total_results" : len(list(results))}

    # read method
    @classmethod
    def list_all_parents(cls):
        '''
        '''
        return cls.query.all()

    # create method
    @classmethod
    def create_parent(cls, instance):
        '''
        '''
        db.session.add(instance)
        db.session.commit()
        return True
    
    # update method
    @classmethod
    def update_parent(cls, parent_id, parent_data):
        '''
        '''
        if parent_id and teacher_data:
            for item in list( parent_data ):
                cls.query.filter_by(id = int(parent_id)).update({f'{list(item.keys())[0]}':f'{list(item.values())[0]}'})
                db.session.commit()
            return True
        return False

    # delete method
    @classmethod
    def delete_parent(cls, parent_id):
        '''
        '''
        parent = cls.query.filter_by(id = parent_id).first()
        if parent:
            db.session.delete(parent)
            db.session.commit()
            return True
        return False

    # delete method
    @classmethod 
    def delete_all(cls):
        '''
        '''
        parents_list = cls.query.all()
        if parents_list:
            for parent in parents_list:
                db.session.delete(parent)
            db.session.commit()
            return True
        return False

    @property
    def password(self):
        '''
        '''
        raise AttributeError('-- You cannot read the password attribute. --')

    @password.setter
    def password(self, password):
        '''
        '''
        self.password_secure = generate_password_hash(password)

    def verify_password(self, trial_password):
        '''
        '''
        return (self.password_secure == trial_password)

    def __repr__(self):
        '''
        '''
        return f'Parent : {self.firstName} / {self.lastName}.'




all_tbls = {
    'teachers' : Teachers,
    'students' : Students,
    'subjects' : Subjects,
    'subjectCategories' : SubjectCategories,
    'streams' : Streams,
    'parents' : Parents,
    'phoneNumbers' : PhoneNumbers,
    'relationships' : Relationships
}