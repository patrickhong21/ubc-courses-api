# ubc-courses-api

This is a REST API built in Python with Flask to allow users to get department and course data from the [UBC SSC](https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments).

Note: Since the [https://irp.ubc.ca/workday_default_profile_changes#:~:text=On%20May%2021%2C%202024%2C%20UBC,have%20more%20than%20one%20profile.](switch to Workday), the course information now requires authentication, so this service no longer functions.

## Examples
```
Endpoint (GET): api/v1/course/info
```
will return
```
{
    "departments": [
        {
            "code": "AANB",
            "faculty": "Faculty of Land and Food Systems",
            "title": "Applied Animal Biology"
        },
        {
            "code": "ACAM",
            "faculty": "Faculty of Arts",
            "title": "Asian Canadian and Asian Migration Studies"
        },
        // ... removed to save space
    ]
}
```
---
```
Endpoint (GET): api/v1/course/info?dept=CPSC
```
will return
```
{
    "courses": [
        {
            "course": "CPSC 100",
            "title": "Computational Thinking"
        },
        {
            "course": "CPSC 103",
            "title": "Introduction to Systematic Program Design"
        },
        // ... removed to save space
    ],
    "description": "The Department of Computer Science offers several options in first year:CPSC 110 is for students pursuing Computer Science specializations or who plan to take CPSC 210. CPSC 103 targets students desiring an introduction to computing and programming, but with no plans to take further Computer Science courses. CPSC 100 targets students desiring a general introduction to computational thinking with little programming. Consult https://www.cs.ubc.ca/students/undergrad/courses/choose-your-first-course for more information. Students who have credit for or exemption from APSC 160, CPSC 107 or CPSC 110 may not take CPSC 100 or CPSC 103. Students with other computer science transfer credit must consult the department. Students currently registered in CPSC 110 or with Computer Science credit from another institution may not take APSC 160 for credit. Students with sufficient background in the concepts presented in CPSC 110 and an advisor's approval are encouraged to challenge CPSC 110 for credit by taking an examination. Additional fees are charged for some courses. For more information students are advised to contact the Department of Computer Science or visit its undergraduate website: http://www.cs.ubc.ca/students/undergrad). For information on credit exclusion between CPSC and other courses, please consult the Faculty of Science Credit Exclusion List.",
    "subject": "Computer Science",
    "subject_code": "CPSC"
}
```
---
```
Endpoint (GET): api/v1/course/info?dept=CPSC&num=213&year=2023&session=W
```
will return
```
{
    "course": "CPSC 213",
    "credits": "4",
    "description": "Software architecture, operating systems, and I/O architectures.  Relationships between application software, operating systems, and computing hardware; critical sections, deadlock avoidance, and performance; principles and operation of disks and networks.",
    "sections": [
        {
            "activity": "Lecture",
            "days": "Tue Thu",
            "end_time": "14:00",
            "interval": "",
            "mode_of_delivery": "In-Person",
            "requires_in_person": "Yes",
            "section": "CPSC 213 101",
            "section_comments": "",
            "start_time": "12:30",
            "status": "Full",
            "term": "1"
        },
        {
            "activity": "Laboratory",
            "days": "Tue",
            "end_time": "16:30",
            "interval": "",
            "mode_of_delivery": "In-Person",
            "requires_in_person": "Yes",
            "section": "CPSC 213 L1A",
            "section_comments": "",
            "start_time": "15:30",
            "status": "Full",
            "term": "1"
        },
        // ... removed to save space
    ],
    "title": "Introduction to Computer Systems"
}
```
---
```
Endpoint (GET): api/v1/course/info?dept=CPSC&num=213&section=101&year=2023&session=W
```
will return
```
{
    "course": "CPSC 213",
    "credits": "4",
    "description": "Software architecture, operating systems, and I/O architectures.  Relationships between application software, operating systems, and computing hardware; critical sections, deadlock avoidance, and performance; principles and operation of disks and networks.",
    "instructor": "JOHNSON, JORDON",
    "mode_of_delivery": "In-Person",
    "requires_in_person": "Yes",
    "seats": {
        "currently_registered": "210",
        "general_remaining": "0",
        "restricted_remaining": "0",
        "total_remaining": "0"
    },
    "section": "101",
    "title": "Introduction to Computer Systems",
    "withdraw_with_w": "October 27, 2023",
    "withdraw_without_w": "September 18, 2023"
}
```

## Uses
This would be useful, for example, to track seats in a certain section.
