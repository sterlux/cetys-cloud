1. Instala AzureCli y Kubernetes CLI:

```
az login
```

2. Crea un Azure Container Registry (ACR):

   ```
   az acr create --resource-group turesourcegroup --name elnombredebeserunico --sku Basic
   ```

3. Build y push de las imagenes de Docker a ACR (abre docker desktop):

   ```
   docker build -t elnombredebeserunico.azurecr.io/product-service:v1 .\product-service\
   az acr login --name elnombredebeserunico
   docker push elnombredebeserunico.azurecr.io/product-service:v1
   ```

4. Repite el paso 2 para order-service

5. Crear el cluster AKS (Azure Kubernetes Service):

   ```
   az provider register --namespace Microsoft.ContainerService
   az provider show -n Microsoft.ContainerService --query registrationState
   ```

6. Espera que el último regrese "Registered" y continua creando el cluster (tarda un poco):

   ```
   az aks create --resource-group tu-resource-group --name AKSCluster --node-count 2 --generate-ssh-keys
   ```

7. Conectarse al cluster AKS:

   ```
   az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
   ```

8. Deploy the services:

   ```
   kubectl apply -f product-deployment.yaml
   kubectl apply -f order-deployment.yaml
   ```

9. Get the external IP of the order service:
   ```
   kubectl get services order-service
   ```

Utilizar la IP pública para probar la app:

1. Get products:

   ```
   curl http://<external-ip>/products
   ```

2. Si nos da error, seguramente hubo error con el docker pull:

   ```
   kubectl get pods
   ```

3. Esto nos mostrará si el status es ImagePullBackOff.

4. Si nos dio el error, tenemos que actualizar para que se junte el ACR con el AKS Cluster:

   ```
   az aks update -n AKSCluster -g tu-resource-group --attach-acr elnombredebeserunico
   kubectl delete pod --all

   ```

5. Create an order:

   ```
   curl -X POST -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 2}' http://<external-ip>/orders
   ```

6. Get orders:
   ```
   curl http://<external-ip>/orders
   ```
