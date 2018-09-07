from ...extension import mysql

class MedicalRecord:
    def __init__(self):
        self.cur = mysql.connection.cursor()
        self.id = 0
        self.height = ''
        self.weight = ''
        self.bmi = ''
        self.bp = ''
        self.pr = ''
        self.temperature = ''
        self.complaint = ''
        self.diagnosis = ''
        self.treatment = ''
        self.note = ''
        self.patient_id = ''
        self.patient = None

    def all(self):
        sql_query = '''
            SELECT 
                id, first_name, last_name, 
                gender, civil_status, date_of_birth,
                birth_place, address, contact_no
            FROM 
                patients
        '''

        self.cur.execute(sql_query)
        result = list(self.cur.fetchall())
        self.cur.close()

        return result

    def find(self, id):
        cur = mysql.connection.cursor()

        sql_query = '''
            SELECT 
                id, first_name, last_name, 
                gender, civil_status, date_of_birth,
                birth_place, address, contact_no
            FROM 
                patients 
            WHERE 
                id = %s
        '''

        cur.execute(sql_query, [id])
        result = cur.fetchone()
        cur.close()

        if result == None:
            return {}

        self.id = result['id']
        self.first_name = result['first_name']
        self.last_name = result['last_name']
        self.gender = result['gender']
        self.civil_status = result['civil_status']
        self.date_of_birth = result['date_of_birth']
        self.birth_place = result['birth_place']
        self.address = result['address']
        self.contact_no = result['contact_no']

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'civil_status': self.civil_status,
            'date_of_birth': self.date_of_birth,
            'birth_place': self.birth_place,
            'address': self.address,
            'contact_no': self.contact_no
        }

    def save_new(self):
        sql_query = '''
            INSERT INTO 
                patients
            SET 
                first_name = %s, 
                last_name = %s, 
                gender = %s, 
                civil_status = %s, 
                date_of_birth = %s,
                birth_place = %s, 
                address = %s, 
                contact_no = %s
        '''

        self.cur.execute(sql_query, [
            self.first_name,
            self.last_name,
            self.gender,
            self.civil_status,
            self.date_of_birth,
            self.birth_place,
            self.address,
            self.contact_no
        ])

        return mysql.connection.insert_id()

    def save_old(self):
        sql_query = '''
            UPDATE 
                patients 
            SET 
                first_name = %s, 
                last_name = %s, 
                gender = %s, 
                civil_status = %s, 
                date_of_birth = %s,
                birth_place = %s, 
                address = %s, 
                contact_no = %s
            WHERE 
                id = %s
        '''

        self.cur.execute(sql_query, [
            self.first_name,
            self.last_name,
            self.gender,
            self.civil_status,
            self.date_of_birth,
            self.birth_place,
            self.address,
            self.contact_no,
            self.id
        ])
    
        return self.id

    def save(self):
        id = 0
        if self.id == 0:
            id = self.save_new()
        else:
            id = self.save_old()

        mysql.connection.commit()
        self.cur.close()

        self.find(id)

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'civil_status': self.civil_status,
            'date_of_birth': self.date_of_birth,
            'birth_place': self.birth_place,
            'address': self.address,
            'contact_no': self.contact_no
        }

    def delete(self, id):
        sql_query = '''
            DELETE FROM
                patients
            WHERE
                id = %s
        '''

        if not self.find(id):
            return {}

        self.cur.execute(sql_query, [id])
        mysql.connection.commit()
        self.cur.close()

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'civil_status': self.civil_status,
            'date_of_birth': self.date_of_birth,
            'birth_place': self.birth_place,
            'address': self.address,
            'contact_no': self.contact_no
        }
    
