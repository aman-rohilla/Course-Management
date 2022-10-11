## Course Management API

#### Python, Flask, MongoDB, pymongo, REST API, JWT, User Authentication

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
    Student can see courses available for enrollment.
    Student can see courses enrolled by him/her.

  Admin :

    A person can be registered as admin only if he/she has database access.
    One admin has been registered already with email = 'rohilla@rohilla.co.in' and password = 'passpass'
    Admin has user role as 'admin'.
    Admin can view all the courses and Users.
    Admin can access admin specific routes.


Register :
<pre>
  {
    "name": "user",
    "email": "user@rohilla.co.in",
    "password": "passpass",
    "role": "student"
  }
  "role": can be student/teacher.
</pre>
Login :
<pre>
  {
    "email": "user@rohilla.co.in",
    "password": "passpass"
  }
</pre>
The access tokens and refresh tokens must be provided in Authorization header for accessing authorized routes.<br/>
The credentials and any data must be send as json in request body.<br/>
Postman Collection, import "Course Management API.postman_collection.json"<br/>

