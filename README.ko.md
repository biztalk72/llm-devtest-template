# LLM DevTest 템플릿

[English](README.en.md) | [한국어](README.ko.md)

Ollama를 사용한 LLM 통합 Python 웹 애플리케이션 및 API 구축을 위한 프로덕션 준비 템플릿입니다. GitHub Actions를 통한 CI/CD 자동화와 함께 완전한 개발/테스트 환경 설정이 포함되어 있습니다.

## 주요 기능

- 🤖 **Ollama 통합**: 비동기 지원을 갖춘 바로 사용 가능한 LLM 클라이언트
- 🚀 **FastAPI 백엔드**: 자동 문서화를 지원하는 최신 고속 API 프레임워크
- 🧪 **완전한 테스트**: 커버리지 리포트를 포함한 Pytest 설정
- 🔄 **CI/CD 파이프라인**: GitHub Actions를 통한 자동화된 테스트 및 배포
- 🌍 **다중 환경**: dev/test/prod 환경별 별도 설정
- 🔐 **GPG 서명**: 보안을 위한 자동 커밋 서명
- 📊 **코드 품질**: Black, Ruff, MyPy 구성

## 사전 요구사항

- Python 3.10+
- [Ollama](https://ollama.ai) 설치 및 실행 중
- GPG가 구성된 Git (커밋 서명용)

## 빠른 시작

### 1. 클론 및 설정

```bash
git clone <your-repo-url>
cd llm-devtest-template
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 2. 환경 설정

적절한 환경 파일을 복사하세요:

```bash
# 개발 환경
cp .env.dev.example .env

# 테스트 환경
cp .env.test.example .env

# 프로덕션 환경
cp .env.prod.example .env
```

`.env` 파일을 원하는 설정으로 수정하세요.

### 3. 애플리케이션 실행

```bash
# 개발 모드 (자동 리로드)
python src/main.py

# 또는 uvicorn 직접 사용
uvicorn src.main:app --reload
```

API는 `http://localhost:8000`에서 사용 가능합니다
- API 문서: `http://localhost:8000/docs`
- 대체 문서: `http://localhost:8000/redoc`

### 4. 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=src --cov-report=html

# 특정 테스트 파일 실행
pytest tests/test_main.py -v
```

## 프로젝트 구조

```
llm-devtest-template/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│       ├── ci.yml         # 자동화된 테스트
│       ├── deploy-dev.yml # 개발 배포
│       └── deploy-test.yml# 테스트 배포
├── src/
│   ├── __init__.py
│   ├── main.py            # FastAPI 애플리케이션
│   ├── config.py          # 설정 관리
│   └── ollama_client.py   # Ollama LLM 통합
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest 픽스처
│   ├── test_config.py
│   ├── test_main.py
│   └── test_ollama_client.py
├── .env.*.example         # 환경 템플릿
├── .gitignore
├── pyproject.toml         # 프로젝트 설정
├── requirements.txt       # 프로덕션 의존성
└── requirements-dev.txt   # 개발 의존성
```

## API 엔드포인트

### 핵심 엔드포인트

- `GET /` - 서비스 정보가 포함된 루트 엔드포인트
- `GET /health` - 헬스 체크 (Ollama 상태 포함)
- `GET /models` - 사용 가능한 Ollama 모델 목록

### LLM 엔드포인트

- `POST /generate` - 프롬프트로부터 텍스트 생성

**요청 예시:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "양자 컴퓨팅을 쉽게 설명해주세요",
    "temperature": 0.7,
    "stream": false
  }'
```

## 브랜치 전략

- `main` - 프로덕션 준비 코드 (보호됨)
- `dev` - 개발 브랜치 (개발 환경에 자동 배포)
- `test` - 테스트 브랜치 (테스트 환경에 자동 배포)

### 워크플로우

1. `dev`에서 기능 브랜치 생성
2. 변경 사항 작성 및 커밋 (GPG 서명됨)
3. 푸시 및 `dev`로 PR 생성
4. CI 자동 실행 (테스트, 린팅, 타입 체킹)
5. `dev`로 병합 후 개발 환경에 자동 배포
6. 테스트 환경을 위해 `test`로 병합
7. 프로덕션을 위해 `main`으로 병합

## 환경 변수

### 개발 환경 (.env.dev)

- `OLLAMA_MODEL=kimi2.5:latest` - Kimi 2.5 모델 (메인 LLM)
- `API_DEBUG=true` - 디버그 모드 활성화
- `LOG_LEVEL=DEBUG` - 상세 로깅

### 테스트 환경 (.env.test)

- `OLLAMA_MODEL=deepseek-coder:latest` - 테스트에 최적화
- `TEST_MODE=true` - 테스트 전용 기능 활성화
- `LOG_LEVEL=INFO` - 표준 로깅

### 프로덕션 환경 (.env.prod)

- `OLLAMA_MODEL=kimi2.5:latest` - Kimi 2.5 모델 (메인 LLM)
- `API_DEBUG=false` - 디버그 모드 비활성화
- `LOG_LEVEL=WARNING` - 최소 로깅

## 개발

### 코드 품질

```bash
# 코드 포맷팅
black src/ tests/

# 코드 린팅
ruff check src/ tests/

# 타입 체크
mypy src/

# 모든 검사 실행
black src/ tests/ && ruff check src/ tests/ && mypy src/
```

### 의존성 추가

```bash
# 프로덕션용 requirements.txt에 추가
echo "package-name>=1.0.0" >> requirements.txt

# 개발용 requirements-dev.txt에만 추가
echo "package-name>=1.0.0" >> requirements-dev.txt

# 설치
pip install -r requirements-dev.txt
```

## CI/CD

### GitHub Actions 워크플로우

1. **CI** (`ci.yml`) - 모든 푸시/PR에서 실행
   - Python 3.10, 3.11, 3.12에서 테스트
   - Ruff로 린팅
   - Black으로 포맷 체크
   - MyPy로 타입 체크
   - 커버리지 리포트

2. **개발 배포** (`deploy-dev.yml`) - `dev`로 푸시 시 실행
   - 테스트 실행
   - 개발 환경에 배포

3. **테스트 배포** (`deploy-test.yml`) - `test`로 푸시 시 실행
   - 커버리지를 포함한 전체 테스트 스위트 실행
   - 통합 테스트
   - 테스트 환경에 배포

## Ollama 모델

사용 사례별 권장 모델:

- **개발**: `kimi2.5:latest` (메인 LLM, 고성능)
- **테스트**: `deepseek-coder:latest` (빠르고 코드 중심)
- **프로덕션**: `kimi2.5:latest` (메인 LLM, 최적화)
- **대안**: `llama3:latest` 또는 `mistral:latest` (대체 옵션)

새 모델 다운로드:

```bash
ollama pull kimi2.5:latest
ollama pull deepseek-coder:latest
ollama pull llama3:latest
```

## 문제 해결

### Ollama 연결 안됨

```bash
# Ollama 실행 중인지 확인
ollama list

# Ollama 시작 (필요시)
ollama serve
```

### Import 오류

```bash
# 의존성 재설치
pip install -r requirements-dev.txt --force-reinstall
```

### GPG 서명 문제

```bash
# GPG 키 확인
git config --global user.signingkey

# GPG 테스트
echo "test" | gpg --clearsign
```

## 기여

기여 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## 라이선스

MIT License - LICENSE 파일 참조

## 작성자

Brian (re3539@outlook.com)

---

**Co-Authored-By: Warp <agent@warp.dev>**
