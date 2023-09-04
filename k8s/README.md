- É necessário ter um cluster rodando

- Utilizamos neste exemplo o kind, e temos um cluster multi-nodes rodando, com um control-plane e um worker

- Executar primeiro o comando para iniciar o cluster
 $ kind create cluster --config=kind.yaml

 -Executar cada yaml
 $ kubectl apply -f secrets-aws.yaml

 $ kubectl apply -f secrets-postgres.yaml

 $ kubectl apply -f deployment.yaml

 $ kubectl apply -f service.yaml

- Verificar pods
 $ kubectl get pods

 - Verificar service
 $ kubectl get service

 - Verificar deployment
 $ kubectl get deployment
 

