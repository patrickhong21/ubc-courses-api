from flask import Blueprint, request
from src.scraper import get_all_dept_info, get_dept_info, get_course_info, get_section_info

course = Blueprint("course", __name__, url_prefix="/api/v1/course")

@course.get("/info")
def info():
	dept = request.args.get("dept")
	num = request.args.get("num")
	section = request.args.get("section")
	year = request.args.get("year")
	session = request.args.get("session")

	# no args
	if dept is None and num is None and section is None and year is None and session is None:
		res = get_all_dept_info()
		return res, 200

	# only dept
	elif dept is not None and num is None and section is None and year is None and session is None:
		try:
			res = get_dept_info(dept)
			return res, 200
		except ValueError as e:
			return str(e), 404

	# dept, num, year, session
	elif dept is not None and num is not None and section is None and year is not None and session is not None:
		try:
			res = get_course_info(dept, num, year, session)
			return res, 200
		except ValueError as e:
			return str(e), 404
		
	# dept, num, section, year, session
	elif dept is not None and num is not None and section is not None and year is not None and session is not None:
		try:
			res = get_section_info(dept, num, section, year, session)
			return res, 200
		except ValueError as e:
			return str(e), 404
	
	else:
		return "Check your param arguments", 404