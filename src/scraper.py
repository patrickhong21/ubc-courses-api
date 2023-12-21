from typing import Dict
import requests
from bs4 import BeautifulSoup
import re

def get_all_dept_info() -> Dict:
	url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments"

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
	}

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")

	res = {}

	tables = soup.find_all("table")
	departments = []

	for table in tables:
		rows = table.find_all("tr")
		for row in rows:
			columns = row.find_all("td")
			if len(columns) == 3:
				code = columns[0].text.strip().split(" ")[0]
				title = columns[1].text.strip()
				faculty = columns[2].text.strip()
				departments.append({"code": code, "title": title, "faculty": faculty})
				
	res["departments"] = departments

	return res

def get_dept_info(dept: str) -> Dict:
	url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept={dept}"

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
	}

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")

	if soup.find(string=re.compile("The requested subject is either no longer offered")) is not None:
		raise ValueError("Department not found.")

	res = {}

	subject_code = soup.find_all("h5")[0].text.strip()
	res["subject_code"] = subject_code.split(" ")[3]
	res["subject"] = subject_code.split("(")[1].split(")")[0]

	res["description"] = soup.find_all("p")[0].text.strip().replace("\r\n", "")

	tables = soup.find_all("table")
	courses = []

	for table in tables:
		rows = table.find_all("tr")
		for row in rows:
			columns = row.find_all("td")
			if len(columns) == 2:
				course = columns[0].text.strip()
				title = columns[1].text.strip()
				courses.append({"course": course, "title": title})
				
	res["courses"] = courses

	return res

def get_course_info(dept: str, num: str, year: str, session: str) -> Dict:
	url = f"https://courses.students.ubc.ca/cs/courseschedule?sesscd={session}&pname=subjarea&tname=subj-course&sessyr={year}&course={num}&dept={dept}"

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
	}

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")

	if soup.find(string=re.compile("The requested course is either no longer offered")) is not None:
		raise ValueError("Course not found.")

	res = {}

	course = soup.find_all("h4")[0].text.strip()
	res["course"] = " ".join(course.split(" ")[0:2])
	res["title"] = " ".join(course.split(" ")[2:])

	res["description"] = soup.find_all("p")[0].text.strip().replace("\r\n", "")
	res["credits"] = soup.find(string=re.compile("Credits")).split(" ")[-1]

	tables = soup.find_all("table")
	sections = []
	
	for table in tables:
		rows = table.find_all("tr")
		
		# track last row attributes for when a section uses two rows
		prev = {"status": "", "section": ""}
		for row in rows:
			columns = row.find_all("td")
			
			if len(columns) >= 2:
				sections.append({
					"status": columns[0].text.strip() if columns[0].text.strip() != "" else prev["status"],
					"section": columns[1].text.strip() if columns[1].text.strip() != "" else prev["section"],
					"activity": columns[2].text.strip(),
					"term": columns[3].text.strip(),
					"mode_of_delivery": columns[4].text.strip(),
					"interval": columns[5].text.strip(),
					"days": columns[6].text.strip(),
					"start_time": columns[7].text.strip(), 
					"end_time": columns[8].text.strip(), 
					"section_comments": "" if len(columns[9].find_all("p")) == 0 else " ".join([p.text.strip() for p in columns[9].find_all("p")]),
					"requires_in_person": columns[10].text.strip()
				})
				prev["status"] = columns[0].text.strip()
				prev["section"] = columns[1].text.strip()
	
	# remove duplicate sections that were scraped
	seen_sections = set()
	unique_sections = []
	for section in sections:
		key = section["section"] + section["days"] + section["start_time"] + section["end_time"]
		if key not in seen_sections:
			unique_sections.append(section)
			seen_sections.add(key)

	res["sections"] = unique_sections

	return res

def get_section_info(dept: str, num: str, section: str, year: str, session: str) -> Dict:
	url = f"https://courses.students.ubc.ca/cs/courseschedule?sesscd={session}&pname=subjarea&tname=subj-section&sessyr={year}&course={num}&section={section}&dept={dept}"
	
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
	}

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")

	if soup.find(string=re.compile("The requested section is either no longer offered")) is not None:
		raise ValueError("Section not found.")

	res = {}

	res["course"] = f"{dept} {num}"
	res["section"] = section
	res["title"] = soup.find_all("h5")[0].text.strip()
	res["description"] = soup.find_all("p")[0].text.strip().replace("\r\n", "")
	res["credits"] = soup.find(string=re.compile("Credits")).split(" ")[-1]
	res["mode_of_delivery"] = soup.find(string=re.compile("Mode of Delivery")).next_element.text.strip()
	res["requires_in_person"] = soup.find(string=re.compile("Requires In-Person Attendance")).next_element.text.strip()
	res["withdraw_without_w"] = soup.find(string=re.compile("Last day to withdraw without a W standing")).next_element.text.strip()
	res["withdraw_with_w"] = soup.find(string=re.compile("Last day to withdraw with a W standing")).next_element.next_element.next_element.text.strip()
	
	instructors = []
	if soup.find("td", string=re.compile("Instructor:")):
		instructor_table = soup.find("td", string=re.compile("Instructor:")).find_parent("tr").find_parent("table")

		for row in instructor_table:
			column = row.find_all("td")
			instructors.append(column[1].text.strip())

	res["instructors"] = instructors

	seats = {}
	seats["total_remaining"] = "" if not soup.find(string=re.compile("Total Seats Remaining:")) else soup.find(string=re.compile("Total Seats Remaining:")).next_element.text.strip()
	seats["currently_registered"] = "" if not soup.find(string=re.compile("Currently Registered:")) else soup.find(string=re.compile("Currently Registered:")).next_element.text.strip()
	seats["general_remaining"] = "" if not soup.find(string=re.compile("General Seats Remaining:")) else soup.find(string=re.compile("General Seats Remaining:")).next_element.text.strip()
	seats["restricted_remaining"] = "" if not soup.find(string=re.compile("Restricted Seats Remaining")) else soup.find(string=re.compile("Restricted Seats Remaining")).next_element.text.strip()

	res["seats"] = seats

	return res