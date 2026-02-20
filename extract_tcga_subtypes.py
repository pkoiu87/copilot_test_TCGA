"""
의도: TCGA 유방암 데이터에서 분자 서브타입별(LumA, Basal, Her2)로 
      각각 80개씩 균형있게 추출하는 모듈
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def load_tcga_breast_cancer_data(metadata_file: str) -> pd.DataFrame:
    """
    의도: TCGA 유방암 메타데이터 파일을 로드하고 기본 전처리 수행
    
    Args:
        metadata_file: TCGA 유방암 메타데이터 파일 경로
        
    Returns:
        로드된 메타데이터 DataFrame
    """
    df = pd.read_csv(metadata_file)
    return df


def filter_by_subtypes(data: pd.DataFrame, 
                       subtype_column: str = 'subtype') -> Dict[str, pd.DataFrame]:
    """
    의도: 전체 데이터를 분자 서브타입별(LumA, Basal, Her2)로 그룹화
    
    Args:
        data: TCGA 메타데이터 DataFrame
        subtype_column: 서브타입이 저장된 컬럼명
        
    Returns:
        {서브타입명: 해당 서브타입 데이터}로 구성된 딕셔너리
    """
    subtypes_of_interest = ['LumA', 'Basal', 'Her2']
    grouped_data = {}
    
    for subtype in subtypes_of_interest:
        # 해당 서브타입의 샘플만 필터링
        subtype_data = data[data[subtype_column].str.strip() == subtype]
        grouped_data[subtype] = subtype_data
        print(f"{subtype} 서브타입: {len(subtype_data)}개 샘플 발견")
    
    return grouped_data


def balance_and_extract_samples(grouped_data: Dict[str, pd.DataFrame>,
                                samples_per_subtype: int = 80) -> pd.DataFrame:
    """
    의도: 각 서브타입에서 정확히 지정된 개수(기본값 80개)씩 
          무작위로 균형있게 추출
    
    Args:
        grouped_data: 서브타입별로 그룹화된 데이터
        samples_per_subtype: 각 서브타입에서 추출할 샘플 수
        
    Returns:
        추출된 샘플들이 합쳐진 DataFrame
    """
    extracted_samples = []
    
    for subtype, data in grouped_data.items():
        # 각 서브타입에서 지정된 개수만큼 랜덤 샘플링
        if len(data) >= samples_per_subtype:
            sampled_data = data.sample(n=samples_per_subtype, random_state=42)
            extracted_samples.append(sampled_data)
            print(f"✓ {subtype}: {len(sampled_data)}개 샘플 추출 완료")
        else:
            # 샘플 부족 시 경고 메시지
            print(f"⚠ {subtype}: 요청한 {samples_per_subtype}개보다 "
                  f"적은 {len(data)}개만 사용 가능")
            extracted_samples.append(data)
    
    # 모든 서브타입의 샘플을 하나로 합치기
    balanced_data = pd.concat(extracted_samples, ignore_index=True)
    
    return balanced_data


def validate_extraction_balance(balanced_data: pd.DataFrame,
                                subtype_column: str = 'subtype') -> Dict[str, int]:
    """
    의도: 추출된 데이터가 각 서브타입별로 균형있게 추출되었는지 검증
    
    Args:
        balanced_data: 추출된 데이터
        subtype_column: 서브타입 컬럼명
        
    Returns:
        {서브타입명: 개수}로 구성된 서브타입별 샘플 개수 딕셔너리
    """
    subtype_counts = balanced_data[subtype_column].value_counts().to_dict()
    
    print("\n=== 추출 결과 검증 ===")
    print(f"총 추출 샘플 수: {len(balanced_data)}")
    for subtype, count in sorted(subtype_counts.items()):
        print(f"  {subtype}: {count}개")
    
    return subtype_counts


def save_extracted_data(balanced_data: pd.DataFrame,
                       output_file: str) -> None:
    """
    의도: 추출된 균형잡힌 데이터를 CSV 파일로 저장
    
    Args:
        balanced_data: 추출된 데이터
        output_file: 저장할 파일 경로
    """
    balanced_data.to_csv(output_file, index=False)
    print(f"\n✓ 데이터 저장 완료: {output_file}")


def extract_tcga_subtypes_main(metadata_file: str,
                               output_file: str = 'tcga_balanced_subtypes.csv',
                               samples_per_subtype: int = 80) -> pd.DataFrame:
    """
    의도: TCGA 유방암 데이터에서 서브타입별로 균형있게 샘플을 추출하는 
          메인 파이프라인 함수
    
    Args:
        metadata_file: TCGA 메타데이터 파일 경로
        output_file: 결과를 저장할 파일 경로
        samples_per_subtype: 각 서브타입에서 추출할 샘플 수
        
    Returns:
        추출된 균형잡힌 데이터
    """
    print("=" * 50)
    print("TCGA 유방암 서브타입 균형 추출 시작")
    print("=" * 50)
    
    # 1단계: 데이터 로드
    print("\n[1단계] 메타데이터 로�� 중...")
    data = load_tcga_breast_cancer_data(metadata_file)
    print(f"총 {len(data)}개의 샘플 로드 완료")
    
    # 2단계: 서브타입별 그룹화
    print("\n[2단계] 서브타입별 그룹화 중...")
    grouped_data = filter_by_subtypes(data)
    
    # 3단계: 균형있게 샘플 추출
    print(f"\n[3단계] 각 서브타입에서 {samples_per_subtype}개씩 추출 중...")
    balanced_data = balance_and_extract_samples(grouped_data, samples_per_subtype)
    
    # 4단계: 추출 결과 검증
    print("\n[4단계] 추출 결과 검증...")
    validate_extraction_balance(balanced_data)
    
    # 5단계: 결과 저장
    print("\n[5단계] 결과 저장 중...")
    save_extracted_data(balanced_data, output_file)
    
    print("\n" + "=" * 50)
    print("작업 완료!")
    print("=" * 50)
    
    return balanced_data


# 사용 예시
if __name__ == "__main__":
    # TCGA 메타데이터 파일 경로를 지정하세요
    metadata_file = 'tcga_breast_cancer_metadata.csv'
    
    # 메인 함수 실행
    balanced_data = extract_tcga_subtypes_main(
        metadata_file=metadata_file,
        output_file='tcga_balanced_subtypes.csv',
        samples_per_subtype=80
    )
    
    # 추출된 데이터 확인
    print("\n추출된 데이터 미리보기:")
    print(balanced_data.head())