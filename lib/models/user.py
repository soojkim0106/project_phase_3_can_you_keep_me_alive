from models.__init__ import CONN, CURSOR
from sqlite3 import IntegrityError
class User:
    all = {}
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
    
    def __repr__(self):
        return f"User {self.id}: {self.name}"

#! Properties and Attributes
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError('Name must be a string')
        elif len(new_name) < 2:
            raise ValueError('Name must be 2 or more characters')
        else:
            self._name = new_name

#!Association Methods

#! ORM class methods
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT
                        );
                    """
                )
        except Exception as e:
            return e

    @classmethod
    def drop_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                """
                    DROP TABLE IF EXISTS users;
                """
                )
        except Exception as e:
            return e

    @classmethod
    def create(cls, name):
        try:
            with CONN:
                new_user = cls(name)
                new_user.save()
                return new_user
        except Exception as e:
            print("Error creating new user:", e)
        
    @classmethod
    def instance_from_db(cls, row):
        try:
            user = cls(row[1], row[0])
            cls.all[user.id] = user
            return user
        except Exception as e:
            print("Error fetching user from database:", e)

    @classmethod
    def get_all(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM users;
                    """
                )
                rows = CURSOR.fetchall()
                return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            print("Error fetching all users:", e)

    @classmethod
    def find_by_name(cls, name):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM users WHERE name =?;
                    """,
                    (name,),
                )
                row = CURSOR.fetchone()
                return cls.instance_from_db(row) if row else None
        except Exception as e:
            print("Error fetching user by name:", e)
    @classmethod
    def find_by_id(cls, id):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM users WHERE id =?;
                    """,
                    (id,),
                )
                row = CURSOR.fetchone()
                return cls.instance_from_db(row) if row else None
        except Exception as e:
            print("Error fetching user by id:", e)

    #! ORM instance method

    def save(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        INSERT INTO users (name)
                        VALUES (?);
                    """,
                    (self.name),
                )
                CONN.commit()
                self.id = CURSOR.lastrowid
                type(self).all[self.id] = self
                return self
        except IntegrityError as e:
            print("Name must be provided")
        except Exception as e:
            print("We could not save this user:", e)

    def delete(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        DELETE FROM users WHERE id =?;
                    """,
                    (self.id,),
                )
                CONN.commit()
                del type(self).all[self.id]
                self.id = None
        except Exception as e:
            print("We could not delete this user:", e)