- To start the api server just run

```commandline
    python3 main.py
```

- Some sample requests
    - To create a customer
      ```commandline
         curl -X POST -H "Content-type:application/json" -H 'x-api-key:'FMfcgzGrbHsKxblngBMPGtCpQvzfkvSJ''  -d '{"name":"test","email":"test@gmail.com","phone":"0123456789","department":"HR","country":"india"}'  http://127.0.0.1:8080/customer
      ```
    - To get a customer's detail
      ```commandline
      curl -H "Content-type:application/json" -H 'x-api-key:FMfcgzGrbHsKxblngBMPGtCpQvzfkvSJ'  'http://127.0.0.1:8080/customer/<c_id>'
      ```
    - To get all customer detail
      ```commandline
      curl -H "Content-type:application/json" -H 'x-api-key:FMfcgzGrbHsKxblngBMPGtCpQvzfkvSJ'  'http://127.0.0.1:8080/customer/'
      ```
    - To delete a customer
      ```commandline
      curl -X DELETE -H "Content-type:application/json" 'http://127.0.0.1:8080/customer/<c_id>'
      ```
    - To update a customer's detail
      ```commandline
      curl -X POST -H 'x-api-key:FMfcgzGrbHsKxblngBMPGtCpQvzfkvSJ' -H "Content-type:application/json" -d '{"department":"Management","phone":9839542709}'  http://127.0.0.1:8080/customer/c0263f55-6997-4dd6-8cd3-cb2a5e7e4859
      ```
