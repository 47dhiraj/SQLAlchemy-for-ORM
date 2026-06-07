from database import get_session

from models import Employee

from sqlalchemy import func, select

from sqlalchemy.orm import aliased

from sqlalchemy.exc import SQLAlchemyError





session = get_session()




try:


    employee_count = session.scalar(select(func.count()).select_from(Employee))


    if employee_count < 1:


        ceo = Employee(
            name="Anita Sharma",
            role="CEO",
            department="Executive",
            level="Top level",
            manager_id=None               
        )


        session.add(ceo)
        session.flush()




        eng_manager = Employee(
            name="Rajan Mehta",
            role="VP Engineering",
            department="Engineering",
            level="Manager",
            manager_id=ceo.id            
        )

        mrkt_manager = Employee(
            name="Priya Verma",
            role="VP Marketing",
            department="Marketing",
            level="Manager",
            manager_id=ceo.id             
        )


        session.add_all([eng_manager, mrkt_manager])
        session.flush()




        engineering_employees = [

            Employee(
                name="Suresh Nair",
                role="Sr. Engineer",
                department="Engineering",
                level="Employee",
                manager_id=eng_manager.id      
            ),
            Employee(
                name="Deepa Joshi",
                role="Engineer",
                department="Engineering",
                level="Employee",
                manager_id=eng_manager.id    
            )

        ]


        marketing_employees = [
            Employee(
                name="Kavita Rao",
                role="Content Lead",
                department="Marketing",
                level="Employee",
                manager_id=mrkt_manager.id   
            ),
            Employee(
                name="Anil Kumar",
                role="Designer",
                department="Marketing",
                level="Employee",
                manager_id=mrkt_manager.id     
            )
        ]
        

        session.add_all(engineering_employees + marketing_employees)
        session.commit()

        print("\nSuccessfully seeded all records structured by management layers.\n")
        
    







    ## *************************************** SELF JOIN ***************************************

    Employee_Reference = aliased(Employee, name="employee_reference")


    stmt = (
        select(Employee, Employee_Reference)
        .join(Employee_Reference, Employee.manager_id == Employee_Reference.id)     
    )

    result = session.execute(stmt)
    # print(result)



    print("\nSELF JOIN")

    for employee, employee_reference in result:
        
        employee_name = employee.name if employee else 'None'
        employee_ref_name = employee_reference.name if employee_reference else 'No Manager'

        print(f"\nEmployee: {employee_name}  ----->  Manager: {employee_ref_name}")



    print("\n")
    # ## *************************************** SELF JOIN CLOSES ***************************************





except SQLAlchemyError as e:

    session.rollback()      

    print(f"Database error: {e}")




finally:

    session.close()

