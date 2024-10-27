-- Insert for question 64
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
64, 'Demographic', 'NACE', 
    'At what degree/certificate/class year are you currently enrolled?', 
    '[
    {
        "option": "Certificate Program",
        "score": 1
    },
    {
        "option": "Associates - 1st Year",
        "score": 2
    },
    {
        "option": "Associates - 2nd Year",
        "score": 3
    },
    {
        "option": "Associates 3rd Year or beyond",
        "score": 4
    },
    {
        "option": "Bachelors - 1st Year",
        "score": 5
    },
    {
        "option": "Bachelors - 2nd Year",
        "score": 6
    },
    {
        "option": "Bachelors - 3rd Year",
        "score": 7
    },
    {
        "option": "Bachelors - 4th Year",
        "score": 8
    },
    {
        "option": "Bachelors - 5th Year or beyond",
        "score": 9
    },
    {
        "option": "Masters",
        "score": 10
    },
    {
        "option": "Doctoral",
        "score": 11
    }
]': :jsonb, 
    NULL
);


-- Insert for question 66
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
66, 'Demographic', 'NACE', 
    'Gender: How do you identify?', 
    '[
    {
        "option": "Prefer not to respond",
        "score": 1
    },
    {
        "option": "Man",
        "score": 2
    },
    {
        "option": "Non-binary",
        "score": 3
    },
    {
        "option": "Woman",
        "score": 4
    }
]': :jsonb,
4.0
);

-- Insert for question 67
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
67, 'Demographic', 'NACE', 
    'Which of the following categories would you use to best describe yourself?', 
    '[
    {
        "option": "Prefer not to respond",
        "score": 1
    },
    {
        "option": "Asian",
        "score": 2
    },
    {
        "option": "Black",
        "score": 3
    },
    {
        "option": "Hispanic or Latinx",
        "score": 4
    },
    {
        "option": "International student with non-immigrant (visa) status in the U.S.",
        "score": 5
    },
    {
        "option": "Multiracial",
        "score": 6
    },
    {
        "option": "Native Hawaiian or Other Pacific Islander",
        "score": 7
    },
    {
        "option": "Native American or Native Alaskan",
        "score": 8
    },
    {
        "option": "White",
        "score": 9
    }
]',
9.0
);

-- Insert for question 68
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
68, 'Demographic', 'NACE', 
    'What is your parent(s) or caregiver(s) highest level of education in the United States?', 
    '[
    {
        "option": "Grade School",
        "score": 1
    },
    {
        "option": "High School",
        "score": 2
    },
    {
        "option": "Some College",
        "score": 3
    },
    {
        "option": "College Graduate (Associate/Bachelor''s Degree)",
        "score": 4
    },
    {
        "option": "Graduate or Professional School",
        "score": 5
    },
    {
        "option": "Unknown",
        "score": 6
    },
    {
        "option": "None of the above (College experience outside the US, etc.)",
        "score": 7
    }
]',
8.0
);
-- Insert for question 69
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
69, 'Demographic', 'NACE', 
    'Do you have a diagnosed disability?', 
    '[
    {
        "option": "Yes",
        "score": 1
    },
    {
        "option": "No",
        "score": 2
    },
    {
        "option": "Prefer not to respond",
        "score": 3
    }
]',
3.0
);

-- Insert for question 70
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
70, 'Demographic', 'NACE', 
    'Do you identify as a member of the LGBTQ+ community?', 
    '[
    {
        "option": "Yes",
        "score": 1
    },
    {
        "option": "No",
        "score": 2
    },
    {
        "option": "Prefer not to respond",
        "score": 3
    }
]',
3.0
);

-- Insert for question 71
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
71, 'Demographic', 'NACE', 
    'Is English the primary language spoken at your childhood home?', 
    '[
    {
        "option": "Yes",
        "score": 1
    },
    {
        "option": "No",
        "score": 2
    },
    {
        "option": "Prefer not to respond",
        "score": 3
    }
]',
3.0
);

-- Insert for question 72
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
72, 'Demographic', 'NACE', 
    'Are you a parent to a child under 18 years old?', 
    '[
    {
        "option": "Yes",
        "score": 1
    },
    {
        "option": "No",
        "score": 2
    },
    {
        "option": "Prefer not to respond",
        "score": 3
    }
]',
3.0
);
--not in the list
-- Insert for question 73
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
73, 'Demographic', 'NACE', 
    'Have you ever served on active duty in the U.S. Armed Forces, Reserves, or National Guard?', 
    '[
    {
        "option": "Prefer not to respond",
        "score": 1
    },
    {
        "option": "Never served in the military",
        "score": 2
    },
    {
        "option": "Only on active duty for training in the Reserves or National Guard",
        "score": 3
    },
    {
        "option": "Now on active duty",
        "score": 4
    },
    {
        "option": "On active duty in the past, but not now",
        "score": 5
    }
]': :jsonb,
5.0
);

INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
74, 'Demographic', 'NACE', 
    'Are you the primary caregiver to a family member (not a child) such as a parent, partner, etc.?', 
    '[
    {
        "option": "Yes",
        "score": 1
    },
    {
        "option": "No",
        "score": 2
    },
    {
        "option": "Prefer not to respond",
        "score": 3
    }
]': :jsonb,
3.0
);
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
75, 'Demographic', 'NACE', 
    'Which of the following sources did you use to finance your college tuition? (Optional)  Select all that apply:', 
    '[
    {
        "option": "Federal Student Loans",
        "score": 1
    },
    {
        "option": "Private Student Loans",
        "score": 1
    },
    {
        "option": "Family / Personal Money",
        "score": 1
    },
    {
        "option": "Merit-based Scholarships and Grants",
        "score": 1
    },
    {
        "option": "Income-based Scholarships and Grants",
        "score": 1
    },
    {
        "option": "Pell Grants",
        "score": 1
    },
    {
        "option": "My Own Employment",
        "score": 1
    },
    {
        "option": "529 Investment Account",
        "score": 1
    },
    {
        "option": "Tuition waivers or reductions due to family or yourself being employed at the college",
        "score": 1
    },
    {
        "option": "Other",
        "score": 1
    }
]': :jsonb,
10.0
);

-- Insert for question 65
INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
65, 'Demographic', 'NACE', 
    'Which of the following best represent your program or area of study?', 
    '[
    {
        "option": "Agriculture, General",
        "score": 1
    },
    {
        "option": "Agricultural Business and Management",
        "score": 1.01
    },
    {
        "option": "Agricultural Mechanization",
        "score": 1.02
    },
    {
        "option": "Agricultural Production Operations",
        "score": 1.03
    },
    {
        "option": "Agricultural and Food Products Processing",
        "score": 1.04
    },
    {
        "option": "Agricultural and Domestic Animal Services",
        "score": 1.05
    },
    {
        "option": "Applied Horticulture and Horticultural Business Services",
        "score": 1.06
    },
    {
        "option": "International Agriculture",
        "score": 1.07
    },
    {
        "option": "Agricultural Public Services",
        "score": 1.08
    },
    {
        "option": "Animal Sciences",
        "score": 1.09
    },
    {
        "option": "Food Science and Technology",
        "score": 1.1
    },
    {
        "option": "Plant Sciences",
        "score": 1.11
    },
    {
        "option": "Soil Sciences",
        "score": 1.12
    },
    {
        "option": "Agriculture, Agriculture Operations, and Related Sciences, Other",
        "score": 1.99
    },
    {
        "option": "Natural Resources Conservation and Research",
        "score": 3.01
    },
    {
        "option": "Natural Resources Management and Policy",
        "score": 3.02
    },
    {
        "option": "Fishing and Fisheries Sciences and Management",
        "score": 3.03
    },
    {
        "option": "Forestry",
        "score": 3.05
    },
    {
        "option": "Wildlife and Wildlands Science and Management",
        "score": 3.06
    },
    {
        "option": "Natural Resources and Conservation, Other",
        "score": 3.99
    },
    {
        "option": "Architecture",
        "score": 4.02
    },
    {
        "option": "City/Urban, Community and Regional Planning",
        "score": 4.03
    },
    {
        "option": "Environmental Design",
        "score": 4.04
    },
    {
        "option": "Interior Architecture",
        "score": 4.05
    },
    {
        "option": "Landscape Architecture",
        "score": 4.06
    },
    {
        "option": "Architectural History and Criticism",
        "score": 4.08
    },
    {
        "option": "Architectural Sciences and Technology",
        "score": 4.09
    },
    {
        "option": "Real Estate Development",
        "score": 4.1
    },
    {
        "option": "Architecture and Related Services, Other",
        "score": 4.99
    },
    {
        "option": "Area Studies",
        "score": 5.01
    },
    {
        "option": "Ethnic, Cultural Minority, Gender, and Group Studies",
        "score": 5.02
    },
    {
        "option": "Communication and Media Studies",
        "score": 9.01
    },
    {
        "option": "Journalism",
        "score": 9.04
    },
    {
        "option": "Radio, Television, and Digital Communication",
        "score": 9.07
    },
    {
        "option": "Public Relations, Advertising, and Applied Communication",
        "score": 9.09
    },
    {
        "option": "Publishing",
        "score": 9.1
    },
    {
        "option": "Communication, Journalism, and Related Programs, Other",
        "score": 9.99
    },
    {
        "option": "Communications Technology/Technician",
        "score": 10.01
    },
    {
        "option": "Audiovisual Communications Technologies/Technicians",
        "score": 10.02
    },
    {
        "option": "Graphic Communications",
        "score": 10.03
    },
    {
        "option": "Communications Technologies/Technicians and Support Services, Other",
        "score": 10.99
    },
    {
        "option": "Computer and Information Sciences, General",
        "score": 11.01
    },
    {
        "option": "Computer Programming",
        "score": 11.02
    },
    {
        "option": "Data Processing",
        "score": 11.03
    },
    {
        "option": "Information Science/Studies",
        "score": 11.04
    },
    {
        "option": "Computer Systems Analysis",
        "score": 11.05
    },
    {
        "option": "Data Entry/Microcomputer Applications",
        "score": 11.06
    },
    {
        "option": "Computer Science",
        "score": 11.07
    },
    {
        "option": "Computer Software and Media Applications",
        "score": 11.08
    },
    {
        "option": "Computer Systems Networking and Telecommunications",
        "score": 11.09
    },
    {
        "option": "Computer/Information Technology Administration and Management",
        "score": 11.1
    },
    {
        "option": "Computer and Information Sciences and Support Services, Other",
        "score": 11.99
    },
    {
        "option": "Computer Programming",
        "score": 11.02
    },
    {
        "option": "Data Processing",
        "score": 11.03
    },
    {
        "option": "Information Science/Studies",
        "score": 11.04
    },
    {
        "option": "Computer Systems Analysis",
        "score": 11.05
    },
    {
        "option": "Data Entry/Microcomputer Applications",
        "score": 11.06
    },
    {
        "option": "Computer Science",
        "score": 11.07
    },
    {
        "option": "Computer Software and Media Applications",
        "score": 11.08
    },
    {
        "option": "Computer Systems Networking and Telecommunications",
        "score": 11.09
    },
    {
        "option": "Computer/Information Technology Administration and Management",
        "score": 11.1
    },
    {
        "option": "Computer and Information Sciences and Support Services, Other",
        "score": 11.99
    },
    {
        "option": "Funeral Service and Mortuary Science",
        "score": 12.03
    },
    {
        "option": "Cosmetology and Related Personal Grooming Services",
        "score": 12.04
    },
    {
        "option": "Culinary Arts and Related Services",
        "score": 12.05
    },
    {
        "option": "Personal and Culinary Services, Other",
        "score": 12.99
    },
    {
        "option": "Education, General",
        "score": 13.01
    },
    {
        "option": "Bilingual, Multilingual, and Multicultural Education",
        "score": 13.02
    },
    {
        "option": "Curriculum and Instruction",
        "score": 13.03
    },
    {
        "option": "Educational Administration and Supervision",
        "score": 13.04
    },
    {
        "option": "Educational/Instructional Media Design",
        "score": 13.05
    },
    {
        "option": "Educational Assessment, Evaluation, and Research",
        "score": 13.06
    },
    {
        "option": "International and Comparative Education",
        "score": 13.07
    },
    {
        "option": "Social and Philosophical Foundations of Education",
        "score": 13.09
    },
    {
        "option": "Special Education and Teaching",
        "score": 13.1
    },
    {
        "option": "Student Counseling and Personnel Services",
        "score": 13.11
    },
    {
        "option": "Teacher Education and Professional Development, Specific Levels and Methods",
        "score": 13.12
    },
    {
        "option": "Teacher Education and Professional Development, Specific Subject Areas",
        "score": 13.13
    },
    {
        "option": "Teaching English or French as a Second or Foreign Language",
        "score": 13.14
    },
    {
        "option": "Teaching Assistants/Aides",
        "score": 13.15
    },
    {
        "option": "Education, Other",
        "score": 13.99
    },
    {
        "option": "Engineering, General",
        "score": 14.01
    },
    {
        "option": "Aerospace, Aeronautical and Astronautical Engineering",
        "score": 14.02
    },
    {
        "option": "Agricultural Engineering",
        "score": 14.03
    },
    {
        "option": "Architectural Engineering",
        "score": 14.04
    },
    {
        "option": "Biomedical/Medical Engineering",
        "score": 14.05
    },
    {
        "option": "Ceramic Sciences and Engineering",
        "score": 14.06
    },
    {
        "option": "Chemical Engineering",
        "score": 14.07
    },
    {
        "option": "Civil Engineering",
        "score": 14.08
    },
    {
        "option": "Computer Engineering",
        "score": 14.09
    },
    {
        "option": "Electrical, Electronics and Communications Engineering",
        "score": 14.1
    },
    {
        "option": "Engineering Mechanics",
        "score": 14.11
    },
    {
        "option": "Engineering Physics",
        "score": 14.12
    },
    {
        "option": "Engineering Science",
        "score": 14.13
    },
    {
        "option": "Environmental/Environmental Health Engineering",
        "score": 14.14
    },
    {
        "option": "Materials Engineering",
        "score": 14.18
    },
    {
        "option": "Mechanical Engineering",
        "score": 14.19
    },
    {
        "option": "Metallurgical Engineering",
        "score": 14.2
    },
    {
        "option": "Mining and Mineral Engineering",
        "score": 14.21
    },
    {
        "option": "Naval Architecture and Marine Engineering",
        "score": 14.22
    },
    {
        "option": "Nuclear Engineering",
        "score": 14.23
    },
    {
        "option": "Ocean Engineering",
        "score": 14.24
    },
    {
        "option": "Petroleum Engineering",
        "score": 14.25
    },
    {
        "option": "Systems Engineering",
        "score": 14.27
    },
    {
        "option": "Textile Sciences and Engineering",
        "score": 14.28
    },
    {
        "option": "Polymer/Plastics Engineering",
        "score": 14.32
    },
    {
        "option": "Construction Engineering",
        "score": 14.33
    },
    {
        "option": "Forest Engineering",
        "score": 14.34
    },
    {
        "option": "Industrial Engineering",
        "score": 14.35
    },
    {
        "option": "Manufacturing Engineering",
        "score": 14.36
    },
    {
        "option": "Operations Research",
        "score": 14.37
    },
    {
        "option": "Surveying Engineering",
        "score": 14.38
    },
    {
        "option": "Geological/Geophysical Engineering",
        "score": 14.39
    },
    {
        "option": "Paper Science and Engineering",
        "score": 14.4
    },
    {
        "option": "Electromechanical Engineering",
        "score": 14.41
    },
    {
        "option": "Mechatronics, Robotics, and Automation Engineering",
        "score": 14.42
    },
    {
        "option": "Biochemical Engineering",
        "score": 14.43
    },
    {
        "option": "Engineering Chemistry",
        "score": 14.44
    },
    {
        "option": "Biological/Biosystems Engineering",
        "score": 14.45
    },
    {
        "option": "Engineering, Other",
        "score": 14.99
    },
    {
        "option": "Engineering Technology, General",
        "score": 15
    },
    {
        "option": "Architectural Engineering Technologies/Technicians",
        "score": 15.01
    },
    {
        "option": "Civil Engineering Technologies/Technicians",
        "score": 15.02
    },
    {
        "option": "Electrical Engineering Technologies/Technicians",
        "score": 15.03
    },
    {
        "option": "Electromechanical Instrumentation and Maintenance Technologies/Technicians",
        "score": 15.04
    },
    {
        "option": "Environmental Control Technologies/Technicians",
        "score": 15.05
    },
    {
        "option": "Industrial Production Technologies/Technicians",
        "score": 15.06
    },
    {
        "option": "Quality Control and Safety Technologies/Technicians",
        "score": 15.07
    },
    {
        "option": "Mechanical Engineering Related Technologies/Technicians",
        "score": 15.08
    },
    {
        "option": "Mining and Petroleum Technologies/Technicians",
        "score": 15.09
    },
    {
        "option": "Construction Engineering Technologies",
        "score": 15.1
    },
    {
        "option": "Engineering-Related Technologies",
        "score": 15.11
    },
    {
        "option": "Computer Engineering Technologies/Technicians",
        "score": 15.12
    },
    {
        "option": "Drafting/Design Engineering Technologies/Technicians",
        "score": 15.13
    },
    {
        "option": "Nuclear Engineering Technologies/Technicians",
        "score": 15.14
    },
    {
        "option": "Engineering-Related Fields",
        "score": 15.15
    },
    {
        "option": "Nanotechnology",
        "score": 15.16
    },
    {
        "option": "Engineering Technologies/Technicians, Other",
        "score": 15.99
    },
    {
        "option": "Linguistic, Comparative, and Related Language Studies and Services",
        "score": 16.01
    },
    {
        "option": "African Languages, Literatures, and Linguistics",
        "score": 16.02
    },
    {
        "option": "East Asian Languages, Literatures, and Linguistics",
        "score": 16.03
    },
    {
        "option": "Slavic, Baltic and Albanian Languages, Literatures, and Linguistics",
        "score": 16.04
    },
    {
        "option": "Germanic Languages, Literatures, and Linguistics",
        "score": 16.05
    },
    {
        "option": "Modern Greek Language and Literature",
        "score": 16.06
    },
    {
        "option": "South Asian Languages, Literatures, and Linguistics",
        "score": 16.07
    },
    {
        "option": "Iranian/Persian Languages, Literatures, and Linguistics",
        "score": 16.08
    },
    {
        "option": "Romance Languages, Literatures, and Linguistics",
        "score": 16.09
    },
    {
        "option": "American Indian/Native American Languages, Literatures, and Linguistics",
        "score": 16.1
    },
    {
        "option": "Middle/Near Eastern and Semitic Languages, Literatures, and Linguistics",
        "score": 16.11
    },
    {
        "option": "Classics and Classical Languages, Literatures, and Linguistics",
        "score": 16.12
    },
    {
        "option": "Celtic Languages, Literatures, and Linguistics",
        "score": 16.13
    },
    {
        "option": "Southeast Asian and Australasian/Pacific Languages, Literatures, and Linguistics",
        "score": 16.14
    },
    {
        "option": "Turkic, Uralic-Altaic, Caucasian, and Central Asian Languages, Literatures, and Linguistics",
        "score": 16.15
    },
    {
        "option": "American Sign Language",
        "score": 16.16
    },
    {
        "option": "Foreign Languages, Literatures, and Linguistics, Other",
        "score": 16.99
    },
    {
        "option": "Work and Family Studies",
        "score": 19
    },
    {
        "option": "Family and Consumer Sciences/Human Sciences, General",
        "score": 19.01
    },
    {
        "option": "Family and Consumer Sciences/Human Sciences Business Services",
        "score": 19.02
    },
    {
        "option": "Family and Consumer Economics and Related Studies",
        "score": 19.04
    },
    {
        "option": "Foods, Nutrition, and Related Services",
        "score": 19.05
    },
    {
        "option": "Housing and Human Environments",
        "score": 19.06
    },
    {
        "option": "Human Development, Family Studies, and Related Services",
        "score": 19.07
    },
    {
        "option": "Apparel and Textiles",
        "score": 19.09
    },
    {
        "option": "Family and Consumer Sciences/Human Sciences, Other",
        "score": 19.99
    },
    {
        "option": "Non-Professional General Legal Studies (Undergraduate)",
        "score": 22
    },
    {
        "option": "Law",
        "score": 22.01
    },
    {
        "option": "Legal Research and Advanced Professional Studies",
        "score": 22.02
    },
    {
        "option": "Legal Support Services",
        "score": 22.03
    },
    {
        "option": "Legal Professions and Studies, Other",
        "score": 22.99
    },
    {
        "option": "English Language and Literature, General",
        "score": 23.01
    },
    {
        "option": "Rhetoric and Composition/Writing Studies",
        "score": 23.13
    },
    {
        "option": "Literature",
        "score": 23.14
    },
    {
        "option": "English Language and Literature/Letters, Other",
        "score": 23.99
    },
    {
        "option": "Liberal Arts and Sciences, General Studies and Humanities",
        "score": 24.01
    },
    {
        "option": "Library Science and Administration",
        "score": 25.01
    },
    {
        "option": "Library and Archives Assisting",
        "score": 25.03
    },
    {
        "option": "Library Science, Other",
        "score": 25.99
    },
    {
        "option": "Biology, General",
        "score": 26.01
    },
    {
        "option": "Biochemistry, Biophysics and Molecular Biology",
        "score": 26.02
    },
    {
        "option": "Botany/Plant Biology",
        "score": 26.03
    },
    {
        "option": "Cell/Cellular Biology and Anatomical Sciences",
        "score": 26.04
    },
    {
        "option": "Microbiological Sciences and Immunology",
        "score": 26.05
    },
    {
        "option": "Zoology/Animal Biology",
        "score": 26.07
    },
    {
        "option": "Genetics",
        "score": 26.08
    },
    {
        "option": "Physiology, Pathology and Related Sciences",
        "score": 26.09
    },
    {
        "option": "Pharmacology and Toxicology",
        "score": 26.1
    },
    {
        "option": "Biomathematics, Bioinformatics, and Computational Biology",
        "score": 26.11
    },
    {
        "option": "Biotechnology",
        "score": 26.12
    },
    {
        "option": "Ecology, Evolution, Systematics, and Population Biology",
        "score": 26.13
    },
    {
        "option": "Molecular Medicine",
        "score": 26.14
    },
    {
        "option": "Neurobiology and Neurosciences",
        "score": 26.15
    },
    {
        "option": "Biological and Biomedical Sciences, Other",
        "score": 26.99
    },
    {
        "option": "Mathematics",
        "score": 27.01
    },
    {
        "option": "Applied Mathematics",
        "score": 27.03
    },
    {
        "option": "Statistics",
        "score": 27.05
    },
    {
        "option": "Mathematics and Statistics, Other",
        "score": 27.99
    },
    {
        "option": "Air Force ROTC, Air Science and Operations",
        "score": 28.01
    },
    {
        "option": "Army ROTC, Military Science and Operations",
        "score": 28.03
    },
    {
        "option": "Navy/Marine ROTC, Naval Science and Operations",
        "score": 28.04
    },
    {
        "option": "Military Science and Operational Studies",
        "score": 28.05
    },
    {
        "option": "Security Policy and Strategy",
        "score": 28.06
    },
    {
        "option": "Military Economics and Management",
        "score": 28.07
    },
    {
        "option": "Military Science, Leadership and Operational Art, Other",
        "score": 28.99
    },
    {
        "option": "Intelligence, Command Control and Information Operations",
        "score": 29.02
    },
    {
        "option": "Military Applied Sciences",
        "score": 29.03
    },
    {
        "option": "Military Systems and Maintenance Technology",
        "score": 29.04
    },
    {
        "option": "Military Technologies and Applied Sciences, Other",
        "score": 29.99
    },
    {
        "option": "Multi-/Interdisciplinary Studies, General",
        "score": 30
    },
    {
        "option": "Biological and Physical Sciences",
        "score": 30.01
    },
    {
        "option": "Peace Studies and Conflict Resolution",
        "score": 30.05
    },
    {
        "option": "Systems Science and Theory",
        "score": 30.06
    },
    {
        "option": "Mathematics and Computer Science",
        "score": 30.08
    },
    {
        "option": "Biopsychology",
        "score": 30.1
    },
    {
        "option": "Gerontology",
        "score": 30.11
    },
    {
        "option": "Historic Preservation and Conservation",
        "score": 30.12
    },
    {
        "option": "Medieval and Renaissance Studies",
        "score": 30.13
    },
    {
        "option": "Museology/Museum Studies",
        "score": 30.14
    },
    {
        "option": "Science, Technology and Society",
        "score": 30.15
    },
    {
        "option": "Accounting and Computer Science",
        "score": 30.16
    },
    {
        "option": "Behavioral Sciences",
        "score": 30.17
    },
    {
        "option": "Natural Sciences",
        "score": 30.18
    },
    {
        "option": "Nutrition Sciences",
        "score": 30.19
    },
    {
        "option": "International/Global Studies",
        "score": 30.2
    },
    {
        "option": "Holocaust and Related Studies",
        "score": 30.21
    },
    {
        "option": "Classical and Ancient Studies",
        "score": 30.22
    },
    {
        "option": "Intercultural/Multicultural and Diversity Studies",
        "score": 30.23
    },
    {
        "option": "Cognitive Science",
        "score": 30.25
    },
    {
        "option": "Cultural Studies/Critical Theory and Analysis",
        "score": 30.26
    },
    {
        "option": "Human Biology",
        "score": 30.27
    },
    {
        "option": "Dispute Resolution",
        "score": 30.28
    },
    {
        "option": "Maritime Studies",
        "score": 30.29
    },
    {
        "option": "Computational Science",
        "score": 30.3
    },
    {
        "option": "Human Computer Interaction",
        "score": 30.31
    },
    {
        "option": "Marine Sciences",
        "score": 30.32
    },
    {
        "option": "Sustainability Studies",
        "score": 30.33
    },
    {
        "option": "Anthrozoology",
        "score": 30.34
    },
    {
        "option": "Climate Science",
        "score": 30.35
    },
    {
        "option": "Cultural Studies and Comparative Literature",
        "score": 30.36
    },
    {
        "option": "Design for Human Health",
        "score": 30.37
    },
    {
        "option": "Earth Systems Science",
        "score": 30.38
    },
    {
        "option": "Economics and Computer Science",
        "score": 30.39
    },
    {
        "option": "Economics and Foreign Language/Literature",
        "score": 30.4
    },
    {
        "option": "Environmental Geosciences",
        "score": 30.41
    },
    {
        "option": "Geoarcheaology",
        "score": 30.42
    },
    {
        "option": "Geobiology",
        "score": 30.43
    },
    {
        "option": "Geography and Environmental Studies",
        "score": 30.44
    },
    {
        "option": "History and Language/Literature",
        "score": 30.45
    },
    {
        "option": "History and Political Science",
        "score": 30.46
    },
    {
        "option": "Linguistics and Anthropology",
        "score": 30.47
    },
    {
        "option": "Linguistics and Computer Science",
        "score": 30.48
    },
    {
        "option": "Mathematical Economics",
        "score": 30.49
    },
    {
        "option": "Mathematics and Atmospheric/Oceanic Science",
        "score": 30.5
    },
    {
        "option": "Philosophy, Politics, and Economics",
        "score": 30.51
    },
    {
        "option": "Digital Humanities and Textual Studies",
        "score": 30.52
    },
    {
        "option": "Thanatology",
        "score": 30.53
    },
    {
        "option": "Data Science",
        "score": 30.7
    },
    {
        "option": "Data Analytics",
        "score": 30.71
    },
    {
        "option": "Multi/Interdisciplinary Studies, Other",
        "score": 30.99
    },
    {
        "option": "Parks, Recreation and Leisure Studies",
        "score": 31.01
    },
    {
        "option": "Parks, Recreation and Leisure Facilities Management",
        "score": 31.03
    },
    {
        "option": "Health and Physical Education/Fitness",
        "score": 31.05
    },
    {
        "option": "Outdoor Education",
        "score": 31.06
    },
    {
        "option": "Parks, Recreation, Leisure, and Fitness Studies, Other",
        "score": 31.99
    },
    {
        "option": "Basic Skills and Developmental/Remedial Education",
        "score": 32.01
    },
    {
        "option": "Citizenship Activities",
        "score": 33.01
    },
    {
        "option": "Health-Related Knowledge and Skills",
        "score": 34.01
    },
    {
        "option": "Interpersonal and Social Skills",
        "score": 35.01
    },
    {
        "option": "Leisure and Recreational Activities",
        "score": 36.01
    },
    {
        "option": "Personal Awareness and Self-Improvement",
        "score": 37.01
    },
    {
        "option": "Philosophy and Religious Studies, General",
        "score": 38
    },
    {
        "option": "Philosophy",
        "score": 38.01
    },
    {
        "option": "Religion/Religious Studies",
        "score": 38.02
    },
    {
        "option": "Philosophy and Religious Studies, Other",
        "score": 38.99
    },
    {
        "option": "Bible/Biblical Studies",
        "score": 39.02
    },
    {
        "option": "Missions/Missionary Studies and Missiology",
        "score": 39.03
    },
    {
        "option": "Religious Education",
        "score": 39.04
    },
    {
        "option": "Religious/Sacred Music",
        "score": 39.05
    },
    {
        "option": "Theological and Ministerial Studies",
        "score": 39.06
    },
    {
        "option": "Pastoral Counseling and Specialized Ministries",
        "score": 39.07
    },
    {
        "option": "Theology and Religious Vocations, Other",
        "score": 39.99
    },
    {
        "option": "Physical Sciences",
        "score": 40.01
    },
    {
        "option": "Astronomy and Astrophysics",
        "score": 40.02
    },
    {
        "option": "Atmospheric Sciences and Meteorology",
        "score": 40.04
    },
    {
        "option": "Chemistry",
        "score": 40.05
    },
    {
        "option": "Geological and Earth Sciences/Geosciences",
        "score": 40.06
    },
    {
        "option": "Physics",
        "score": 40.08
    },
    {
        "option": "Materials Sciences",
        "score": 40.10
    },
    {
        "option": "Physical Sciences, Other",
        "score": 40.99
    },
    {
        "option": "Science Technologies/Technicians, General",
        "score": 41
    },
    {
        "option": "Biology Technician/Biotechnology Laboratory Technician",
        "score": 41.01
    },
    {
        "option": "Nuclear and Industrial Radiologic Technologies/Technicians",
        "score": 41.02
    },
    {
        "option": "Physical Science Technologies/Technicians",
        "score": 41.03
    },
    {
        "option": "Science Technologies/Technicians, Other",
        "score": 41.99
    },
    {
        "option": "Psychology, General",
        "score": 42.01
    },
    {
        "option": "Research and Experimental Psychology",
        "score": 42.27
    },
    {
        "option": "Clinical, Counseling and Applied Psychology",
        "score": 42.28
    },
    {
        "option": "Psychology, Other",
        "score": 42.99
    },
    {
        "option": "Criminal Justice and Corrections",
        "score": 43.01
    },
    {
        "option": "Fire Protection",
        "score": 43.02
    },
    {
        "option": "Homeland Security",
        "score": 43.03
    },
    {
        "option": "Homeland Security, Law Enforcement, Firefighting and Related Protective Services, Other",
        "score": 43.99
    },
    {
        "option": "Human Services, General",
        "score": 44
    },
    {
        "option": "Community Organization and Advocacy",
        "score": 44.02
    },
    {
        "option": "Public Administration",
        "score": 44.04
    },
    {
        "option": "Public Policy Analysis",
        "score": 44.05
    },
    {
        "option": "Social Work",
        "score": 44.07
    },
    {
        "option": "Public Administration and Social Service Professions, Other",
        "score": 44.99
    },
    {
        "option": "Social Sciences, General",
        "score": 45.01
    },
    {
        "option": "Anthropology",
        "score": 45.02
    },
    {
        "option": "Archeology",
        "score": 45.03
    },
    {
        "option": "Criminology",
        "score": 45.04
    },
    {
        "option": "Demography and Population Studies",
        "score": 45.05
    },
    {
        "option": "Economics",
        "score": 45.06
    },
    {
        "option": "Geography and Cartography",
        "score": 45.07
    },
    {
        "option": "International Relations and National Security Studies",
        "score": 45.09
    },
    {
        "option": "Political Science and Government",
        "score": 45.10
    },
    {
        "option": "Sociology",
        "score": 45.11
    },
    {
        "option": "Urban Studies/Affairs",
        "score": 45.12
    },
    {
        "option": "Sociology and Anthropology",
        "score": 45.13
    },
    {
        "option": "Rural Sociology",
        "score": 45.14
    },
    {
        "option": "Social Sciences, Other",
        "score": 45.99
    },
    {
        "option": "Construction Trades, General",
        "score": 46
    },
    {
        "option": "Mason/Masonry",
        "score": 46.01
    },
    {
        "option": "Carpenters",
        "score": 46.02
    },
    {
        "option": "Electrical and Power Transmission Installers",
        "score": 46.03
    },
    {
        "option": "Building/Construction Finishing, Management, and Inspection",
        "score": 46.04
    },
    {
        "option": "Plumbing and Related Water Supply Services",
        "score": 46.05
    },
    {
        "option": "Construction Trades, Other",
        "score": 46.99
    },
    {
        "option": "Mechanics and Repairers, General",
        "score": 47
    },
    {
        "option": "Electrical/Electronics Maintenance and Repair Technology",
        "score": 47.01
    },
    {
        "option": "Heating, Air Conditioning, Ventilation and Refrigeration Maintenance Technology/Technician (HAC, HACR, HVAC, HVACR)",
        "score": 47.02
    },
    {
        "option": "Heavy/Industrial Equipment Maintenance Technologies",
        "score": 47.03
    },
    {
        "option": "Precision Systems Maintenance and Repair Technologies",
        "score": 47.04
    },
    {
        "option": "Vehicle Maintenance and Repair Technologies",
        "score": 47.06
    },
    {
        "option": "Mechanic and Repair Technologies/Technicians, Other",
        "score": 47.99
    },
    {
        "option": "Precision Production Trades, General",
        "score": 48
    },
    {
        "option": "Leatherworking and Upholstery",
        "score": 48.03
    },
    {
        "option": "Precision Metal Working",
        "score": 48.05
    },
    {
        "option": "Woodworking",
        "score": 48.07
    },
    {
        "option": "Boilermaking/Boilermaker",
        "score": 48.08
    },
    {
        "option": "Precision Production, Other",
        "score": 48.99
    },
    {
        "option": "Air Transportation",
        "score": 49.01
    },
    {
        "option": "Ground Transportation",
        "score": 49.02
    },
    {
        "option": "Marine Transportation",
        "score": 49.03
    },
    {
        "option": "Transportation and Materials Moving, Other",
        "score": 49.99
    },
    {
        "option": "Visual and Performing Arts, General",
        "score": 50.01
    },
    {
        "option": "Crafts/Craft Design, Folk Art and Artisanry",
        "score": 50.02
    },
    {
        "option": "Dance",
        "score": 50.03
    },
    {
        "option": "Design and Applied Arts",
        "score": 50.04
    },
    {
        "option": "Drama/Theatre Arts and Stagecraft",
        "score": 50.05
    },
    {
        "option": "Film/Video and Photographic Arts",
        "score": 50.06
    },
    {
        "option": "Fine and Studio Arts",
        "score": 50.07
    },
    {
        "option": "Music",
        "score": 50.09
    },
    {
        "option": "Arts, Entertainment,and Media Management",
        "score": 50.10
    },
    {
        "option": "Visual and Performing Arts, Other",
        "score": 50.99
    },
    {
        "option": "Health Services/Allied Health/Health Sciences, General",
        "score": 51
    },
    {
        "option": "Chiropractic",
        "score": 51.01
    },
    {
        "option": "Communication Disorders Sciences and Services",
        "score": 51.02
    },
    {
        "option": "Dentistry",
        "score": 51.04
    },
    {
        "option": "Advanced/Graduate Dentistry and Oral Sciences",
        "score": 51.05
    },
    {
        "option": "Dental Support Services and Allied Professions",
        "score": 51.06
    },
    {
        "option": "Health and Medical Administrative Services",
        "score": 51.07
    },
    {
        "option": "Allied Health and Medical Assisting Services",
        "score": 51.08
    },
    {
        "option": "Allied Health Diagnostic, Intervention, and Treatment Professions",
        "score": 51.09
    },
    {
        "option": "Clinical/Medical Laboratory Science/Research and Allied Professions",
        "score": 51.10
    },
    {
        "option": "Health/Medical Preparatory Programs",
        "score": 51.11
    },
    {
        "option": "Medicine",
        "score": 51.12
    },
    {
        "option": "Medical Clinical Sciences/Graduate Medical Studies",
        "score": 51.14
    },
    {
        "option": "Mental and Social Health Services and Allied Professions",
        "score": 51.15
    },
    {
        "option": "Optometry",
        "score": 51.17
    },
    {
        "option": "Ophthalmic and Optometric Support Services and Allied Professions",
        "score": 51.18
    },
    {
        "option": "Osteopathic Medicine/Osteopathy",
        "score": 51.19
    },
    {
        "option": "Pharmacy, Pharmaceutical Sciences, and Administration",
        "score": 51.20
    },
    {
        "option": "Podiatric Medicine/Podiatry",
        "score": 51.21
    },
    {
        "option": "Public Health",
        "score": 51.22
    },
    {
        "option": "Rehabilitation and Therapeutic Professions",
        "score": 51.23
    },
    {
        "option": "Veterinary Medicine",
        "score": 51.24
    },
    {
        "option": "Veterinary Biomedical and Clinical Sciences",
        "score": 51.25
    },
    {
        "option": "Health Aides/Attendants/Orderlies",
        "score": 51.26
    },
    {
        "option": "Medical Illustration and Informatics",
        "score": 51.27
    },
    {
        "option": "Dietetics and Clinical Nutrition Services",
        "score": 51.31
    },
    {
        "option": "Bioethics/Medical Ethics",
        "score": 51.32
    },
    {
        "option": "Alternative and Complementary Medicine and Medical Systems",
        "score": 51.33
    },
    {
        "option": "Alternative and Complementary Medical Support Services",
        "score": 51.34
    },
    {
        "option": "Somatic Bodywork and Related Therapeutic Services",
        "score": 51.35
    },
    {
        "option": "Movement and Mind-Body Therapies and Education",
        "score": 51.36
    },
    {
        "option": "Energy and Biologically Based Therapies",
        "score": 51.37
    },
    {
        "option": "Registered Nursing, Nursing Administration, Nursing Research and Clinical Nursing",
        "score": 51.38
    },
    {
        "option": "Practical Nursing, Vocational Nursing and Nursing Assistants",
        "score": 51.39
    },
    {
        "option": "Business/Commerce, General",
        "score": 52.01
    },
    {
        "option": "Business Administration, Management and Operations",
        "score": 52.02
    },
    {
        "option": "Accounting and Related Services",
        "score": 52.03
    },
    {
        "option": "Business Operations Support and Assistant Services",
        "score": 52.04
    },
    {
        "option": "Business/Corporate Communications",
        "score": 52.05
    },
    {
        "option": "Business/Managerial Economics",
        "score": 52.06
    },
    {
        "option": "Entrepreneurial and Small Business Operations",
        "score": 52.07
    },
    {
        "option": "Finance and Financial Management Services",
        "score": 52.08
    },
    {
        "option": "Hospitality Administration/Management",
        "score": 52.09
    },
    {
        "option": "Human Resources Management and Services",
        "score": 52.10
    },
    {
        "option": "International Business",
        "score": 52.11
    },
    {
        "option": "Management Information Systems and Services",
        "score": 52.12
    },
    {
        "option": "Management Sciences and Quantitative Methods",
        "score": 52.13
    },
    {
        "option": "Marketing",
        "score": 52.14
    },
    {
        "option": "Real Estate",
        "score": 52.15
    },
    {
        "option": "Taxation",
        "score": 52.16
    },
    {
        "option": "Insurance",
        "score": 52.17
    },
    {
        "option": "General Sales, Merchandising and Related Marketing Operations",
        "score": 52.18
    },
    {
        "option": "Specialized Sales, Merchandising and Marketing Operations",
        "score": 52.19
    },
    {
        "option": "Construction Management",
        "score": 52.20
    },
    {
        "option": "Telecommunications Management",
        "score": 52.21
    },
    {
        "option": "Business, Management, Marketing, and Related Support Services, Other",
        "score": 52.99
    },
    {
        "option": "High School/Secondary Diploma Programs",
        "score": 53.01
    },
    {
        "option": "High School/Secondary Certificate Programs",
        "score": 53.02
    },
    {
        "option": "History",
        "score": 54.01
    },
    {
        "option": "Dental Residency Programs",
        "score": 60.01
    },
    {
        "option": "Veterinary Residency Programs",
        "score": 60.03
    },
    {
        "option": "Medical Residency Programs - General Certificates",
        "score": 60.04
    },
    {
        "option": "Medical Residency Programs - Subspecialty Certificates",
        "score": 60.05
    },
    {
        "option": "Podiatric Medicine Residency Programs",
        "score": 60.06
    }
]', 
    NULL
);



INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
VALUES 
(uuid_generate_v4(), '{
    "students"
}',
76, 'Demographic', 'NACE', 
    'What is your age? (Optional)', 
    '[]',
    NULL
);

-- Social Capital

    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options, score_total)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
37, 
        'Social Capital', 
        'PLUS', 
        'I have relationships with former employers and teachers/professors who would be willing to give me a formal recommendation if/when needed.', 
        '[
    {
        "question": "Employers (Choose Below)",
        "options": [
            {
                "option": "Not yet",
                "score": 0
            },
            {
                "option": "1 Relationship",
                "score": 1
            },
            {
                "option": "2 Relationships",
                "score": 2
            },
            {
                "option": "3 or more Relationships",
                "score": 3
            }
        ]
    },
    {
        "question": "Teachers/Professors (Choose Below)",
        "options": [
            {
                "option": "Not yet",
                "score": 0
            },
            {
                "option": "1 Relationship",
                "score": 1
            },
            {
                "option": "2 Relationships",
                "score": 2
            },
            {
                "option": "3 or more Relationships",
                "score": 3
            }
        ]
    }
]': :jsonb,
3.0
    );
    
    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
38, 
        'Social Capital', 
        'PLUS', 
        'I have proactively asked family members (other than parents/guardians) and friends about their job or career.', 
        '[
    {
        "question": "Family Members (Choose Below)",
        "options": [
            {
                "option": "No and I had not considered this",
                "score": 0
            },
            {
                "option": "Not yet but I plan to",
                "score": 1
            },
            {
                "option": "Yes. Once",
                "score": 2
            },
            {
                "option": "Yes. Multiple times",
                "score": 3
            }
        ]
    },
    {
        "question": "Friends and Family Friends (Choose Below)",
        "options": [
            {
                "option": "No and I had not considered this",
                "score": 0
            },
            {
                "option": "Not yet but I plan to",
                "score": 1
            },
            {
                "option": "Yes. Once",
                "score": 2
            },
            {
                "option": "Yes. Multiple times",
                "score": 3
            }
        ]
    }
]': :jsonb
    );

    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
39, 
        'Social Capital', 
        'PLUS', 
        'I feel confident proactively introducing myself to professionals I have never met (who could be helpful in my career).', 
        '[
    {
        "option": "Strongly Disagree",
        "score": 0
    },
    {
        "option": "Disagree",
        "score": 1
    },
    {
        "option": "Agree",
        "score": 2
    },
    {
        "option": "Strongly Agree",
        "score": 3
    }
]': :jsonb
    );


    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
40, 
        'Social Capital', 
        'PLUS', 
        'I have proactively reached out to an alum from my school to learn about their career path.', 
        '[
    {
        "option": "No and I had not considered this",
        "score": 0
    },
    {
        "option": "Not yet but I plan to",
        "score": 1
    },
    {
        "option": "Yes. Once",
        "score": 2
    },
    {
        "option": "Yes. Multiple times",
        "score": 3
    }
]': :jsonb
    );

    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
41, 
        'Social Capital', 
        'PLUS', 
        "I have proactively asked to have a career conversation with a professional at an organization I'm interested in working for.", 
        '[
    {
        "option": "No and I had not considered this",
        "score": 0
    },
    {
        "option": "Not yet but I plan to",
        "score": 1
    },
    {
        "option": "Yes. Once",
        "score": 2
    },
    {
        "option": "Yes. Multiple times",
        "score": 3
    }
]': :jsonb
    );

    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
42, 
        'Social Capital', 
        'PLUS', 
        'I have proactively asked someone I know to introduce me to someone they know so I can talk to them to learn about their career.', 
        '[
    {
        "option": "No and I had not considered this",
        "score": 0
    },
    {
        "option": "Not yet but I plan to",
        "score": 1
    },
    {
        "option": "Yes. Once",
        "score": 2
    },
    {
        "option": "Yes. Multiple times",
        "score": 3
    }
]': :jsonb
    );

    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
44, 
        'Life Design', 
        'PLUS', 
        'When things don\'t go the way I had envisioned or when I encounter a setback, I recognize that the setback is an opportunity to learn and grow, rather than a \\\"mistake\\\".', 
        '[
    {
        "option": "Strongly Disagree",
        "score": 0
    },
    {
        "option": "Disagree",
        "score": 1
    },
    {
        "option": "Agree",
        "score": 2
    },
    {
        "option": "Strongly Agree",
        "score": 3
    }
]': :jsonb
    );
    
    INSERT INTO question_bank (id, target, question_order, category, org_name, question, options)
    VALUES 
    (
        uuid_generate_v4(),
        '{
    "students"
}',
51, 
        'Career Mobility', 
        'PLUS', 
        'I have received helpful career advice from a faculty member, career counselor, or employer.', 
        '[
    {
        "question": "Professor or Faculty Member (Choose Below)",
        "options": [
            {
                "option": "No and I had not considered this",
                "score": 1
            },
            {
                "option": "Not yet but I plan to",
                "score": 2
            },
            {
                "option": "Yes. Once",
                "score": 3
            },
            {
                "option": "Yes. Multiple times",
                "score": 4
            }
        ]
    },
    {
        "question": "Career Counselor (Choose Below)",
        "options": [
            {
                "option": "No and I had not considered this",
                "score": 1
            },
            {
                "option": "Not yet but I plan to",
                "score": 2
            },
            {
                "option": "Yes. Once",
                "score": 3
            },
            {
                "option": "Yes. Multiple times",
                "score": 4
            }
        ]
    },
    {
        "question": "Employers (Choose Below)",
        "options": [
            {
                "option": "No and I had not considered this",
                "score": 1
            },
            {
                "option": "Not yet but I plan to",
                "score": 2
            },
            {
                "option": "Yes. Once",
                "score": 3
            },
            {
                "option": "Yes. Multiple times",
                "score": 4
            }
        ]
    }
]'::jsonb);