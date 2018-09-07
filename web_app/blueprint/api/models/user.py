from ...extension import mysql

class User:
    def __init__(self):
        self.cur = mysql.connection.cursor()
        self.id = 0
        self.name = ''
        self.username = ''
        self.password = ''

    def all(self):
        sql_query = '''
            SELECT 
                id, name, username, password
            FROM 
                users
        '''

        self.cur.execute(sql_query)
        result = list(self.cur.fetchall())
        self.cur.close()

        return result
    
    def find(self, id):
        cur = mysql.connection.cursor()

        sql_query = '''
            SELECT 
                id, name, username, password
            FROM 
                users 
            WHERE 
                id = %s
        '''

        cur.execute(sql_query, [id])
        result = cur.fetchone()
        cur.close()
        
        if result == None:
            return {}

        self.id = result['id']
        self.name = result['name']
        self.username = result['username']
        self.password = result['password']

        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password
        }

    def find_by_username(self, username):
        sql_query = '''
            SELECT 
                id, name, username, password
            FROM 
                users 
            WHERE 
                username = %s
        '''

        self.cur.execute(sql_query, [username])
        result = self.cur.fetchone()
        self.cur.close()
        
        if result == None:
            return {}

        self.id = result['id']
        self.name = result['name']
        self.username = result['username']
        self.password = result['password']

        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password
        }
        
    def save_new(self):
        sql_query = '''
            INSERT INTO 
                users 
            SET 
                username = %s, 
                password = %s, 
                name = %s
        '''

        self.cur.execute(sql_query, [
            self.username, 
            self.password, 
            self.name
        ])

        return mysql.connection.insert_id()

    def save_old(self):
        sql_query = '''
            UPDATE 
                users 
            SET 
                username = %s, 
                password = %s, 
                name = %s
            WHERE 
                id = %s
        '''

        self.cur.execute(sql_query, [
            self.username, 
            self.password, 
            self.name,
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
            'name': self.name,
            'username': self.username,
            'password': self.password
        }

    def delete(self, id):
        sql_query = '''
            DELETE FROM
                users
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
            'name': self.name,
            'username': self.username,
            'password': self.password
        }
