import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('db.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 读取.env配置文件
def load_env_config():
    # 从src/database目录向上查找.env文件
    current_dir = os.path.dirname(os.path.abspath(__file__))  # database目录
    project_dir = os.path.dirname(current_dir)  # src目录
    root_dir = os.path.dirname(project_dir)  # main目录
    
    env_file = os.path.join(root_dir, '.env')
    logger.info(f"查找.env文件: {env_file}")
    
    if os.path.exists(env_file):
        logger.info("找到.env文件，正在读取...")
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
                    logger.debug(f"读取配置: {key.strip()} = {value.strip()}")
    else:
        logger.warning(f"未找到.env文件: {env_file}")

load_env_config()

try:
    import mysql.connector
    from mysql.connector import pooling
    from mysql.connector.errors import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    logger.warning("MySQL connector not available")

class DBManager:
    _instance = None
    _pool = None
    _connected = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        if not MYSQL_AVAILABLE:
            logger.warning("MySQL connector not installed")
            return
            
        try:
            # 从环境变量读取数据库配置
            db_password = os.environ.get('DB_PASSWORD', '')
            
            self._pool = pooling.MySQLConnectionPool(
                pool_name='math_exercise_pool',
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                user='root',
                password=db_password,
                database='math_exercise',
                charset='utf8mb4',
                autocommit=True
            )
            self._connected = True
            logger.info("数据库连接池初始化成功")
        except Error as e:
            self._connected = False
            logger.warning(f"数据库连接池初始化失败: {e}")

    def is_connected(self):
        return self._connected

    def get_connection(self):
        if not self._connected or not MYSQL_AVAILABLE:
            raise Exception("数据库未连接")
            
        try:
            conn = self._pool.get_connection()
            if conn.is_connected():
                logger.debug("成功获取数据库连接")
                return conn
        except Error as e:
            logger.error(f"获取数据库连接失败: {e}")
            raise

    def close_connection(self, conn):
        if not MYSQL_AVAILABLE:
            return
        try:
            if conn.is_connected():
                conn.close()
                logger.debug("数据库连接已释放")
        except Error as e:
            logger.error(f"关闭数据库连接失败: {e}")

    def execute_query(self, sql, params=None):
        if not self._connected:
            logger.warning("数据库未连接，返回空结果")
            return []
            
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            result = cursor.fetchall()
            logger.debug(f"执行查询成功: {sql[:50]}...")
            return result
        except Error as e:
            logger.error(f"执行查询失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.close_connection(conn)

    def execute_update(self, sql, params=None):
        if not self._connected:
            logger.warning("数据库未连接，跳过更新")
            return 0
            
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            affected = cursor.rowcount
            logger.debug(f"执行更新成功，影响行数: {affected}")
            return affected
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"执行更新失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.close_connection(conn)

    def execute_insert(self, sql, params=None):
        if not self._connected:
            logger.warning("数据库未连接，跳过插入")
            return 0
            
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            last_id = cursor.lastrowid
            logger.debug(f"执行插入成功，插入ID: {last_id}")
            return last_id
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"执行插入失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.close_connection(conn)

    def create_tables(self):
        if not self._connected:
            logger.warning("数据库未连接，跳过表创建")
            return False
            
        tables = [
            """
            CREATE TABLE IF NOT EXISTS exercise_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                file_type ENUM('addition', 'subtraction', 'mixed') NOT NULL,
                question_count INT NOT NULL,
                file_suffix VARCHAR(50),
                content TEXT,
                file_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS answer_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                exercise_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL UNIQUE,
                content TEXT,
                file_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exercise_id) REFERENCES exercise_files(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS practice_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                exercise_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL UNIQUE,
                content TEXT,
                file_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exercise_id) REFERENCES exercise_files(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS checking_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                practice_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL UNIQUE,
                total_count INT NOT NULL,
                correct_count INT NOT NULL,
                wrong_count INT NOT NULL,
                score INT NOT NULL,
                content TEXT,
                file_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (practice_id) REFERENCES practice_results(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS equations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                exercise_id INT NOT NULL,
                equation_text VARCHAR(100) NOT NULL,
                answer INT NOT NULL,
                index_num INT NOT NULL,
                FOREIGN KEY (exercise_id) REFERENCES exercise_files(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            """
            CREATE TABLE IF NOT EXISTS practice_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                exercise_type ENUM('addition', 'subtraction', 'mixed') NOT NULL,
                total_count INT NOT NULL,
                correct_count INT NOT NULL,
                duration INT NOT NULL,
                answers TEXT,
                file_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        ]

        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            for table_sql in tables:
                cursor.execute(table_sql)
            conn.commit()
            logger.info("所有数据表创建成功")
            return True
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"创建数据表失败: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.close_connection(conn)

    def insert_exercise_file(self, filename, file_type, question_count, file_suffix, content, file_path=None):
        if not self._connected:
            logger.warning("数据库未连接，跳过插入")
            return 0
            
        sql = """
        INSERT INTO exercise_files (filename, file_type, question_count, file_suffix, content, file_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content = %s, file_path = %s, updated_at = CURRENT_TIMESTAMP
        """
        params = (filename, file_type, question_count, file_suffix, content, file_path, content, file_path)
        return self.execute_insert(sql, params)

    def insert_answer_file(self, exercise_id, filename, content, file_path=None):
        if not self._connected:
            logger.warning("数据库未连接，跳过插入")
            return 0
            
        sql = """
        INSERT INTO answer_files (exercise_id, filename, content, file_path)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content = %s, file_path = %s
        """
        params = (exercise_id, filename, content, file_path, content, file_path)
        return self.execute_insert(sql, params)

    def insert_practice_result(self, exercise_id, filename, content, file_path=None):
        if not self._connected:
            logger.warning("数据库未连接，跳过插入")
            return 0
            
        sql = """
        INSERT INTO practice_results (exercise_id, filename, content, file_path)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content = %s, file_path = %s
        """
        params = (exercise_id, filename, content, file_path, content, file_path)
        return self.execute_insert(sql, params)

    def insert_checking_result(self, practice_id, filename, total_count, correct_count, wrong_count, score, content, file_path=None):
        if not self._connected:
            logger.warning("数据库未连接，跳过插入")
            return 0
            
        sql = """
        INSERT INTO checking_results (practice_id, filename, total_count, correct_count, wrong_count, score, content, file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE content = %s, file_path = %s, updated_at = CURRENT_TIMESTAMP
        """
        params = (practice_id, filename, total_count, correct_count, wrong_count, score, content, file_path, content, file_path)
        return self.execute_insert(sql, params)

    def get_exercise_by_filename(self, filename):
        if not self._connected:
            return None
            
        sql = "SELECT * FROM exercise_files WHERE filename = %s"
        result = self.execute_query(sql, (filename,))
        return result[0] if result else None

    def get_all_exercises(self):
        if not self._connected:
            return []
            
        sql = "SELECT * FROM exercise_files ORDER BY created_at DESC"
        return self.execute_query(sql)

    def get_exercises_by_type(self, file_type):
        if not self._connected:
            return []
            
        sql = "SELECT * FROM exercise_files WHERE file_type = %s ORDER BY created_at DESC"
        return self.execute_query(sql, (file_type,))

    def delete_exercise(self, exercise_id):
        if not self._connected:
            return 0
            
        sql = "DELETE FROM exercise_files WHERE id = %s"
        return self.execute_update(sql, (exercise_id,))

    def get_practice_results_by_exercise(self, exercise_id):
        if not self._connected:
            return []
            
        sql = "SELECT * FROM practice_results WHERE exercise_id = %s ORDER BY created_at DESC"
        return self.execute_query(sql, (exercise_id,))

    def get_checking_results_by_practice(self, practice_id):
        if not self._connected:
            return []
            
        sql = "SELECT * FROM checking_results WHERE practice_id = %s ORDER BY created_at DESC"
        return self.execute_query(sql, (practice_id,))

    def get_answer_by_exercise(self, exercise_id):
        if not self._connected:
            return None
            
        sql = "SELECT * FROM answer_files WHERE exercise_id = %s"
        result = self.execute_query(sql, (exercise_id,))
        return result[0] if result else None

    def get_file_path_by_filename(self, filename, file_type='exercise'):
        """根据文件名获取文件路径"""
        if not self._connected:
            return None
            
        if file_type == 'exercise':
            sql = "SELECT file_path FROM exercise_files WHERE filename = %s"
        elif file_type == 'answer':
            sql = "SELECT file_path FROM answer_files WHERE filename = %s"
        elif file_type == 'practice':
            sql = "SELECT file_path FROM practice_results WHERE filename = %s"
        elif file_type == 'checking':
            sql = "SELECT file_path FROM checking_results WHERE filename = %s"
        else:
            logger.warning(f"不支持的文件类型: {file_type}")
            return None
            
        result = self.execute_query(sql, (filename,))
        return result[0]['file_path'] if result else None

    def load_file_content_by_path(self, file_path):
        """根据文件路径读取文件内容"""
        if not file_path or not os.path.exists(file_path):
            logger.warning(f"文件路径不存在或为空: {file_path}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"成功读取文件内容: {file_path}")
            return content
        except Exception as e:
            logger.error(f"读取文件内容失败: {e}")
            return None

    def get_file_content_by_filename(self, filename, file_type='exercise'):
        """根据文件名从数据库获取文件路径，然后读取文件内容"""
        file_path = self.get_file_path_by_filename(filename, file_type)
        if file_path:
            return self.load_file_content_by_path(file_path)
        return None

    def update_file_path(self, filename, file_path, file_type='exercise'):
        """更新文件的路径"""
        if not self._connected:
            logger.warning("数据库未连接，跳过更新")
            return 0
            
        if file_type == 'exercise':
            sql = "UPDATE exercise_files SET file_path = %s, updated_at = CURRENT_TIMESTAMP WHERE filename = %s"
        elif file_type == 'answer':
            sql = "UPDATE answer_files SET file_path = %s WHERE filename = %s"
        elif file_type == 'practice':
            sql = "UPDATE practice_results SET file_path = %s WHERE filename = %s"
        elif file_type == 'checking':
            sql = "UPDATE checking_results SET file_path = %s WHERE filename = %s"
        else:
            logger.warning(f"不支持的文件类型: {file_type}")
            return 0
            
        return self.execute_update(sql, (file_path, filename))

    def get_exercises_by_type(self, file_type):
        """根据类型获取练习文件列表"""
        if not self._connected:
            return []
            
        sql = "SELECT id, filename, file_type, question_count, content, file_path, created_at FROM exercise_files WHERE file_type = %s ORDER BY created_at DESC"
        return self.execute_query(sql, (file_type,))

    def get_exercise_by_filename(self, filename):
        """根据文件名获取练习文件详情"""
        if not self._connected:
            return None
            
        sql = "SELECT id, filename, file_type, question_count, content, file_path, created_at FROM exercise_files WHERE filename = %s"
        result = self.execute_query(sql, (filename,))
        return result[0] if result else None

    def get_all_file_paths(self, file_type='exercise'):
        """获取指定类型所有文件的路径信息"""
        if not self._connected:
            return []
            
        if file_type == 'exercise':
            sql = "SELECT id, filename, file_path, file_type FROM exercise_files WHERE file_path IS NOT NULL"
        elif file_type == 'answer':
            sql = "SELECT id, filename, file_path FROM answer_files WHERE file_path IS NOT NULL"
        elif file_type == 'practice':
            sql = "SELECT id, filename, file_path FROM practice_results WHERE file_path IS NOT NULL"
        elif file_type == 'checking':
            sql = "SELECT id, filename, file_path FROM checking_results WHERE file_path IS NOT NULL"
        else:
            logger.warning(f"不支持的文件类型: {file_type}")
            return []
            
        return self.execute_query(sql)

    def insert_practice_record(self, exercise_type, total_count, correct_count, duration, answers, file_name=None):
        """插入练习记录"""
        if not self._connected:
            logger.warning("数据库未连接，跳过插入")
            return 0
            
        sql = """
        INSERT INTO practice_records (exercise_type, total_count, correct_count, duration, answers, file_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (exercise_type, total_count, correct_count, duration, answers, file_name)
        return self.execute_insert(sql, params)

db_manager = DBManager()

if __name__ == "__main__":
    db = DBManager()
    if db.is_connected():
        db.create_tables()
        print("数据库初始化成功")
        exercises = db.get_all_exercises()
        print(f"现有习题文件数量: {len(exercises)}")
    else:
        print("数据库未连接，请检查MySQL配置")