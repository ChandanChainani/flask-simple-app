# Sample Flask App with jwt authentication

- Login with username and password
  `curl --request POST --url http://localhost:5000/auth --header 'Content-Type: application/json' --data '{ "username": "user1", "password": "u1" }'`

- Get list of theatres
  `curl --request GET --url http://localhost:5000/theatres`

- Get theatre info
  `curl --request GET --url http://localhost:5000/theatres/Victory%20Theatre`

- Get theatre seats info
  `curl --request GET --url http://localhost:5000/theatres/One%20Theatre/seats --header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzIzMjg4NzUsImlhdCI6MTYzMjMyODU3NSwibmJmIjoxNjMyMzI4NTc1LCJpZGVudGl0eSI6MX0.qpYfoVPFgMDNw0X5QjRomkfw51NBnLmmc596CFKPXgE'`

- Add New theatre
  `curl --request POST --url http://localhost:5000/theatre/new --header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzIzMjg4NzUsImlhdCI6MTYzMjMyODU3NSwibmJmIjoxNjMyMzI4NTc1LCJpZGVudGl0eSI6MX0.qpYfoVPFgMDNw0X5QjRomkfw51NBnLmmc596CFKPXgE' --header 'Content-Type: application/json' --data '{ "name": "One Theatre", "seats": 30 }'`

- Book seats in theatre
  `curl --request POST --url http://localhost:5000/booking/new --header 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzIzMjk4NDcsImlhdCI6MTYzMjMyOTU0NywibmJmIjoxNjMyMzI5NTQ3LCJpZGVudGl0eSI6Mn0.As7BeeeMIGTC6LV3843ZJK5v6Rk5bUDcFCmyBLwr238' --header 'Content-Type: application/json' --data '{ "seats": 27 }'`
