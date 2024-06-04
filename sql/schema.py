import os
import sqlite3

def create_table():
    conn = sqlite3.connect('skyanalytics.db')
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS airplanes
             (ref_aero string [primary key],
              type_model string,
              debut_service date,
              last_maint datetime,
              en_maintenance bool,
              end_maint datetime)"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS composants
             (ref_compo string [primary key],
              categorie string,
              aero string ,
              desc varchar(255),
              lifespan int,
              taux_usure_actuel float,
              cout_composant int)"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS logs_vol
             (ref_vol string [primary key],
              aero_linked string,
              jour_vol date,
              time_en_air tinyint,
              sensor_data varchar(255),
              etat_voyant tinyint)"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS degradation
             (ref_deg string,
              linked_aero string,
              compo_concerned string,
              usure_cumulee float,
              measure_day date,
              need_replacement bool)"""
    )
    

    conn.commit()
    conn.close()

def delete_db():
    db_path = 'skyanalytics.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Database {db_path} deleted.")
    else:
        print(f"Database {db_path} does not exist.")

if __name__ == "__main__":
    #delete_db()
    create_table()

