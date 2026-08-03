# NCP Developer Tools 배포 연습 (Flask 예제, GitHub 대신 SourceCommit 사용)

> GitHub 2차 인증 잠김 문제로 GitHub 대신 **NCP SourceCommit**을 소스 저장소로 사용하는 버전입니다.
> 참고 튜토리얼: [Kubernetes 클러스터에 애플리케이션 배포하기 — NAVER Cloud Developer Tools 실습](https://medium.com/naver-cloud-platform/kubernetes-%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%97%90-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0-494f653341ab)
> 파일 구성(`app.py`, `requirements.txt`, `Dockerfile`, `flask-deployment.yaml`, `flask-service.yaml`)은 튜토리얼과 동일하게 맞췄습니다.

## 0. 사전 준비물

- [ ] NKS 클러스터 1개
- [ ] Container Registry 레지스트리 1개
- [ ] Object Storage 버킷 1개 (SourceBuild 산출물 저장용, 선택)
- [ ] Developer Tools(SourceCommit/SourceBuild/SourceDeploy/SourcePipeline) 이용 신청

## 1. SourceCommit: 저장소 생성 및 코드 업로드

1. NCP 콘솔 → Developer Tools → SourceCommit → 저장소 생성 (예: `flask-cicd-practice`)
2. 이 폴더(`cicd-practice-flask/`) 내용을 새 SourceCommit 저장소로 push
   ```
   cd cicd-practice-flask
   git init
   git remote add origin <SourceCommit repository clone URL>
   git add .
   git commit -m "practice: initial commit"
   git push origin main
   ```
   - SourceCommit 인증은 HTTPS(계정 비밀번호/Access Key) 또는 SSH 키 방식입니다. GitHub 계정과 무관합니다.

## 2. Container Registry + NKS 연동 준비

1. Container Registry 레지스트리를 만들고 `<registry-name>.kr.ncr.ntruss.com` 도메인을 확인합니다.
2. NKS가 이미지를 pull할 수 있도록 `imagePullSecret`을 생성합니다.
   ```
   kubectl create secret docker-registry ncr-pull-secret \
     --docker-server=<registry-name>.kr.ncr.ntruss.com \
     --docker-username=<NCP Access Key> \
     --docker-password=<NCP Secret Key>
   ```
   - `flask-deployment.yaml`의 `imagePullSecrets.name: ncr-pull-secret`과 이름을 맞춥니다.
3. `flask-deployment.yaml`의 `<TODO: Container Registry 도메인>`을 실제 도메인으로 교체합니다.

## 3. SourceBuild

1. Developer Tools → SourceBuild → 빌드 프로젝트 생성
2. 소스: SourceCommit / `flask-cicd-practice` / `main` 브랜치
3. Dockerfile 빌드 옵션: 경로 `Dockerfile`, 저장할 Container Registry, 이미지 이름 `flask-cicd-practice`, 태그 `latest`
4. (선택) 빌드 산출물 Object Storage 업로드 활성화 — 버킷/경로 지정
5. 저장 후 1회 수동 빌드 실행 → Container Registry에 이미지 push 확인

## 4. SourceDeploy

1. Developer Tools → SourceDeploy → 배포 프로젝트 생성, 배포 대상 = NKS 클러스터
2. 배포 시나리오 생성:
   - 매니페스트 저장소: SourceCommit / `flask-cicd-practice` / `main`
   - 매니페스트 경로: `flask-deployment.yaml`, `flask-service.yaml`
   - 배포 전략: Rolling
3. 저장 후 1회 수동 배포 실행

## 5. SourcePipeline

1. Developer Tools → SourcePipeline → 파이프라인 생성
2. Source: SourceCommit `flask-cicd-practice` / `main` (push 트리거)
3. Build: 3단계 SourceBuild 프로젝트
4. Deploy: 4단계 SourceDeploy 프로젝트/시나리오
5. SourceCommit에 커밋 push → Build → Deploy 자동 실행 확인

## 6. 검증

```
kubectl get pods -l app=flask-cicd-practice
kubectl get svc flask-cicd-practice
kubectl port-forward svc/flask-cicd-practice 8080:80
curl localhost:8080/
```

## 7. Rollback 연습

- `kubectl rollout undo deployment/flask-cicd-practice`
- SourceDeploy 배포 이력에서 이전 배포 건 재실행

## 8. 정리 (비용 방지)

- [ ] `kubectl delete -f flask-deployment.yaml -f flask-service.yaml`
- [ ] Container Registry 테스트 이미지 삭제
- [ ] Object Storage 테스트 산출물 삭제
- [ ] NKS 클러스터 삭제 (계속 쓸 게 아니라면)
- [ ] 실습용 Access Key 폐기

## GitHub로 나중에 전환하고 싶다면

2차 인증 문제가 풀리면, SourceBuild/SourceDeploy 소스 설정에서 "SourceCommit" 대신 "GitHub"를 선택하고 Personal Access Token 또는 OAuth로 연결하면 됩니다. 파일 구성은 동일하게 재사용 가능합니다.
