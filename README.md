# 프로젝트 개요
이 프로젝트는 TCGA 데이터 분석을 위한 도구입니다. TCGA(Tumor Cancer Genome Atlas) 데이터 세트를 활용하여 암 유전체 데이터를 분석하고 시각화하는 기능을 제공합니다.

# 설치 방법
1. 이 저장소를 클론합니다.
   ```
   git clone https://github.com/pkoiu87/copilot_test_TCGA.git
   ```
2. 필요한 종속성을 설치합니다.
   ```
   cd copilot_test_TCGA
   pip install -r requirements.txt
   ```

# 사용 가이드
프로젝트를 실행하기 위해 필요한 명령어는 다음과 같습니다.
```bash
python main.py --input <input_file> --output <output_file>
```

# 파일 구조
```
/copilot_test_TCGA
|-- main.py        # 메인 실행 파일
|-- requirements.txt # 필요한 패키지 목록
|-- data/         # 데이터 파일 저장소
|-- results/      # 결과 파일 저장소
```

# 입력/출력 형식
- **입력**: TCGA 데이터 세트 파일 (CSV 형식)
- **출력**: 분석 결과가 포함된 CSV 파일

# 예시 결과
분석이 성공적으로 완료되면 출력 파일은 다음과 같은 형식으로 저장됩니다:
```
Gene,Expression
TP53,0.85
EGFR,0.76
```

# 중요 참고 사항
- 이 프로젝트는 연구 목적으로만 사용되어야 합니다.
- TCGA 데이터에 대한 접근 권한이 필요합니다.
  
이 README 파일은 프로젝트의 모든 주요 정보를 담고 있습니다.