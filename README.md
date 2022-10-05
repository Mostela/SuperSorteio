# Super Sorteio - Super Raffle

Version: 0.1.0

## Stack

* Golang ( Server not use frameworks, only Golang pure )
* Python
  * FastApi (Web Framework)
  * Walrus (Redis)
  * Peewee (Database ORM)
  * Pydantic (Schema Validation)
  * Uvicorn ( Web Server Implementation )
* MariaDb (Database Relational)
* KeyDB (Database key value, like Redis)
* Kubernetes ( Container Orchestration )
* Helm (Kubernetes Package Manager)
* Kind (Kubernetes platform  local to develop)
* Istio (Service Mesh)
* Docker Compose (Docker Orchestration)
* Docker
* K6 (Load Test, Test the application if she can be stable)

## Steps to Run

To run this application you need a Kubernetes Cluster, use one what you like how ACS, AKS, GKE or another. Here we use Kind.io

Follow the steps to install kind in your machine and created a cluster. I think is better you create a cluster with 3
 nodes, 1 Main and 2 Sons

Install Istio.io in your cluster to have a break with start load test

    istioctl install --profile=default -y

After you can install Nginx Ingress too, in my case I use [Kind](https://kind.sigs.k8s.io/docs/user/ingress/)

Now, can install a tools to help you to observer application in cluster like Kiali, Grafana and Jaeger

### Steps above we go start create application

After created your cluster go to folder [kubernetes](./kubernetes) and apply file [namespace](./kubernetes/namespace.yml)

    kubectl apply -f ./kubernetes/namespace.yml

create database inside cluster because is more simple to manager, you not need create security groups and another snuffs 
to access database, *But not make it in real life :)*

Let's install database MariaDb and KeyDb with Helm 

    helm install mysql bitnami/mariadb --namespace=sorteio --set auth.rootPassword=sorteio

    helm install keydb enapter/keydb --namespace=sorteio

wait some seconds to create new Namespace called `sorteio` and execute this command above

    kubectl apply -f ./kubernetes/

Will create another services like, deployment, load balance, destination rule and more in namespace `sorteio`
but not will stay stable because no have a database created at this moment.

Wait more one or two minutes and open your browser in [http://localhost/admin](http://localhost/admin), you can use 
this page to show data created by raffle application

    username: root
    password: sorteio
    host: mysql-mariadb
    database: leave blank

Create a new database with name `sorteio`


## Load Test


## Uses Cases


## Endpoints
