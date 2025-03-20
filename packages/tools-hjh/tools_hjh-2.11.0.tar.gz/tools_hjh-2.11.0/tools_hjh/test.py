from tools_hjh import OracleTools, Tools
import re


def main():

    @staticmethod
    def get_table_ddl_pg(dba_conn, username, table, forever_number_to_numeric=True, to_lower=True):
        sql_list = []
        metadata = OracleTools.get_table_metadata(dba_conn, username, table)
        if metadata == {}:
            return sql_list
        
        if to_lower:
            create_table_sql = 'create table ' + username + '."' + metadata['name'].lower() + '"'
        else:
            create_table_sql = 'create table ' + username + '."' + metadata['name'] + '"'
        
        create_table_sql = create_table_sql + '\n(\n'
        for col in metadata['columns']:
            if to_lower:
                name = str(col['name']).lower().strip()
            else:
                name = str(col['name']).strip()
            type_ = str(col['type'])
            
            # 列类型
            if 'VARCHAR' in type_:
                type_ = type_.replace('VARCHAR2', 'VARCHAR')
                type_ = type_.replace('NVARCHAR', 'VARCHAR')
                type_ = type_.replace('NVARCHAR2', 'VARCHAR')
            elif 'CHAR' in type_:
                type_ = type_.replace('NCHAR', 'CHAR')
            elif 'NUMBER' in type_:
                if '(' in type_ and ',' in type_:
                    size_1 = int(type_.split('(')[1].split(')')[0].split(',')[0].strip())
                    size_2 = int(type_.split('(')[1].split(')')[0].split(',')[1].strip())
                    if size_2 > size_1:
                        type_ = 'NUMERIC'
                    else:
                        type_ = type_.replace('NUMBER', 'NUMERIC')
                elif not forever_number_to_numeric and '(' in type_ and ',' not in type_:
                    size_ = int(type_.split('(')[1].split(')')[0])
                    if size_ <= 4:
                        type_ = 'SMALLINT'
                    elif size_ > 4 and size_ <= 9: 
                        type_ = 'INT'
                    elif size_ > 9 and size_ <= 18: 
                        type_ = 'BIGINT'
                    else:
                        type_ = type_.replace('NUMBER', 'NUMERIC')
                else:
                    type_ = type_.replace('NUMBER', 'NUMERIC')
            elif 'RAW' in type_:
                if '(' in type_:
                    size_ = int(type_.split('(')[1].split(')')[0])
                    if size_ == 16:
                        # type_ = 'VARCHAR(32)'
                        type_ = 'UUID'
                    else:
                        type_ = 'BYTEA'
                else:
                    type_ = 'BYTEA'
            elif type_.startswith('TIMESTAMP(') and 'WITH LOCAL TIME ZONE' in type_:
                type_ = 'TIMESTAMPTZ'
            elif type_.startswith('INTERVAL DAY('):
                second_ = type_.split(' TO ')[1].strip()
                type_ = 'INTERVAL DAY TO ' + second_
            else:
                type_ = type_.replace('BINARY_INTEGER', 'INTEGER')
                type_ = type_.replace('BINARY_FLOAT', 'FLOAT')
                type_ = type_.replace('DATE', 'TIMESTAMP(0)')
                type_ = type_.replace('NCLOB', 'TEXT')
                type_ = type_.replace('CLOB', 'TEXT')
                type_ = type_.replace('LONG', 'TEXT')
                type_ = type_.replace('BLOB', 'BYTEA')
                type_ = type_.replace('LONG RAW', 'BYTEA')
                
                # 暂定
                type_ = type_.replace('UROWID', 'VARCHAR(18)')
                type_ = type_.replace('ROWID', 'VARCHAR(18)')
                
            # 默认值
            if col['default_value'] != None:
                # to_number
                if 'to_number(' in col['default_value'].lower():
                    to_number_content = Tools.get_fun_content(col['default_value'], 'to_number'.upper())
                    a1 = col['default_value'].split('TO_NUMBER(' + to_number_content + ')')[0]
                    a2 = col['default_value'].split('TO_NUMBER(' + to_number_content + ')')[1]
                    col['default_value'] = a1 + to_number_content + '::numeric' + a2
                
                # ''值不可在非字符类型上
                if col['default_value'].strip() == "''" and ('VARCHAR' not in type_ or type_ != 'TEXT'):
                    col['default_value'] = 'NULL'
                    
                col['default_value'] = re.sub('sys_guid', 'uuid_generate_v4', col['default_value'], flags=re.IGNORECASE)
                col['default_value'] = re.sub('systimestamp', 'current_timestamp', col['default_value'], flags=re.IGNORECASE)
                col['default_value'] = re.sub('sysdate', 'statement_timestamp()', col['default_value'], flags=re.IGNORECASE)
                
                # 时间加减
                if str(col['default_value']).startswith('statement_timestamp()-'):
                    jz = str(col['default_value']).split('-')[1].strip()
                    col['default_value'] = "statement_timestamp() - interval '" + jz + " days'"
                elif str(col['default_value']).startswith('statement_timestamp()+'):
                    jz = str(col['default_value']).split('+')[1].strip()
                    col['default_value'] = "statement_timestamp() + interval '" + jz + " days'"
                    
                # 虚拟列
                if col['virtual'] == 'NO':
                    default_value = 'default ' + str(col['default_value']).strip()
                else:
                    for col2 in metadata['columns']:
                        col2_name = str(col2['name'])
                        if '"' + col2_name.upper() + '"' in str(col['default_value']):
                            if to_lower:
                                col['default_value'] = col['default_value'].replace(col2_name.upper(), col2_name.lower())
                            else:
                                col['default_value'] = col['default_value'].replace(col2_name.upper(), col2_name)
                    default_value = 'generated always as (' + col['default_value'] + ') stored'
            else:
                default_value = ''
    
            # 非空
            if col['nullable']:
                nullable = ''
            else:
                nullable = 'not null'
                
            if col['virtual'] == 'NO':
                create_table_sql = create_table_sql + '[--gt--]"' + name + '"' + ' ' + type_ + ' ' + default_value + ' ' + nullable + ',\n'
            else:
                create_table_sql = create_table_sql + '[--gt--]"' + name + '"' + ' ' + type_ + ' ' + default_value + ',\n'
            
        create_table_sql = Tools.merge_spaces(create_table_sql.rstrip().rstrip(',')).replace(' ,', ',').replace('[--gt--]', '  ')
        create_table_sql = create_table_sql + '\n)'
        
        pk_add_cols_list = []
        
        partition_columns = ''
        partitions = []
        if metadata['partition'] != None:
            partition = metadata['partition']
            partitions = partition['partitions']
            partition_type = partition['partition_type']
            partition_columns = partition['partition_columns']
            for col in partition_columns.split(','):
                if to_lower:
                    col = col.strip().lower()
                else:
                    col = col.strip()
                if col not in pk_add_cols_list:
                    pk_add_cols_list.append(col)
            subpartition_type = partition['subpartition_type']
            subpartition_columns = partition['subpartition_columns']
            
            pcs = ''
            for pc in partition_columns.split(','):
                if to_lower:
                    pc = '"' + pc.lower() + '"'
                else:
                    pc = '"' + pc + '"'
                pcs = pcs + pc + ','
            pcs = pcs[:-1]
            create_table_sql = create_table_sql + ' partition by ' + partition_type + ' (' + pcs + ')'
            
        sql_list.append(create_table_sql)    
        
        # 分区
        q_val = None
        idx = 0
        for part in partitions:
            if to_lower:
                name = (table + '_part' + str(idx)).lower()
            else:
                name = (table + '_PART' + str(idx))
            value = part['value']
            if partition_type == 'RANGE':
                if value.startswith("TIMESTAMP' "):
                    value = value.replace("TIMESTAMP", '')
                if value.startswith("TO_DATE(' "):
                    value = value.split(',')[0].replace('TO_DATE(', '')
                if q_val is None:
                    q_val = 'MINVALUE'
                if to_lower:
                    part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table.lower() + '" for values from (' + q_val + ') to (' + value + ')'
                else:
                    part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table + '" for values from (' + q_val + ') to (' + value + ')'
                q_val = value
            elif partition_type == 'HASH':
                if to_lower:
                    part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table.lower() + '" for values with (modulus ' + str(len(partitions)) + ', remainder ' + str(idx) + ')'
                else:
                    part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table + '" for values with (modulus ' + str(len(partitions)) + ', remainder ' + str(idx) + ')'
            elif partition_type == 'LIST':
                if value.lower() == 'default':
                    if to_lower:
                        part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table.lower() + '" default'
                    else:
                        part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table + '" default'
                else:
                    if to_lower:
                        part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table.lower() + '" for values in (' + value + ')'
                    else:
                        part_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + table + '" for values in (' + value + ')'
            if subpartition_type is not None:
                sub_cols = ''
                for col in subpartition_columns.split(','):
                    if to_lower:
                        sub_cols = sub_cols + '"' + col.strip().lower() + '", '
                        col = col.strip().lower()
                    else:
                        sub_cols = sub_cols + '"' + col.strip() + '", '
                        col = col.strip()
                    if col not in pk_add_cols_list:
                        pk_add_cols_list.append(col)
                part_sql = part_sql + ' partition by ' + subpartition_type + ' (' + sub_cols[:-2] + ')'
            idx = idx + 1
            sql_list.append(part_sql)
            
        # 子分区
        q_val = None
        idx = 0
        for part in partitions:
            sub_idx = 0
            if to_lower:
                par_name = (table + '_part' + str(idx)).lower()
            else:
                par_name = (table + '_PART' + str(idx))
            for subpar in part['subpartitions']:
                if to_lower:
                    name = (par_name + '_subpart' + str(sub_idx)).lower()
                else:
                    name = (par_name + '_SUBPART' + str(sub_idx))
                value = subpar['value']
                if subpartition_type == 'RANGE':
                    if value.startswith("TIMESTAMP' "):
                        value = value.replace("TIMESTAMP", '')
                    if value.startswith("TO_DATE(' "):
                        value = value.split(',')[0].replace('TO_DATE(', '')
                    if q_val is None:
                        q_val = 'MINVALUE'
                    subpar_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + par_name + '" for values from (' + q_val + ') to (' + value + ')'
                    q_val = value
                elif subpartition_type == 'HASH':
                    subpar_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + par_name + '" for values with (modulus ' + str(len(part['subpartitions'])) + ', remainder ' + str(sub_idx) + ')'
                elif subpartition_type == 'LIST':
                    if value.lower() == 'default':
                        subpar_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + par_name + '" default'
                    else:
                        subpar_sql = 'create table ' + username + '."' + name + '" partition of ' + username + '."' + par_name + '" for values in (' + value + ')'
                sub_idx = sub_idx + 1
                sql_list.append(subpar_sql)
            idx = idx + 1
            
        # 注释
        if metadata['comments'] != None:
            comments_str = ''
            if to_lower:
                comments_str = 'comment on table ' + username + '."' + table.lower() + '"' + " is '" + metadata['comments'].replace('\\u', '\\\\u').replace("'", "''") + "'"
            else:
                comments_str = 'comment on table ' + username + '."' + table + '"' + " is '" + metadata['comments'].replace('\\u', '\\\\u').replace("'", "''") + "'"
            sql_list.append(comments_str)
            
        for col in metadata['columns']:
            comments_str = ''
            if to_lower:
                name = col['name'].lower().strip()
            else:
                name = col['name'].strip()
            comments = col['comments']
            if comments != None: 
                if to_lower:
                    comments_str = comments_str + 'comment on column ' + username + '."' + table.lower() + '"."' + name.lower() + '"' + " is '" + comments.replace('\\u', '\\\\u').replace("'", "''") + "'"
                else:
                    comments_str = comments_str + 'comment on column ' + username + '."' + table + '"."' + name + '"' + " is '" + comments.replace('\\u', '\\\\u').replace("'", "''") + "'"
                sql_list.append(comments_str)
                
        # 索引
        for idx in metadata['indexes']:
            index_str = ''
            name = idx['name']
            type_ = idx['type']
            my_cols_ = idx['columns']
            
            my_cols = ''
            for col in my_cols_.split('SC,'):
                is_asc_or_desc = ''
                if col.endswith(' A') or col.endswith(' ASC'):
                    is_asc_or_desc = 'ASC'
                elif col.endswith(' DESC') or col.endswith(' DE'):
                    is_asc_or_desc = 'DESC'
                col = col.replace(' ASC', '').replace(' DESC', '').replace(' A', '').replace(' DE', '').strip()
                
                # 索引字段是数字
                if col.isdigit():
                    col = '(' + col + ') ' + is_asc_or_desc
                # 索引字段是字符串（列写错成字符串）
                if col.startswith("'") and col.endswith("'"):
                    if to_lower:
                        col = '"' + col.strip("'").lower() + '" ' + is_asc_or_desc
                    else:
                        col = '"' + col.strip("'") + '" ' + is_asc_or_desc
                # 索引字段是 case when then
                if 'case' in col.lower() and 'when' in col.lower() and 'then' in col.lower():
                    col = '(' + col + ') ' + is_asc_or_desc
                # 索引字段是||连接
                if '||' in col:
                    col = '(' + col + ') ' + is_asc_or_desc
                # 索引字段是 trunc() 函数
                if 'trunc(' in col:
                    fun_content = Tools.get_fun_content(col, 'trunc')
                    col = col.split('trunc')[0] + "date_trunc('day', " + fun_content + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                if 'TRUNC(' in col:
                    fun_content = Tools.get_fun_content(col, 'TRUNC')
                    col = col.split('TRUNC')[0] + "date_trunc('day', " + fun_content + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                # 索引字段是 to_number() 函数
                if 'to_number(' in col:
                    fun_content = Tools.get_fun_content(col, 'to_number')
                    col = col.split('to_number')[0] + '(' + fun_content + '::numeric ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                if 'TO_NUMBER(' in col:
                    fun_content = Tools.get_fun_content(col, 'TO_NUMBER')
                    col = col.split('TO_NUMBER')[0] + '(' + fun_content + '::numeric ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                # 索引字段是 to_char() 函数，且不是日期格式化
                if 'to_char(' in col and ',' not in col:
                    fun_content = Tools.get_fun_content(col, 'to_char')
                    col = col.split('to_char')[0] + '(' + fun_content + '::varchar ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                if 'TO_CHAR(' in col and ',' not in col:
                    fun_content = Tools.get_fun_content(col, 'TO_CHAR')
                    col = col.split('TO_CHAR')[0] + '(' + fun_content + '::varchar ' + col.split(fun_content)[1] + ' ' + is_asc_or_desc
                # 索引字段是 sys_op_c2c() 函数
                if 'sys_op_c2c(' in col:
                    fun_content = Tools.get_fun_content(col, 'sys_op_c2c')
                    col = col.split('sys_op_c2c')[0] + fun_content + col.split(fun_content + ')')[1] + ' ' + is_asc_or_desc
                if 'SYS_OP_C2C(' in col:
                    fun_content = Tools.get_fun_content(col, 'SYS_OP_C2C')
                    col = col.split('SYS_OP_C2C')[0] + fun_content + col.split(fun_content + ')')[1] + ' ' + is_asc_or_desc
                
                my_cols = my_cols + col + ', '
            my_cols = my_cols[:-2]
            
            if type_ == 'UNIQUE' and metadata['partition'] != None:
                cols_partition_columns = ''
                my_cols_list = []
                for col in my_cols.split(','):
                    if not (col.lower().startswith('(case ') and 'when' in col.lower() and 'then' in col.lower()):
                        if to_lower:
                            col = col.strip().lower()
                        else:
                            col = col.strip()
                        if ' ' in col:
                            col = col.split(' ')[0]
                        if col not in my_cols_list:
                            my_cols_list.append(col)
                    else:
                        if to_lower:
                            col = col.strip().lower()
                        else:
                            col = col.strip()
                        if ') ' in col:
                            col = col.split(') ')[0] + ')'
                        if col not in my_cols_list:
                            my_cols_list.append(col)
                pk_cols_list = my_cols_list.copy()
                for col in pk_add_cols_list:
                    if col not in pk_cols_list:
                        pk_cols_list.append(col)
                for col in pk_cols_list:
                    cols_partition_columns = cols_partition_columns + col + ', '
                cols_partition_columns = cols_partition_columns[:-2]
                
            if type_ == 'NORMAL':
                type_ = ''
                
            if type_ == 'UNIQUE' and metadata['partition'] != None:
                cols = cols_partition_columns
            else:
                cols = my_cols.replace(',', ', ')
                
            if not to_lower:
                cols2 = ''
                for c in cols.split(','):
                    if ' ' in c and 'sc' in c.lower():
                        cl = c.split(' ')
                        cols2 = cols2 + '"' + cl[0].strip() + '" ' + cl[1] + ', '
                    else:
                        cols2 = cols2 + '"' + c.strip() + '", '
                cols = cols2[:-2]
            
            if to_lower:
                index_str = index_str + 'create ' + type_ + ' index "' + name.lower() + '" on ' + username + '."' + table.lower() + '" (' + cols.lower() + ') '
            else:
                index_str = index_str + 'create ' + type_ + ' index "' + name + '" on ' + username + '."' + table + '" (' + cols + ') '
                
            index_str = Tools.merge_spaces(index_str)
            index_str = index_str.replace(' asc', '')
            sql_list.append(index_str)
    
        # 约束（主键、唯一、外键）
        for constraint in metadata['constraints']:
            k_str = ''
            name = constraint['name']
            my_cols_ = constraint['columns']
            
            my_cols = ''
            for col in my_cols_.split(','):
                if col.replace(' ASC', '').replace(' DESC', '').strip().isdigit() and len(col.split(' ')) == 2:
                    col = '(' + col.split(' ')[0] + ') ' + col.split(' ')[1]
                elif 'case' in col.lower() and 'when' in col.lower() and 'then' in col.lower() and 'else' in col.lower():
                    col = '(' + col + ') '
                my_cols = my_cols + col + ', '
            my_cols = my_cols[:-2]
            
            type_ = constraint['type']
            r_table = constraint['r_table']
            r_cols = constraint['r_cols']
            
            if type_ == 'primary_key' or type_ == 'unique':
                cols_partition_columns = ''
                my_cols_list = []
                for col in my_cols.split(','):
                    if to_lower:
                        col = col.strip().lower()
                    else:
                        col = col.strip()
                    if ' ' in col:
                        col = col.split(' ')[0]
                    if col not in my_cols_list:
                        my_cols_list.append(col)
                pk_cols_list = my_cols_list.copy()
                for col in pk_add_cols_list:
                    if col not in pk_cols_list:
                        pk_cols_list.append(col)
                for col in pk_cols_list:
                    cols_partition_columns = cols_partition_columns + col + ', '
                cols_partition_columns = cols_partition_columns[:-2]
                
            if not to_lower and my_cols is not None:
                my_cols2 = ''
                for c in my_cols.split(','):
                    my_cols2 = my_cols2 + '"' + c.strip() + '", '
                my_cols2 = my_cols2[:-2]
                my_cols = my_cols2
            if not to_lower and cols_partition_columns is not None: 
                cols_partition_columns2 = ''
                for c in cols_partition_columns.split(','):
                    cols_partition_columns2 = cols_partition_columns2 + '"' + c.strip() + '", '
                cols_partition_columns2 = cols_partition_columns2[:-2]
                cols_partition_columns = cols_partition_columns2
            if not to_lower and r_cols is not None: 
                r_cols2 = ''
                for c in r_cols.split(','):
                    r_cols2 = r_cols2 + '"' + c.strip() + '", '
                r_cols2 = r_cols2[:-2]
                r_cols = r_cols2
                
            if type_ == 'primary_key' and metadata['partition'] != None:
                if to_lower:
                    k_str = k_str + 'alter table ' + username + '."' + table.lower() + '" add constraint "' + name.lower() + '" primary key (' + cols_partition_columns.lower() + ')'
                else:
                    k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint "' + name + '" primary key (' + cols_partition_columns + ')'
            if type_ == 'primary_key' and metadata['partition'] == None:
                if to_lower:
                    k_str = k_str + 'alter table ' + username + '."' + table.lower() + '" add constraint "' + name.lower() + '" primary key (' + my_cols.lower() + ')'
                else:
                    k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint "' + name + '" primary key (' + my_cols + ')'
            elif type_ == 'unique' and metadata['partition'] != None:
                if to_lower:
                    k_str = k_str + 'alter table ' + username + '."' + table.lower() + '" add constraint "' + name.lower() + '" unique (' + cols_partition_columns.lower() + ')'
                else:
                    k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint "' + name + '" unique (' + cols_partition_columns + ')'
            elif type_ == 'unique' and metadata['partition'] == None:
                if to_lower:
                    k_str = k_str + 'alter table ' + username + '."' + table.lower() + '" add constraint "' + name.lower() + '" unique (' + my_cols.lower() + ')'
                else:
                    k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint "' + name + '" unique (' + my_cols + ')'
            elif type_ == 'foreign_key':
                if to_lower:
                    k_str = k_str + 'alter table ' + username + '."' + table.lower() + '" add constraint "' + name.lower() + '" foreign key (' + my_cols.lower() + ') references ' + r_table.lower() + ' (' + r_cols.lower() + ')'
                else:
                    r_table = r_table.split('.')[0] + '."' + r_table.split('.')[1] + '"'
                    k_str = k_str + 'alter table ' + username + '."' + table + '" add constraint "' + name + '" foreign key (' + my_cols + ') references ' + r_table + ' (' + r_cols + ')'
                delete_rule = constraint['delete_rule']
                if delete_rule == 'CASCADE':
                    k_str = k_str + ' on delete cascade'
                elif delete_rule == 'SET NULL':
                    k_str = k_str + ' on delete set null'
            sql_list.append(k_str)
        return sql_list
    
