# Задание 1  

## 1. Установить Jenkins, SAST – Semgrep, SCA – Dependency Check, Container Scanning – Trivy, DAST – OWASP ZAP.

**Machine**: Ubuntu 22.04 in AWS Cloud   
### 1.1. Jenkins:
```bash
chmod +x install-jenkins.sh
./install-jenkins.sh
``` 
![](images/Screenshot%202023-04-19%20at%2013.56.46.png)
### 1.2. Semgrep 
```bash
chmod +x install-semgrep.sh 
./install-semgrep.sh
```
Warning: ` WARNING: The script semgrep is installed in '/home/ubuntu/.local/bin' which is not on PATH.`
-> We should add this path to $PATH 
```bash
$ sudo vi ~/.bashrc
export PATH="/home/ubuntu/.local/bin:$PATH"
$ source ~/.bashrc
```
### 1.3. Dependency check
```bash
$ git clone --depth 1 https://github.com/jeremylong/DependencyCheck.git
$ cd DependencyCheck
$ mvn -s settings.xml install
$./cli/target/release/bin/dependency-check.sh -h
$ ./cli/target/release/bin/dependency-check.sh --out . --scan ./src/test/resources
```
### 1.4. Trivy 

```bash
chmod +x install-trivy.sh
./install-trivy.sh
```
1.5. OWASP ZAP
```bash
chmod +x install-zap.sh
./install-zap.sh
```
## 2. Разработать Dockerfile для сборки веб-приложения (код веб-сервиса можно взять из открытых источников, на любом из языков программирования). Использование приложений на микросервисной архитектуре – приветствуется. При разработке Dockerfile, необходимо ориентироваться на лучшие практики по безопасности: (например, https://sysdig.com/blog/dockerfile-best-practices/).

The application code is showed in the repository `app.py`  

Clone source code from repository: `git clone https://github.com/tronglamitmo142/hackathon_devsecops.git`  

The Dockerfile: [Dockerfile](./Dockerfile)

## 3. Написать СI/СD Pipeline

Add global credentials in Jenkins:
- Github credentials (for accesing to github repository):
![](./images/Screenshot%202023-04-20%20at%2010.55.41.png)
- Install dependency-check plugin:
  - Download the plugin
  - Install the plugin 
    ![](./images/Screenshot%202023-04-19%20at%2015.07.58.png)
    ![](images/Screenshot%202023-04-20%20at%2010.57.38.png)
- In Linux server:
  - Install `docker`:  
    ```bash
    chmod +x install-docker.sh
    ./install-docker.sh
    ```
  - Because when we run jenkins ci/cd pipeline, the user is jenkins, so we need to add jenkins to group docker, so we can use docker in jenkins without sudo permission
    ```bash
    usermod -a -G docker jenkins
    ``` 
  - add permision to jenkin suser in agent machine
    ```bash
    usermod -a -G root jenkins
    ```
### 1.2. Write Jenkinsfile
Every stages is describe in [Jenkinsfile](./Jenkinsfile) 
![](images/Screenshot%202023-04-20%20at%2011.05.50.png)
Scanning result is showed in workspace directory and dashboard: 
![](images/Screenshot%202023-04-20%20at%2011.16.24.png)

Details: 
- [SAST report](./scanning_report/SAST_report.txt)
- SCA (dependency check):
  ![](images/Screenshot%202023-04-20%20at%2011.20.41.png)
- [Container Scanning Report](./scanning_report/result.cdx)
- [DAST report](./scanning_report/DAST_report.txt)

# Задание 2
Note: The PodSecurityPolicy is unvailable in Kubernetes version 1.25+ (Now is 1.27), so I use older Kubernetes version (1.24.0) and kubectl (v1.24.0) for this lab
## 1. Установить Minikube на вашу хостовую машину.
```bash
chmod +x install-minikube-kubectl.sh
./install-minikube-kubectl.sh
```
Verify:
```bash
kubectl version --client
```
Start minikube
```bash 
minikube start --kubernetes-version=v1.24.0
```
Result:  
![](images/Screenshot%202023-04-20%20at%2013.35.32.png)
![](./images/Screenshot%202023-04-20%20at%2013.35.55.png)

## 2. Установить PodSecurityPolicy для Minikube, согласно мануалу: https://minikube.sigs.k8s.io/docs/tutorials/using_psp/

Create the directory 
```bash
mkdir -p ~/.minikube/files/etc/kubernetes/addons
```
Create [PodSecurityPolicy](./psp.yaml) into `~/.minikube/files/etc/kubernetes/addons`

Apply [PodSecurityPolicy](./psp.yaml): 

```bash
kubectl apply -f ~/.minikube/files/etc/kubernetes/addons/psp.yaml
```
![](images/Screenshot%202023-04-20%20at%2013.48.15.png)

Reload minikube
```bash
minikube stop
minikube start --extra-config=apiserver.enable-admission-plugins=PodSecurityPolicy
```

## 3. Разработать Kubernetes templates yaml, которые будут запускать веб-сервис из задания 1, включающий в себя:
## - Deployment с Security Contexts из PodSecurityPolicy Restricted: (privileged: false, RunAsUser: 10000, fsGroup: 10000, SeLinux Rules, etc.), работающий на 8080 порту и вытягивающий образ из Dockerhub.
## - Маунт в контейнер Configmap и Secret (опционально).
## - Service по типу ClusterIP.
## - Ingress для публикации сервиса по HTTP.

Create [Deployment](./deployment.yaml)  
Create [Service](./service.yaml)  
Apply: 
```bash
kubectl apply -f service.yaml
kubectl apply -f deployment.yaml
```
Verify:
![](./images/Screenshot%202023-04-20%20at%2018.42.02.png)

Ingress Task:  
There are some problem with my EC2 machine, it can not rut ingress, tried different ways.
![](./images/Screenshot%202023-04-20%20at%2019.48.48.png)
So I tried to do this task in the another machine:  
Install ingress
```bash
minikube addons enable ingress
```
![](./images/Screenshot%202023-04-20%20at%2019.51.05.png)

Create [Ingress Object](./ingress.yaml)  
I run the nginx-ingress, so it will expose the application in port 80 

```bash
kubectl apply -f ingress.yaml
```
Verify   
![](./images/Screenshot%202023-04-20%20at%2019.59.55.png)
Address is ip of minikube node.
Access to this ip and verify the ingress object
```bash
minikube ssh 
curl localhost:80
```
Result:  
![](./images/Screenshot%202023-04-20%20at%2020.02.08.png)

