# Dockerfile

# 베이스 이미지로 Python 3.8 사용
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# 로컬의 requirements.txt를 컨테이너로 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# game-archive 폴더의 모든 파일과 하위 폴더를 컨테이너로 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python", "run.py"]