from fastapi import FastAPI
from pydantic import BaseModel
import clickhouse_connect
import uvicorn
import datetime

# Определите модель данных для логов
class Log(BaseModel):
    id: int
    event_type: str
    user_id: int
    parameters: str
    created_at: datetime.datetime
    # Добавьте остальные параметры

# Создайте клиент для подключения к ClickHouse
client = clickhouse_connect.get_client(host='localhost', port = 8123, username='default', password='')
client.command('CREATE DATABASE IF NOT EXISTS test')
# Создайте таблицу для логов
client.command('''
CREATE TABLE IF NOT EXISTS test.logs_test_wtime_1 (
    id UUID DEFAULT generateUUIDv4(),
    event_type String,
    user_id Int,
    parameters String,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
PRIMARY KEY id
ORDER BY id
SETTINGS index_granularity = 8192;
''')

app = FastAPI()

@app.post("/log")
async def log_event(log: Log):
    try:
        # Вставка данных в таблицу с использованием параметризованного запроса
        query = f'''
        INSERT INTO test.logs_test_wtime_1 (event_type, user_id, parameters) VALUES
        ('{log.event_type}', {log.user_id}, '{log.parameters}')
        '''
        client.command(query)
        return {"status": "log posted",
                "event_type": log.event_type, "user_id": log.user_id, "parameters": log.parameters,
                "created_at": log.created_at}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
