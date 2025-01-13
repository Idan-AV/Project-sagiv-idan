import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))






from src.utils.dal import DAL


class UserLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_users(self):
        '''returns: list of user dictionaries'''
        '''empty list if no users in the database'''

        query = "SELECT * from mydb.users"
        result = self.dal.get_table(query)
        return result if result is not None else []
    
    def get_all_users_by_role(self, role):
        '''returns: list of user dictionaries'''
        '''empty list if no users in the database'''

        query = f"SELECT * from mydb.users where role_id = {role}"
        result = self.dal.get_table(query)
        return result if result is not None else []

    def add_user(self, first_name, last_name, email, password, date_of_birth, role_id):
        try:
            query = """
            INSERT INTO mydb.users 
            (first_name, last_name, email, password, date_of_birth, role_id)
            VALUES 
            (%s, %s, %s, %s, %s, %s)
            """
            params = (first_name, last_name, email,
                      password, date_of_birth, role_id)
            self.dal.insert(query, params)
            return True

        except Exception as err:
            print(f"Error adding user: {err}")
            return False

    def edit_user(self, id, **kwargs):
        if not kwargs:
            return False

        clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])

        params = tuple(kwargs.values()) + (id,)
        query = f"UPDATE mydb.users SET {clause} WHERE id = %s"

        try:
            self.dal.update(query, params)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def del_user(self, id):
        query = "DELETE FROM mydb.users WHERE id = %s"
        params = (id,)
        try:
            result = self.dal.delete(query, params)
            return True
        except Exception as err:
            print(f"Error deleting user: {err}")
            return False


if __name__ == "__main__":
    try:
        with UserLogic() as user_logic:
            # user_logic.add_user("Tzahi", "Aviram", "tzahi.av@singa.ort.il", "Gogo123", "2000-01-20", 2)
            # user_logic.edit_user(10, password="MoMo321")
            # user_logic.del_user(9)
            # users = user_logic.get_all_users_by_role(1)
            users = user_logic.get_all_users()
            for user in users:
                print("----------------------")
                print(user)
    except Exception as err:
        print(f"Error: {err}")
