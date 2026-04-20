from database import get_session            

from models import Student, Course, Enrollment


from sqlalchemy import select, func

from sqlalchemy.exc import SQLAlchemyError



session = get_session()




try:

    ## *************************** Data Insertion (Objects creation) ***************************

    user_count = session.scalar(select(func.count(Student.id)))

    if user_count < 1:

        math = Course(title='Mathematics')
        physics = Course(title='Physics')

        ram = Student(
            name='Ram',
            enrollments=[
                Enrollment(course=math, grade="A+"),
                Enrollment(course=physics, grade="A")
            ]
        )

        shyam = Student(
            name='Shyam',
            enrollments=[
                Enrollment(course=math, grade="A")
            ]
        )

        session.add_all([ram, shyam])
        session.commit()







    ## *************************** Fetching related data by student ***************************


    ram = session.execute(select(Student).filter_by(name='Ram')).scalar_one()
    shyam = session.execute(select(Student).filter_by(name='Shyam')).scalar_one()


    ram_courses = [enrollment.course.title for enrollment in ram.enrollments]

    print(f"Ram's Courses: {ram_courses}")
    # for course in ram_courses:
    #     print(course)
    


    shyam_courses = [enrollment.course.title for enrollment in shyam.enrollments]

    print(f"Shyam's Courses: {shyam_courses}")
    # for course in shyam_courses:
    #     print(course)






    ## *************************** Fetching related data by course ***************************


    math = session.execute(select(Course).filter_by(title='Mathematics')).scalar_one()
    physics = session.execute(select(Course).filter_by(title='Physics')).scalar_one()


    math_students = [enrollment.student.name for enrollment in math.enrollments]

    print(f"Math students: {math_students}")
    # for student in math_students:
    #     print(student)

    

    physics_students = [enrollment.student.name for enrollment in physics.enrollments]

    print(f"Physics students: {physics_students}")
    # for student in physics_students:
    #     print(student)






    ## ********** Accessing the extra field/data  **********

    ram= session.execute(select(Student).filter_by(name='Ram')).scalar_one()
 
    for enrollment in ram.enrollments:
        print(enrollment.student.name,', ', enrollment.course.title,', ', enrollment.grade)




    math = session.execute(select(Course).filter_by(title='Mathematics')).scalar_one()

    for enrollment in math.enrollments:
        print(enrollment.course.title,', ', enrollment.student.name,', ', enrollment.grade)



    

except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")
    

finally:
    session.close()
