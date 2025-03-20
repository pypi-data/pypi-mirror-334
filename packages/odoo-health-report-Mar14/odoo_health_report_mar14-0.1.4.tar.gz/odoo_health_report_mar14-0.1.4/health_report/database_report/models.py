# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import timedelta
import os
from pprint import pprint
import psutil
from django.db import connections,models
import math
from django.utils.timezone import now
import pytz
import xmlrpc.client


DB_SETTING_NAME = 'postgresql'
ODOO_DATA_DIR = "/var/lib/odoo/filestore/"
# ODOO_FILESTORE_DIR = "/var/lib/odoo/filestore/" 


class DatabaseMetrics(models.Model):
    """Class representing the database metrics"""
    _name = 'database.metrics'
    _description = 'Database Metrics'

    def collect_database_metrics(self):
        """Collect database performance metrics"""
        with connections[DB_SETTING_NAME].cursor() as cur:
            # Active database name
            cur.execute("SELECT current_database();")
            active_db = cur.fetchone()[0]
            # Total connections
            cur.execute("SELECT count(*) FROM pg_stat_activity;")
            total_connections = cur.fetchone()[0]
            # Database size in MB
            cur.execute("""
            SELECT
                pg_size_pretty(pg_database_size(current_database()));
              """)
            db_size_mb = cur.fetchone()[0]
            # Cache hit ratio
            cur.execute("""
                SELECT ROUND(100 * SUM(blks_hit) / NULLIF(SUM(blks_hit) + SUM(blks_read), 0), 2)
                FROM pg_stat_database
                WHERE datname = current_database();
            """)
            cache_hit_ratio = round(cur.fetchone()[0], 2)
            # Deadlocks
            cur.execute("SELECT deadlocks FROM pg_stat_database WHERE datname = current_database();")
            deadlocks = cur.fetchone()[0]
             # Connection utilization
            cur.execute("SHOW max_connections;")
            max_connections = int(cur.fetchone()[0])
            cur.execute("SELECT state, COUNT(*) FROM pg_stat_activity GROUP BY state;")
            state_counts = dict(cur.fetchall())
            total_current = sum(state_counts.values())
            connection_utilization = (total_current / max_connections) * 100

            # cur.execute("""
            #     SELECT 
            #         COUNT(*)::FLOAT / NULLIF((SELECT setting::FLOAT FROM pg_settings WHERE name = 'max_connections'), 0) 
            #         AS connection_utilization
            #     FROM pg_stat_activity;
            # """)
            # connection_utilization = round(cur.fetchone()[0] * 100, 2)
            
            # Number of schemas
            cur.execute("SELECT COUNT(*) FROM information_schema.schemata;")
            no_of_schema = cur.fetchone()[0]
            # User schema count
            cur.execute("""SELECT COUNT(*) FROM pg_namespace
                        WHERE nspname NOT LIKE 'pg_%'
                        AND nspname != 'information_schema';""")
            user_schema_count = cur.fetchone()[0]
            # System schema count
            cur.execute("""SELECT COUNT(*) FROM pg_namespace
                        WHERE nspname LIKE 'pg_%' OR
                        nspname = 'information_schema';""")
            system_schema_count = cur.fetchone()[0]
            # Number of user-created tables
            cur.execute(""" SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                            WHERE c.relkind = 'r' AND n.nspname NOT LIKE 'pg_%'
                            AND n.nspname != 'information_schema';""")
            user_created_tables = cur.fetchone()[0]
            # Number of system tables
            cur.execute("""SELECT COUNT(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                            WHERE c.relkind = 'r' AND (n.nspname
                            LIKE 'pg_%' OR n.nspname = 'information_schema');""")
            system_tables = cur.fetchone()[0]
            # Number of views
            cur.execute("""SELECT COUNT(*) FROM pg_class WHERE relkind = 'v';""")
            num_of_views = cur.fetchone()[0]
            # Number of materialized views
            cur.execute("""SELECT COUNT(*) FROM pg_class WHERE relkind = 'm';""")
            materialized_views = cur.fetchone()[0]
            # Total rows in all tables
            cur.execute("""SELECT SUM(reltuples::bigint) FROM pg_class WHERE relkind = 'r';""")
            total_row = cur.fetchone()[0]
            # Largest table
            cur.execute("""SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) AS size FROM pg_class
                            ORDER BY pg_total_relation_size(oid) DESC LIMIT 1;""")
            largest_table = cur.fetchone()[0]
        process = psutil.Process()
        cpu_usage_percent = process.cpu_percent()

        return {
            'db_name': active_db,
            'total_connections': total_connections,
            'db_size_mb': db_size_mb,
            'cache_hit_ratio': cache_hit_ratio,
            'deadlocks': deadlocks,
            'connection_utilization': connection_utilization,
            'cpu_usage_percent': cpu_usage_percent,
            'no_of_schema': no_of_schema,
            'user_schema_count': user_schema_count,
            'system_schema_count': system_schema_count,
            'user_created_tables': user_created_tables,
            'system_tables': system_tables,
            'num_of_views': num_of_views,
            'materialized_views': materialized_views,
            'total_row': total_row,
            'largest_table': largest_table
        }

    def odoo_file_health(self):
        """Fetch Odoo's file health from PostgreSQL"""
        tz = pytz.utc  # Ensure timezone consistency
        current_time = now().astimezone(tz)
        
        with connections[DB_SETTING_NAME].cursor() as cursor:
            # Fetch all attachments (id, created_date, store_fname, mimetype, file_size)
            cursor.execute("""
                SELECT id, create_date, store_fname, mimetype, file_size 
                FROM ir_attachment;
            """)
            # attachments = cursor.fetchall()
            url = 'http://cybrosys:8018'  # Odoo instance URL
            database = 'server_report'  # Database name
            user = 'a'  # Username
            password = '82a6dd0b06d2bd066c424bb3bba2dcb107e55982'  # Password

            # Authenticate using the common endpoint
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(database, user, password, {})

            if uid:
                
                # Now connect to the object endpoint
                model = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

                # Fetch all attachments
                attachments = model.execute_kw(database, uid, password, 'ir.attachment', 'search', [[]])
                print("Attachments IDs:", attachments)
                print("Attachments IDs length:", len(attachments))

            else:
                print("Authentication failed! Check credentials.")

            # Count uploaded files in the last 30 days
            cursor.execute("""
                SELECT COUNT(*) FROM ir_attachment 
                WHERE create_date >= NOW() - INTERVAL '30 days';
            """)
            uploaded_files = cursor.fetchone()[0]

            # Fetch file sizes for database and filesystem storage
            total_size = 0
            size_distribution = defaultdict(int)
            file_types = defaultdict(int)
            files_last_30_days = []
            
            for attachment in attachments:
                # pprint(attachment)
                attach_id, create_date, store_fname, mimetype, file_size = attachment
                file_size = file_size if file_size else 0
                create_date = create_date.replace(tzinfo=pytz.utc)  # Ensure create_date is timezone-aware
                if create_date >= current_time - timedelta(days=30):
                    files_last_30_days.append(file_size or 0)
                
                if store_fname:
                    file_path = os.path.join(ODOO_DATA_DIR, store_fname)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                else:
                    total_size += file_size or 0
                    
                # Categorize by size
                if file_size < 10 * 1024:
                    size_distribution['Small (<10KB)'] += 1
                elif file_size < 100 * 1024:
                    size_distribution['Medium (10KB-100KB)'] += 1
                elif file_size < 500 * 1024:
                    size_distribution['Large (100KB-500KB)'] += 1
                else:
                    size_distribution['Very Large (>500KB)'] += 1
                
                # Categorize by file type
                if mimetype:
                    file_types[mimetype.strip().lower()] += 1
            
            total_size_mb = total_size / (1024 * 1024)
            
            # Compute average file size in the last 30 days
            if files_last_30_days:
                avg_size_bytes = sum(files_last_30_days) / len(files_last_30_days)
                avg_size_tb = avg_size_bytes / (1024 ** 4)
                exponent = math.floor(math.log10(avg_size_tb)) if avg_size_tb > 0 else 0
                coefficient = avg_size_tb / (10 ** exponent)
                average_size = f"{coefficient:.3f} × 10^{exponent} TB"
            else:
                average_size = "0 TB"

            # Count missing files (no store_fname)
            cursor.execute("""
                SELECT COUNT(*) FROM ir_attachment 
                WHERE store_fname IS NULL 
                AND write_date >= NOW() - INTERVAL '30 days';
            """)
            missing_files = cursor.fetchone()[0]
        
        # System health checks
        free_disk_space_mb = psutil.disk_usage('/').free / (1024 * 1024)
        available_memory_mb = psutil.virtual_memory().available / (1024 * 1024)
        cpu_usage = psutil.cpu_percent(interval=1)

        disk_limit_mb = free_disk_space_mb * 0.1
        memory_limit_mb = available_memory_mb * 0.2
        cpu_limit_mb = 5 if cpu_usage > 80 else 100
        safe_upload_limit = min(disk_limit_mb, memory_limit_mb, cpu_limit_mb)

        return {
            'uploaded_files': uploaded_files,
            'average_size': average_size,
            'missing_files': missing_files,
            'file_types': file_types,
            'file_distribution': size_distribution,
            'safe_upload_limit': safe_upload_limit,
            'total_size_mb': round(total_size_mb, 2)
        }
        
    def get_concurrent_session_count(self):
        """Fetch Concurrent sesssions"""

        self.env.cr.execute(""" SELECT COUNT(*) FROM pg_stat_activity WHERE datname = %s AND state = 'active'; """,
                            (self.env.cr.dbname,))

        active_sessions = self.env.cr.fetchall()
        # active_sessions_count = int(active_sessions[0][0]) if active_sessions else 0  # Convert to int

        self.env.cr.execute("""
                            SELECT setting
                            FROM pg_settings
                            WHERE name = 'max_connections';
                        """)
        max_connections = self.env.cr.fetchone()
        max_connections_value = int(max_connections[0]) if max_connections else 0  # Convert to int

        return {
            'active_sessions': len(active_sessions),
            'max_connections': max_connections_value
        }