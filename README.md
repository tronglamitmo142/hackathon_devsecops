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

The Dockerfile: `Dockerfile`

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
Every stages is describe in Jenkinsfile 
![](images/Screenshot%202023-04-20%20at%2011.05.50.png)
Scanning result is showed in workspace directory and dashboard: 
![](images/Screenshot%202023-04-20%20at%2011.16.24.png)

Details: 
- [SAST report](./scanning_report/SAST_report.txt)
- SCA (dependency check):
  ![](images/Screenshot%202023-04-20%20at%2011.20.41.png)
- [Container Scanning Report](./scanning_report/result.cdx)
- [DAST report](./scanning_report/DAST_report.txt)