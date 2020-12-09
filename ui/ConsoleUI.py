from src.UBCProfFinder import ProfFinder

course_dept = input("Enter course name: ").upper()
course_num = input("Enter course number: ").upper()
section = input("Enter section: ").upper()


prof_finder = ProfFinder()
try:
    prof_finder.find_prof(course_dept, course_num, section)
finally:
    pass

