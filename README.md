Course Management System API

Teachers can publish a course and students can enroll.
Admin can see the courses and users.

User Roles :

  Teacher :
    
    Anyone can register as teacher.
    Teacher has user role as 'teacher'.
    Teacher can publish/delete/update his/her course.
    Teacher can see students enrolled in his courses.

  Student :

    Anyone can register as student.
    Student has user role as 'student'.
    Student can enroll/unenroll a course.
    Student can see courses enrolled by him/her or course available to him for enrollment.

  Admin :

    A person can be registered as admin only if he/she has database access.
    One admin has been registered already with email = 'rohilla@rohilla.co.in' and password = 'passpass'
    Admin has user role as 'admin'.
    Admin can view all the courses and Users.
    Admin can access admin specific routes.


Register :

  {<br/>
    "name": "user",<br/>
    "email": "user@rohilla.co.in",<br/>
    "password": "passpass",<br/>
    "role": "student"<br/>
  }<br/>
  "role": can be student/teacher.<br/>

Login :

  {<br/>
    "email": "user@rohilla.co.in",<br/>
    "password": "passpass"<br/>
  }<br/>

The access tokens and refresh tokens must be provided in Authorization header for accessing authorized routes.<br/>
The credentials and any data must be send as json in request body.<br/>
Postman Collection, import "Course Management API.postman_collection.json"<br/>

