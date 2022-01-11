This is my bot to buy sneakers from **NIKE SNKRS** (tested RU only). This code has been written in Jan 2021 and it was my very first experience in OOP (so please be gentle). 
The main goal of the project was not only just to buy sneakers but also to test my DevOps skills using Gitlab-CI.
***
1) Desktop - just the code itself to try if script is still working;
2) Docker-compose - create docker-compose.yaml file using python3 templating, build an image and run it;
3) Helm - build an image using Kaniko, upload it to Gitlab Registry and deploy as K8s jobs using Helm, upload results to S3 created by Terraform;
4) AWS - build a custom AMI using Packer, create VPC,EC2,S3 using Terraform and configure nodes using Ansible, upload results to S3  
***

Some issues about code:

- I use a couple of .crx extensions (it's a secret which ones) because Nike anti-bot algorithms is not a joke. If you want to do the same, just google how to download browser extensions in .crx format, put them in your project directory and change their names at **lines 33-34** and **46-47** in the sneakers.py file. If you want to skip this, just comment these lines;
- Use residential proxies with good score only, otherwise you won't be able even to login;
- Accepting cookies may be a problem, uncomment **172-173** to cope with it;
- You'd better have only 1 delivery address in your account;
- The more accs you use, the better chance you have.
