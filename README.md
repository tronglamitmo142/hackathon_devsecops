1. Install Jenkins, SAST - Semgrep, SCA - Dependency Check, Container Scanning - Trivy, DAST - OWSAP ZAP 

Machine: Ubuntu 20.04 in AWS Cloud 
1.1. Jenkins:
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

lamnt56
1

1.2. Semgrep 
```bash
python3 -m pip install semgrep
semgrep --version
```
Exits the warning: ` WARNING: The script semgrep is installed in '/home/ubuntu/.local/bin' which is not on PATH.`
We should add this path to $PATH 
```bash
sudo vi ~/.bashrc
export PATH="/home/ubuntu/.local/bin:$PATH"
source ~/.bashrc
```
1.3. Dependency check
```bash
git clone --depth 1 https://github.com/jeremylong/DependencyCheck.git
cd DependencyCheck
mvn -s settings.xml install
./cli/target/release/bin/dependency-check.sh -h
$ ./cli/target/release/bin/dependency-check.sh --out . --scan ./src/test/resources

```
1.4. Trivy 

```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```
1.5. OWASP ZAP
```bash
wget https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz
tar -xvf ZAP_2.12.0_Linux.tar.gz
```



