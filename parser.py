import sqlite3
from sqlite3 import Cursor
import re
import os
from os import walk
import ntpath

class Parser:

    def __init__(self):
        self.init_database()
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    def __parse_dir(self, path):
        assert os.path.isdir(path), f'{path} is not a directory'
        print(f'parsing directory {path}', end="\r")
        for (dirpath, _, filenames) in os.walk(path):
            for filename in filenames:
                if(filename.endswith('.java')) : self.parse(dirpath+'/'+filename)
                
    
    def parse(self, file_path):
        
        #redirect if directory
        if(os.path.isdir(file_path)):
            self.__parse_dir(file_path)
            self.conn.commit()
            return

        #extract the filename
        head, tail = ntpath.split(file_path)
        filename = tail or ntpath.basename(head)

        print(f'parsing file {filename}', end="\r")
        with  open(file_path, 'r') as file:
            line = file.readline()
            while line: 
                self.save_line(line.rstrip().strip(';'), filename.split('.')[0], filename)
                line = file.readline()
        self.conn.commit()


    def save_line(self, line : str, jclass : str, path : str):
        if line.startswith('package'):
            try:    
                package_id = self.save_package_line(line)
                self.save_class(jclass, package_id)
            except Exception as e:
                print(f'Error parsing package or class {e}')

        elif line.startswith('import'):
            try:    
                self.save_link_line(line, jclass)
            except Exception as e:
                print(f'Error parsing link {e}')

    def save_package_line(self, line : str) -> int:
        items = line.split(' ')
        if(len(items) == 2):
            return self.save_package(items[1])
        return -1

    def save_package(self, package_name : str) -> int:
        print(f'saving package : {package_name}', end="\r"),
        success = self.__execute_sql(self.cursor, f'''
            INSERT INTO package (id, package_name, absolute_path)
            VALUES(null, "{package_name}", "")
        ''')

        if not(success) :
            self.__query(self.cursor, f'''
                SELECT id FROM package WHERE package_name = "{package_name}"
            ''')
            return self.cursor.fetchone()[0]

        return self.cursor.lastrowid

    def save_link_line(self, line : str, src_class) -> int:
        result = re.search('import (.*)\.([^.]+$)', line)
        return self.save_link(result.group(2), result.group(1), src_class)

    def save_link(self, dst_class, dst_package, src_class) -> int:
        print(f'saving link : {dst_class} {dst_package} {src_class}', end="\r")
        dst_class_id = self.save_class_package(dst_class, dst_package)
        self.__query(self.cursor, f'''
            SELECT id FROM class WHERE class_name="{src_class}"
        ''')
        src_class_id = self.cursor.fetchone()[0]
        success = self.__execute_sql(self.cursor, f'''
            INSERT INTO link (id, class_src, class_dst)
            VALUES (null, "{src_class_id}", "{dst_class_id}")
        ''')

        return -1 if not success else  self.cursor.lastrowid

    def save_class_package(self, jclass, package_name : str) -> int:
        package_id = self.save_package(package_name)
        return self.save_class(jclass, package_id)
    
    def save_class(self, jclass, package_id : int) -> int:
        print(f'saving  class : {jclass} {package_id}', end="\r")
        success = self.__execute_sql(self.cursor, f'''
            INSERT INTO class(id, class_name, absolute_path, package_id)
            VALUES(null, "{jclass}", "", "{package_id}")
        ''')
        if not(success) :
            self.__query(self.cursor, f'''
                SELECT id FROM class WHERE class_name = "{jclass}"
            ''')
            return self.cursor.fetchone()[0]
        
        return self.cursor.lastrowid

    def init_database(self):

        print('creating database...')
        self.conn = sqlite3.connect('test.db')
        c = self.conn.cursor()

        # Open and read the file as a single buffer
        fd = open('database.sql', 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        # Execute every command from the input file
        for command in sqlCommands:
            self.__execute_sql(c, command)
        c.close()
       
    def __execute_sql(self, cursor, query) -> bool:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(query)
            return True
        except Exception as e:
            #print(f'Command skipped:  {e} {query}'),
            return False

    def __query(self, cursor, query):
        try:
            return cursor.execute(query)
        except Exception as e:
            #print(f'Command skipped:  {e} {query}'),
            return None