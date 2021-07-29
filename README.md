# Setu API

### To build Docker image:

`docker build -t setu_api:latest .`

### To run the get_bangalore_vaccine_slots function with custom date and pincodes:

`docker run -e DATE="30-07-2021" -e PINCODES="[530068, 560004, 560008]" setu_api`

### To run the tests with custom date:

`docker run -e DATE="30-07-2021" setu_api pytest`
