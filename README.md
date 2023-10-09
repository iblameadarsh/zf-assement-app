# zf-assement-app
An Assignment to build backend on rest api(s) to perform given tasks in assesment. 
This project is built in django, there are two apps in there consisting API(s) for all the mentioned tasks in the notion link.
1. Authentication - this app contains all user table for registration.
   a. register/ (for user registeration(Agents/Consumers))
   b. login/ (generates token for authentication after checking in user table)
   c. get-user (To verify if the token is correct and working this api provide user details for the token provided)
2. Zfundsapp - this app contains Product, order tables defined in models.py api routes -
   a. Agents registering users[GET]
   b.Agent retrieving list of clients/users they've registered.[GET]
   c. products/ - A viewset for admin to list, create products [GET,POST].
   d. Agents and users buying/creating orders for desired products. [GET]
The authentication part where I validate token and retrieve user details in each view can be improved, those certain lines of repetitive code could've been avoided but
would've required susbsequent time in setting up permissions and jwt customizations  and that would be a detour from completing the task, hence I went for a consistent approach.
