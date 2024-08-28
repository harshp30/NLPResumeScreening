# Threshold for a perfect match in terms of database skills
DB_SKILL_THRESHOLD = 5
# This parameter defines the number of database-related skills that need to be present in the resume
# for the resume to be considered a 100% match for a job requiring database skills.

# Threshold for a perfect match in terms of job description skills
JOB_SKILL_THRESHOLD = 3
# This parameter specifies the number of skills from the job description that must be present in the resume
# to achieve a 100% match with the job description.

# Weight for semantic similarity in the overall match calculation
SEMANTIC_WEIGHT = 0.3
# This parameter represents the weight given to semantic similarity between the resume and job description
# when calculating the match percentage. A value of 0.3 means that 30% of the match score is based on semantic similarity.

# Weight for skills match in the overall match calculation
SKILLS_WEIGHT = 0.7
# This parameter represents the weight given to the number of matching skills between the resume and job description
# in the match percentage calculation. A value of 0.7 means that 70% of the match score is based on the number of matching skills.
