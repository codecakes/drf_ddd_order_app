# drf_ddd_order_app
An example Order App in transient DDD style on django drf

### Note
This is for demo only.
DO NOT RUN IN PRODUCTION. USE AT YOUR OWN RISK.
Django keys and hard coded secrets inside.

## Motivation
How to use DDD in django drf.
When you start out with a web application,
it is easy to prototype using RAD tools like django & drf.
Eventually, you get locked-in and there is little space to free your concerns
to Plain-Old Python Objects.

Why do that? Here is a good article from Snapchat to understand why:
https://eng.snap.com/en-US/monolith-to-multicloud-microservices-snap-service-mesh

You will see couple of libraries sprinkled here and there.
That is to showcase what may you need in order to build this.

## How to Test?

Just do this to register 
```bash
curl --location --request POST 'https://drfdddorderapp-production.up.railway.app/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "dkljhlksfrfasasddas",
    "password": "kldsjfsda"
}'
```

And this to login 
```bash
curl --location --request POST 'https://drfdddorderapp-production.up.railway.app/auth/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "dkljhlksfrfasasddas",
    "password": "kldsjfsda"
}'
```

In both cases you should get a jwt back.

Then you can use it to create an order.
Which is the motivation for this app.
But it is not done yet.

## How to Run locally?
Build it like:

```bash
docker build . --progress=auto -t order_mgmt:demo -f Dockerfile
```

and run it like:
```bash
docker run -e "DEBUG=FALSE" -e "ALLOWED_ENV_URL=127.0.0.1" -p 8000:8000 order_mgmt:demo
```
<br />

#### But You have left password in plain text? This isn't there, that isn't there, this is missing, 
Yes, See what this repo is about in the above description.

#### But but but!
I charge for these services. I am not a charity.


### TODO:
- [x] Create Tokens
- [x] Create Users
- [x] Login Users
- [ ] Add pre-commit, pylintrc and best practices security keys and configurations.
- [ ] Add CI/CD
- [ ] Create Order
- [ ] Create Fake payment processor
- [ ] Get Order with status
- [ ] List Items
- [ ] Add tests
- [ ] Add redis queue for incoming orders processing.
- [ ] Add redis queue for confirmed orders that can be used in `Get Order`.
- [ ] Replace sqlite with a separate Database service for Order Management and User management.
- [ ] Refactor to async requests and processing
- [ ] Separate Order Management and User Management into microservices.
