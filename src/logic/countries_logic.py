import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))






from src.utils.dal import DAL


class CountryLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_countries(self):
        '''returns: list of country dictionaries'''
        '''empty list if no countries in the database'''

        query = "SELECT * from mydb.countries"
        result = self.dal.get_table(query)
        return result if result is not None else []
    

    def check_if_country_exists(self, country_name):
        
        query = f"SELECT * from mydb.countries where country_name like '{country_name}'"
        result = self.dal.get_table(query)
        return True if result is not None else False



    def add_country(self, country_name):
        try:
            query = """
            INSERT INTO mydb.countries 
            (country_name)
            VALUES 
            (%s)
            """
            params = (country_name,)
            self.dal.insert(query, params)
            return True

        except Exception as err:
            print(f"Error adding country: {err}")
            return False

    def edit_country(self, id, **kwargs):
        if not kwargs:
            return False

        clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])

        params = tuple(kwargs.values()) + (id,)
        query = f"UPDATE mydb.countries SET {clause} WHERE id = %s"

        try:
            self.dal.update(query, params)
            return True
        except Exception as e:
            print(f"Error updating country: {e}")
            return False

    def del_country(self, id):
        query = "DELETE FROM mydb.countries WHERE id = %s"
        params = (id,)
        try:
            result = self.dal.delete(query, params)
            return True
        except Exception as err:
            print(f"Error deleting country: {err}")
            return False


if __name__ == "__main__":
    try:
        with CountryLogic() as country_logic:

            # country_logic.add_country("Bangladesh")
            # country_logic.edit_country(15, country_name="South Korea")
            countries = country_logic.get_all_countries()
            for country in countries:
                print("----------------------")
                print(country)
    except Exception as err:
        print(f"Error: {err}")
        
        # aa aa
