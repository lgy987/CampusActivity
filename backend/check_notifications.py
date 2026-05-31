# check_notifications.py
import sqlite3

# 连接数据库
conn = sqlite3.connect('instance/campus_activity.db')
cursor = conn.cursor()

# 查询所有通知
cursor.execute("SELECT id, receiver_type, receiver_id, title, type, related_id, is_read, created_at FROM notification")
rows = cursor.fetchall()

print("=== 所有通知 ===")
for row in rows:
    print(f"ID: {row[0]}, 接收者: {row[1]}:{row[2]}, 类型: {row[4]}, 标题: {row[3]}, 已读: {row[6]}, 活动ID: {row[5]}")

print("\n=== 活动变更通知 ===")
cursor.execute("SELECT id, receiver_id, content FROM notification WHERE type = 'activity_change'")
change_rows = cursor.fetchall()
for row in change_rows:
    print(f"ID: {row[0]}, 用户ID: {row[1]}, 内容: {row[2]}")

conn.close()